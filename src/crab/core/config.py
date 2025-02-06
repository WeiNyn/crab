from pathlib import Path
from typing import Dict, List, Optional, Union

import tomli
from pydantic import BaseModel, Field


class DependencyGroup(BaseModel):
    name: str
    packages: List[str]


class LintToolConfig(BaseModel):
    args: Optional[List[str]] = None
    config: Optional[str] = None


def default_dependencies() -> Dict[str, List[Union[str, DependencyGroup]]]:
    return {
        "sources": ["https://pypi.org/simple"],
        "groups": [DependencyGroup(name="dev", packages=["pytest", "ruff"])],
    }


def default_lint() -> Dict[str, Union[List[str], LintToolConfig]]:
    return {
        "enabled_tools": ["ruff", "mypy"],
        "ruff": LintToolConfig(args=["--fix"], config="ruff.toml"),
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
    lint: Dict[str, Union[List[str], LintToolConfig]] = Field(
        default_factory=default_lint
    )

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
        """Load and validate crab.toml."""

        with open(path, "rb") as f:
            data = tomli.load(f)
        return cls(**data)
