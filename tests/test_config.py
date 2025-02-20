"""Test cases for the config module."""

from pathlib import Path

import pytest

from crab.core.config import CrabConfig


def test_load_valid_config(sample_pyproject_toml: Path) -> None:
    """Test loading a valid configuration."""
    config = CrabConfig.load(sample_pyproject_toml)

    assert config.template == "basic"
    assert config.venv_directory == ".venv"
    assert config.paths["source"] == "src"
    assert config.paths["tests"] == "tests"
    assert config.paths["docs"] == "docs"
    assert config.lint["enabled_tools"] == ["ruff", "mypy"]
    assert config.test["directory"] == "tests"
    assert config.test["pytest_args"] == ["-v", "--cov"]
    assert config.test["coverage"]["enable"] is True
    assert config.test["coverage"]["threshold"] == 90


def test_load_missing_file(temp_dir: Path) -> None:
    """Test loading a non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        CrabConfig.load(temp_dir / "nonexistent.toml")


def test_load_missing_crab_section(temp_dir: Path) -> None:
    """Test loading a pyproject.toml without [tool.crab] section."""
    pyproject = temp_dir / "pyproject.toml"
    pyproject.write_text("""
[project]
name = "test"
version = "0.1.0"
    """)

    with pytest.raises(KeyError, match="Missing \\[tool.crab\\] section"):
        CrabConfig.load(pyproject)


def test_default_values() -> None:
    """Test default configuration values."""
    config = CrabConfig()

    assert config.template == "basic"
    assert config.venv_directory == ".venv"
    assert config.paths == {
        "source": "src",
        "tests": "tests",
        "docs": "docs",
    }
    assert config.lint["enabled_tools"] == ["ruff", "mypy"]
    assert config.test["directory"] == "tests"
    assert config.test["pytest_args"] == ["-v"]
    assert config.test["coverage"]["enable"] is True
    assert config.test["coverage"]["threshold"] == 90


def test_partial_config(temp_dir: Path) -> None:
    """Test loading a partial configuration with some values overridden."""
    pyproject = temp_dir / "pyproject.toml"
    pyproject.write_text("""
[tool.crab]
template = "custom"
venv_directory = "venv"

[tool.crab.paths]
source = "custom_src"
    """)

    config = CrabConfig.load(pyproject)
    assert config.template == "custom"
    assert config.venv_directory == "venv"
    assert config.paths["source"] == "custom_src"
    # Check defaults are still set
    assert config.paths["tests"] == "tests"
    assert config.paths["docs"] == "docs"
