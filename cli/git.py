import logging
import subprocess

from cli.toolchain import Toolchain


def get_last_tag(toolchain: Toolchain, default="0.0.0.0") -> str:
    """Get the last git tag as version, or return default if not found."""
    if toolchain.git_executable is None:
        logging.warning("Git executable not found, skipping get tag.")
        return default
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0", "--first-parent"],
            stderr=subprocess.DEVNULL,
            text=True,
            shell=True
        ).strip()
    except subprocess.CalledProcessError:
        return default

    return tag if tag else default
