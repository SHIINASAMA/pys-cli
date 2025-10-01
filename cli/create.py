import logging
import shutil
import subprocess
from pathlib import Path

import toml
from glom import assign


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
    data = toml.load(pyproject_file)
    assign(data, 'project.name', name)
    with pyproject_file.open('w', encoding='utf-8') as f:
        toml.dump(data, f)

    git_dir = project_path / '.git'
    shutil.rmtree(git_dir)

    subprocess.run(
        [
            'git',
            'init'
        ],
        cwd=project_path
    )

    logging.info(f"Project {name} created successfully.")
