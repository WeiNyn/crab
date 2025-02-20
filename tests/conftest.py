"""Common test fixtures and utilities."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        old_cwd = os.getcwd()
        os.chdir(tmp_dir)
        try:
            yield Path(tmp_dir)
        finally:
            os.chdir(old_cwd)


@pytest.fixture
def sample_pyproject_toml(temp_dir: Path) -> Path:
    """Create a sample pyproject.toml file."""
    content = """
[project]
name = "test-project"
version = "0.1.0"
description = "Test project"
authors = [{ name = "Test Author" }]
dependencies = []
requires-python = ">=3.8"

[tool.crab]
template = "basic"
venv_directory = ".venv"

[tool.crab.paths]
source = "src"
tests = "tests"
docs = "docs"

[tool.crab.lint]
enabled_tools = ["ruff", "mypy"]

[tool.crab.test]
directory = "tests"
pytest_args = ["-v", "--cov"]

[tool.crab.test.coverage]
enable = true
threshold = 90
"""
    pyproject_path = temp_dir / "pyproject.toml"
    pyproject_path.write_text(content)
    return pyproject_path


@pytest.fixture
def mock_venv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock UV venv creation for testing."""

    def mock_create_venv(venv_dir: Path) -> None:
        venv_dir.mkdir(parents=True)
        (venv_dir / "pyvenv.cfg").touch()

    monkeypatch.setattr("crab.integrations.uv.create_venv", mock_create_venv)


@pytest.fixture
def mock_git(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock git initialization for testing."""

    def mock_run(*args, **kwargs) -> subprocess.CompletedProcess:
        # Create .git directory to simulate git init
        if len(args) > 0 and isinstance(args[0], list) and args[0][0] == "git":
            cwd = kwargs.get("cwd", Path.cwd())
            git_dir = Path(cwd) / ".git"
            git_dir.mkdir(exist_ok=True)
        return subprocess.CompletedProcess(args, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr("subprocess.run", mock_run)


@pytest.fixture
def mock_install_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock dependency installation for testing."""

    def mock_install(*args, **kwargs) -> None:
        pass

    monkeypatch.setattr("crab.integrations.uv.install_dependencies", mock_install)
