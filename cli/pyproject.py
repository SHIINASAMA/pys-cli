import sys
from typing import Tuple, List

import glom
import toml


def load_pyproject() -> Tuple[List[str], List[str]]:
    """get and build vars from pyproject.toml
     1. nuitka command options list
     2. enabled languages list"""
    with open("pyproject.toml") as f:
        data = toml.load(f)
    config = glom.glom(data, "tool.pyside-cli", default={})
    platform_config = glom.glom(data, f"tool.pyside-cli.{sys.platform}", default={})
    config.update(platform_config)

    extra_nuitka_options_list = []
    for k, v in config.items():
        if isinstance(v, list) and v:
            cmd = f"--{k}={','.join(v)}"
            extra_nuitka_options_list.append(cmd)
        elif isinstance(v, str) and v != "":
            cmd = f"--{k}={v}"
            extra_nuitka_options_list.append(cmd)
        elif type(v) is bool and v:
            cmd = f"--{k}"
            extra_nuitka_options_list.append(cmd)

    lang_list = glom.glom(data, "tool.pyside-cli.i18n.languages", default=[])

    return extra_nuitka_options_list, lang_list
