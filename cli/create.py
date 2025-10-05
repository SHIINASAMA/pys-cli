import logging
import os
import shutil
import stat
import subprocess
from pathlib import Path

import toml
from glom import assign, delete, glom


def _remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _remove_git(path: Path):
    shutil.rmtree(path, onerror=_remove_readonly)


def create(name: str):
    dst = name
    if name == '.':
        name = Path.cwd().name
        dst = '.'

    logging.info(f"Creating ...")

    rt = subprocess.run([
        'git',
        'clone',
        'https://github.com/SHIINASAMA/pyside_template.git',
        dst
    ])
    if rt.returncode:
        logging.error('Failed to clone template')
        return

    project_path = Path(dst)
    pyproject_file = project_path / 'pyproject.toml'

    with pyproject_file.open('r', encoding='utf-8') as f:
        data = toml.load(f)

    assign(data, 'project.name', name)
    value = glom(data, "project.scripts.pyside_template")
    delete(data, "project.scripts.pyside_template")
    assign(data, f'project.scripts.{name}', value)

    with pyproject_file.open('w', encoding='utf-8') as f:
        toml.dump(data, f)

    git_dir = project_path / '.git'
    _remove_git(git_dir)

    subprocess.run([
        'git',
        'init'],
        cwd=project_path
    )

    logging.info(f"Project {name} created successfully")
