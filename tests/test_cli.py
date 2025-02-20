"""Test cases for the CLI commands."""

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from crab.cli import app


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


def test_init_basic(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test basic project initialization."""
    os.chdir(temp_dir)

    result = runner.invoke(
        app,
        ["init", "test-project", "--author", "Test Author"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, f"Command failed with output:\n{result.stdout}"

    project_dir = temp_dir / "test-project"
    assert project_dir.exists()

    # Check basic files
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / "src").is_dir()
    assert (project_dir / "tests").is_dir()
    assert (project_dir / "docs").is_dir()


def test_init_with_venv(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test project initialization with virtual environment."""
    os.chdir(temp_dir)

    result = runner.invoke(
        app,
        ["init", "test-project", "--author", "Test Author", "--venv"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, f"Command failed with output:\n{result.stdout}"

    venv_dir = temp_dir / "test-project" / ".venv"
    assert venv_dir.exists()
    assert (venv_dir / "pyvenv.cfg").exists()


def test_init_with_git(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test project initialization with git."""
    os.chdir(temp_dir)

    result = runner.invoke(
        app,
        ["init", "test-project", "--author", "Test Author", "--setup-git"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, f"Command failed with output:\n{result.stdout}"

    git_dir = temp_dir / "test-project" / ".git"
    assert git_dir.exists()


def test_init_existing_directory(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test initialization in existing directory."""
    os.chdir(temp_dir)

    project_dir = temp_dir / "test-project"
    project_dir.mkdir()
    (project_dir / "existing_file.txt").touch()

    result = runner.invoke(
        app,
        ["init", "test-project", "--author", "Test Author"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, f"Command failed with output:\n{result.stdout}"

    # Check that existing files are preserved
    assert (project_dir / "existing_file.txt").exists()
    # Check that new files are created
    assert (project_dir / "pyproject.toml").exists()


def test_init_invalid_name(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test initialization with invalid project name."""
    os.chdir(temp_dir)

    result = runner.invoke(
        app,
        ["init", "../invalid", "--author", "Test Author"],
        catch_exceptions=False,
    )
    assert result.exit_code != 0
    assert "Invalid project name" in result.stdout or "Invalid project name" in str(
        result.exception
    )


def test_init_no_install(
    runner: CliRunner,
    temp_dir: Path,
    mock_venv: None,
    mock_git: None,
    mock_install_deps: None,
) -> None:
    """Test initialization without dependency installation."""
    os.chdir(temp_dir)

    result = runner.invoke(
        app,
        [
            "init",
            "test-project",
            "--author",
            "Test Author",
            "--no-install",
            "--no-setup-git",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, f"Command failed with output:\n{result.stdout}"

    # Check that pyproject.toml exists but no venv or git
    project_dir = temp_dir / "test-project"
    assert (project_dir / "pyproject.toml").exists()
    assert not (project_dir / ".venv").exists()
    assert not (project_dir / ".git").exists()
