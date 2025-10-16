import logging
import subprocess

from cli.toolchain import Toolchain


def run_test(toolchain: Toolchain, args):
    if toolchain.pytest_executable is None:
        logging.warning("Pytest executable not found, skipping test")
        return -1
    cmd = ['pytest'] + args.backend_args
    logging.debug(' '.join(cmd))
    result = subprocess.run(cmd, shell=True)
    return result.returncode
