import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def create_venv(venv_dir: Path) -> None:
    """
    Create a Python virtual environment using `uv`.

    Args:
        venv_dir: Path to the virtual environment directory (e.g., `.venv`).

    Raises:
        RuntimeError: If `uv` is not installed or the command fails.
        FileExistsError: If the target directory already exists.
    """
    # Check if uv is installed
    uv_path: Optional[str] = shutil.which("uv")
    if not uv_path:
        raise RuntimeError(
            "uv is not installed. Install it with `pip install uv` or see "
            "https://github.com/astral-sh/uv for instructions."
        )

    # Check for existing venv directory
    if venv_dir.exists():
        raise FileExistsError(
            f"Virtual environment directory '{venv_dir}' already exists. "
            "Delete it or choose a different path."
        )

    # Run `uv venv` command
    try:
        result = subprocess.run(
            [uv_path, "venv", str(venv_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.debug("uv venv output:\n%s", result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("uv venv failed (exit code %d):\n%s", e.returncode, e.stderr)
        raise RuntimeError(
            f"Failed to create virtual environment: {e.stderr.strip()}"
        ) from e

    logger.info("Virtual environment created at %s", venv_dir)


def install_dependencies(project_dir: Path) -> None:
    """Install project dependencies using uv."""
    cmd = ["uv", "sync"]
    try:
        subprocess.run(cmd, check=True, capture_output=False, cwd=project_dir)
    except subprocess.CalledProcessError as e:
        logger.error("uv sync failed (exit code %d):\n%s", e.returncode, e.stderr)
        raise RuntimeError(f"Failed to install dependencies: {e.stderr.strip()}") from e
