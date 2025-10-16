import logging
import os
import shutil
import site


def _add_path():
    appended_path = ""
    items = site.getsitepackages()

    package_names = [
        "PySide6"
    ]

    for item in items:
        for package_name in package_names:
            full_path = os.path.join(item, package_name)
            if os.path.exists(full_path):
                appended_path += full_path + os.path.pathsep

    os.environ["PATH"] += appended_path


def find_toolchain():
    _add_path()
    toolchain = Toolchain()
    toolchain.git_executable = shutil.which("git")
    toolchain.uic_executable = shutil.which("uic")
    toolchain.rcc_executable = shutil.which("rcc")
    toolchain.lupdate_executable = shutil.which("lupdate")
    toolchain.lrelease_executable = shutil.which("lrelease")
    toolchain.nuitka_executable = shutil.which("nuitka")
    toolchain.pyinstaller_executable = shutil.which("pyinstaller")
    toolchain.pytest_executable = shutil.which("pytest")
    return toolchain


class Toolchain:
    git_executable = None
    uic_executable = None
    rcc_executable = None
    lupdate_executable = None
    lrelease_executable = None
    nuitka_executable = None
    pyinstaller_executable = None
    pytest_executable = None

    def print_toolchain(self):
        logging.info("Found toolchain:")

        logging.info(f"GIT: {self.git_executable is not None}")
        logging.info(f"UIC: {self.uic_executable is not None}")
        logging.info(f"RCC: {self.rcc_executable is not None}")
        logging.info(f"LUPDATE: {self.lupdate_executable is not None}")
        logging.info(f"LRELEASE: {self.lrelease_executable is not None}")
        logging.info(f"NUITKA: {self.nuitka_executable is not None}")
        logging.info(f"PYINSTALLER: {self.pyinstaller_executable is not None}")
        logging.info(f"PYTEST: {self.pytest_executable is not None}")

        logging.debug(f"Path to GIT: {self.git_executable}")
        logging.debug(f"Path to UIC: {self.rcc_executable}")
        logging.debug(f"Path to RCC: {self.rcc_executable}")
        logging.debug(f"Path to LUPDATE: {self.lupdate_executable}")
        logging.debug(f"Path to LRELEASE: {self.lrelease_executable}")
        logging.debug(f"Path to NUITKA: {self.nuitka_executable}")
        logging.debug(f"Path to PYINSTALLER: {self.pyinstaller_executable}")
        logging.debug(f"Path to PYTEST: {self.pytest_executable}")
