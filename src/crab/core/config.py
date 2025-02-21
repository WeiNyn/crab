from pathlib import Path
from typing import Dict, List, Optional, Union

import tomli
from pydantic import BaseModel, Field


class PreCommitToolConfig(BaseModel):
    enabled: bool = True
    args: Optional[List[str]] = None
    require_serial: bool = True


class LintConfig(BaseModel):
    isort: PreCommitToolConfig = Field(
        default_factory=lambda: PreCommitToolConfig(args=["--profile", "black"])
    )
    mypy: PreCommitToolConfig = Field(
        default_factory=lambda: PreCommitToolConfig(
            args=["--strict", "--explicit-package-bases"]
        )
    )
    ruff_format: PreCommitToolConfig = Field(
        default_factory=lambda: PreCommitToolConfig()
    )
    ruff_lint: PreCommitToolConfig = Field(
        default_factory=lambda: PreCommitToolConfig(args=["--fix"])
    )


class DependencyGroup(BaseModel):
    name: str
    packages: List[str]


def default_dependencies() -> Dict[str, List[Union[str, DependencyGroup]]]:
    return {
        "sources": ["https://pypi.org/simple"],
        "groups": [
            DependencyGroup(
                name="dev",
                packages=[
                    "isort",
                    "mypy",
                    "ruff",
                    "pre-commit",
                ],
            )
        ],
    }


def default_test() -> Dict[str, Union[str, List[str], Dict[str, Union[bool, int]]]]:
    return {
        "directory": "tests",
        "pytest_args": ["-v"],
        "coverage": {"enable": True, "threshold": 90},
    }


class CrabConfig(BaseModel):
    # Project Metadata
    template: str = "basic"
    venv_directory: str = ".venv"

    # Dependency Management
    dependencies: Dict[str, List[Union[str, DependencyGroup]]] = Field(
        default_factory=default_dependencies
    )

    # Linting
    lint: LintConfig = Field(default_factory=LintConfig)

    # Testing
    test: Dict[str, Union[str, List[str], Dict[str, Union[bool, int]]]] = Field(
        default_factory=default_test
    )

    # Paths
    paths: Dict[str, str] = Field(
        default_factory=lambda: {
            "source": "src",
            "tests": "tests",
            "docs": "docs",
        }
    )

    @classmethod
    def load(cls, path: Path) -> "CrabConfig":
        """Load and validate configuration from pyproject.toml.

        Args:
            path: Path to pyproject.toml file.

        Returns:
            CrabConfig: Validated configuration object.

        Raises:
            FileNotFoundError: If pyproject.toml doesn't exist.
            KeyError: If [tool.crab] section is missing.
            ValueError: If configuration is invalid.
        """
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, "rb") as f:
            data = tomli.load(f)

        try:
            crab_config = data["tool"]["crab"]
        except KeyError:
            raise KeyError("Missing [tool.crab] section in pyproject.toml")

        return cls(**crab_config)
