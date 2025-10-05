import logging
import subprocess


def run_test(args):
    cmd = ['pytest'] + args.backend_args
    logging.debug(' '.join(cmd))
    result = subprocess.run(cmd)
    return result.returncode
