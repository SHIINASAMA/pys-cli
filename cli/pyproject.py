import sys

import glom
import toml

class PyProjectConfig:
    extra_nuitka_options_list = []
    extra_pyinstaller_options_list = []
    lang_list = []

    def __init__(self):
        """get and build vars from pyproject.toml
         1. nuitka command options list
         2. pyinstaller command options list
         3. enabled languages list"""
        with open("pyproject.toml") as f:
            data = toml.load(f)
        nuitka_config = glom.glom(data, "tool.pyside-cli", default={})
        nuitka_platform_config = glom.glom(data, f"tool.pyside-cli.{sys.platform}", default={})
        nuitka_config.update(nuitka_platform_config)

        for k, v in nuitka_config.items():
            if isinstance(v, list) and v:
                cmd = f"--{k}={','.join(v)}"
                self.extra_nuitka_options_list.append(cmd)
            elif isinstance(v, str) and v != "":
                cmd = f"--{k}={v}"
                self.extra_nuitka_options_list.append(cmd)
            elif type(v) is bool and v:
                cmd = f"--{k}"
                self.extra_nuitka_options_list.append(cmd)

        pyinstaller_config = glom.glom(data, "tool.pyside-cli.pyinstaller", default={})
        for k, v in pyinstaller_config.items():
            if isinstance(v, list) and v:
                cmd = f"--{k}={','.join(v)}"
                self.extra_pyinstaller_options_list.append(cmd)
            elif isinstance(v, str) and v != "":
                cmd = f"--{k}={v}"
                self.extra_pyinstaller_options_list.append(cmd)
            elif type(v) is bool and v:
                cmd = f"--{k}"
                self.extra_pyinstaller_options_list.append(cmd)

        self.lang_list = glom.glom(data, "tool.pyside-cli.i18n.languages", default=[])

