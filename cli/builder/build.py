import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List

from cli.builder.nuitka import build_nuitka_cmd
from cli.builder.pyinstaller import build_pyinstaller_cmd


def gen_version_py(version):
    with open('app/resources/version.py', 'w', encoding='utf-8') as f:
        f.write(f'__version__ = "{version}"\n')


def gen_filelist(root_dir: str, filelist_name: str):
    paths = []
    for current_path, dirs, files in os.walk(root_dir, topdown=False):
        for file in files:
            relative_path = os.path.relpath(os.path.join(current_path, file), root_dir)
            logging.debug(relative_path)
            paths.append(relative_path)
        relative_path = os.path.relpath(os.path.join(current_path, ""), root_dir)
        if relative_path != ".":
            logging.debug(relative_path)
            paths.append(relative_path)

    with open(filelist_name, "w", encoding="utf-8") as f:
        f.write("\n".join(paths))
        f.write("\n")


def build(args, extra_backend_options_list: List[str]):
    """call nuitka to build the app"""
    if sys.platform != 'win32':
        path = Path('build/App')
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
        elif path.exists() and path.is_file():
            path.unlink()
    start = time.perf_counter()
    logging.info('Building the app...')
    if args.backend == 'nuitka':
        cmd = build_nuitka_cmd(args, extra_backend_options_list)
    else:
        cmd = build_pyinstaller_cmd(args)
    logging.debug(' '.join(cmd))
    try:
        result = subprocess.run(cmd, shell=True)
        end = time.perf_counter()
        if result.returncode != 0:
            logging.error(f'Failed to build app in {end - start:.3f}s.')
            sys.exit(1)
        logging.info(f'Build complete in {end - start:.3f}s.')
        if not args.onefile:
            if args.backend == 'nuitka':
                if os.path.exists('build/App'):
                    shutil.rmtree('build/App')
                shutil.move('build/app.dist', 'build/App')
            logging.info("Generate the filelist.")
            gen_filelist('build/App', 'build/App/filelist.txt')
            logging.info("Filelist has been generated.")
    except Exception as e:
        end = time.perf_counter()
        logging.error(f'Exception during build: {e}, time: {end - start:.3f}s.')
        sys.exit(1)
