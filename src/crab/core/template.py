from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict

import jinja2
import toml
import yaml


class TemplateRenderer:
    def __init__(self, template_name: str = "basic"):
        self.template_name = template_name
        search_path = (
            Path(__file__).parent.parent / "data" / "templates" / template_name
        )
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(search_path) + "/"),
            autoescape=False,
            keep_trailing_newline=True,
        )

    def render(
        self,
        target_dir: Path,
        context: Dict[str, Any],
    ) -> None:
        # Create project directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy and render all template files
        for template_path in self.env.list_templates():
            template = self.env.get_template(template_path)
            rendered_content = template.render(**context)

            # Replace {{ project_name }} in paths and handle .j2 extension
            output_file = template_path.replace(
                "{{ project_name }}", context["project_name"]
            )

            output_path: Path = target_dir.parent / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered_content)

            pyproject_renderer = PyprojectRenderer()
            pyproject_renderer.render(
                target_dir,
                context["project_name"],
                context["author"],
                self.template_name,
            )

            pre_commit_hook_renderer = PreCommitHookRenderer()
            pre_commit_hook_renderer.render(target_dir)

            # Add Makefile rendering
            makefile_renderer = MakefileRenderer()
            makefile_renderer.render(target_dir)


class PreCommitHookRenderer:
    def __init__(self):
        self.mypy: bool = True
        self.ruff: bool = True
        self.black: bool = False
        self.isort: bool = True

    def with_mypy(self, enabled: bool = True) -> "PreCommitHookRenderer":
        self.mypy = enabled
        return self

    def with_ruff(self, enabled: bool = True) -> "PreCommitHookRenderer":
        self.ruff = enabled
        return self

    def with_black(self, enabled: bool = True) -> "PreCommitHookRenderer":
        self.black = enabled
        return self

    def with_isort(self, enabled: bool = True) -> "PreCommitHookRenderer":
        self.isort = enabled
        return self

    def _render_mypy(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "mypy",
                "name": "mypy",
                "entry": "mypy",
                "language": "python",
                "types": ["python"],
                "args": ["--install-type", "--non-interactive"],
            }
        ]

    def _render_ruff(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "ruff-format",
                "name": "ruff format",
                "entry": "ruff format",
                "language": "python",
                "types": ["python"],
                "require_serial": True,
            },
            {
                "id": "ruff-checck",
                "name": "ruff check",
                "entry": "ruff check",
                "language": "python",
                "types": ["python"],
                "args": ["--fix"],
            },
        ]

    def _render_black(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "black",
                "name": "black",
                "entry": "black",
                "language": "python",
                "types": ["python"],
            }
        ]

    def _render_isort(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "isort",
                "name": "isort",
                "entry": "isort",
                "language": "python",
                "types": ["python"],
            }
        ]

    def render(self, target_dir: Path) -> None:
        hooks = []

        if self.mypy:
            hooks.extend(self._render_mypy())
        if self.ruff:
            hooks.extend(self._render_ruff())
        if self.black:
            hooks.extend(self._render_black())
        if self.isort:
            hooks.extend(self._render_isort())

        config = {}
        config["repos"] = [
            {
                "repo": "local",
                "hooks": hooks,
            }
        ]
        with open(target_dir / ".pre-commit-config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(config, f, sort_keys=False)


class PyprojectRenderer:
    def __init__(self):
        self.dependencies = []
        self.dev_dependencies = [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
        ]
        self.ruff = True
        self.mypy = True
        self.black = False
        self.isort = True

    def with_dependency(self, dependency: str) -> "PyprojectRenderer":
        self.dependencies.append(dependency)
        return self

    def with_dev_dependency(self, dependency: str) -> "PyprojectRenderer":
        self.dev_dependencies.append(dependency)
        return self

    def with_ruff(self, enabled: bool = True) -> "PyprojectRenderer":
        self.ruff = enabled
        return self

    def with_mypy(self, enabled: bool = True) -> "PyprojectRenderer":
        self.mypy = enabled
        return self

    def with_black(self, enabled: bool = True) -> "PyprojectRenderer":
        self.black = enabled
        return self

    def with_isort(self, enabled: bool = True) -> "PyprojectRenderer":
        self.isort = enabled
        return self

    def _render_ruff(self) -> dict[str, Any]:
        return (
            {
                "tool": {
                    "ruff": {
                        "line-length": 88,
                        "target-version": "py38",
                        "lint": {
                            "select": ["E4", "E7", "E9", "F"],
                            "ignore": [],
                        },
                    },
                    "format": {
                        "quote-style": "double",
                        "indent-style": "space",
                        "skip-magic-trailing-comma": False,
                        "line-ending": "auto",
                    },
                },
            }
            if self.ruff
            else {}
        )

    def _render_mypy(self) -> dict[str, Any]:
        return (
            {
                "tool": {
                    "mypy": {
                        "strict_optional": True,
                        "disallow_untyped_defs": False,
                        "disallow_untyped_calls": False,
                        "disallow_untyped_decorators": False,
                        "disallow_subclassing_any": True,
                        "incremental": True,
                        "show_error_codes": True,
                        "strict": True,
                        "ignore_missing_imports": True,
                        "follow_imports": "silent",
                        "cache_dir": ".mypy_cache",
                        "warn_unused_ignores": True,
                        "warn_redundant_casts": True,
                        "warn_return_any": True,
                        "warn_unreachable": True,
                    },
                }
            }
            if self.mypy
            else {}
        )

    def _render_black(self) -> dict[str, Any]:
        return (
            {
                "tool": {
                    "black": {
                        "line-length": 88,
                        "target-version": ["py38"],
                    },
                }
            }
            if self.black
            else {}
        )

    def _render_isort(self) -> dict[str, Any]:
        return (
            {
                "tool": {
                    "isort": {
                        "profile": "black",
                    },
                }
            }
            if self.isort
            else {}
        )

    def _render_crab(self, template: str, venv_directory: str) -> dict[str, Any]:
        return {
            "tool": {
                "crab": {
                    "template": template,
                    "venv-directory": venv_directory,
                },
                "paths": {
                    "source": "src",
                    "tests": "tests",
                    "docs": "docs",
                },
                "lint": {
                    "enabled-tools": ["ruff", "mypy"],
                },
                "test": {
                    "directory": "tests",
                    "pytest-args": ["-v", "--cov"],
                    "coverage": {
                        "enable": True,
                        "threshold": 90,
                    },
                },
            }
        }

    def _render_pytest(self) -> dict[str, Any]:
        return {
            "tool": {
                "pytest": {
                    "ini_options": {
                        "testpaths": ["tests"],
                    },
                },
            }
        }

    def _render_project(self, project_name: str, author: str) -> dict[str, Any]:
        return {
            "project": {
                "name": project_name,
                "version": "0.1.0",
                "description": "My new Python project",
                "authors": [{"name": author}],
                "dependencies": self.dependencies,
                "requires-python": ">=3.11",
                "readme": "README.md",
                "license": {
                    "text": "MIT",
                },
            }
        }

    def _render_devl_dependencies(self) -> dict[str, Any]:
        return {
            "dependency-groups": {
                "dev": self.dev_dependencies,
            }
        }

    def render(
        self, target_dir: Path, project_name: str, author: str, template: str
    ) -> None:
        config: OrderedDict[Any, Any] = OrderedDict()

        config = _merge_dictionaries(config, self._render_project(project_name, author))
        config = _merge_dictionaries(config, self._render_crab(template, ".venv"))
        config = _merge_dictionaries(config, self._render_ruff())
        config = _merge_dictionaries(config, self._render_mypy())
        config = _merge_dictionaries(config, self._render_black())
        config = _merge_dictionaries(config, self._render_isort())
        config = _merge_dictionaries(config, self._render_pytest())
        config = _merge_dictionaries(config, self._render_devl_dependencies())

        with open(target_dir / "pyproject.toml", "w", encoding="utf-8") as f:
            f.write(toml.dumps(config))


def _merge_dictionaries(
    dict1: OrderedDict[Any, Any], dict2: dict[Any, Any]
) -> OrderedDict[Any, Any]:
    """
    Recursive merge dictionaries.

    :param dict1: Base dictionary to merge.
    :param dict2: Dictionary to merge on top of base dictionary.
    :return: Merged dictionary
    """
    merged_dict = OrderedDict()
    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            merged_dict[key] = _merge_dictionaries(
                OrderedDict(val), OrderedDict(dict2_node)
            )
        else:
            if key not in dict2:
                merged_dict[key] = val

    for key, val in dict2.items():
        if key not in dict1:
            merged_dict[key] = val

    return merged_dict


class MakefileRenderer:
    def __init__(self):
        self.template = """
.PHONY: lint fix test build clean

SRC_DIR = src
TEST_DIR = tests

lint:
\truff check $(SRC_DIR) $(TEST_DIR)
\tmypy $(SRC_DIR) $(TEST_DIR)

fix:
\tisort $(SRC_DIR) $(TEST_DIR)
\truff format $(SRC_DIR) $(TEST_DIR)

test:
\tpytest -v 

build: clean
\tpython -m build

clean:
\trm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage .mypy_cache/ .ruff_cache/
"""

    def render(self, target_dir: Path) -> None:
        with open(target_dir / "Makefile", "w", encoding="utf-8") as f:
            f.write(self.template.lstrip())
