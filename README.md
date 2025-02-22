# 🦀 Crab - Modern Python Project Manager

Crab is a batteries-included CLI tool that streamlines Python project setup and management by automating boilerplate configuration and integrating modern development tools.

## Features

- 🚀 **Quick Project Setup**: Create new Python projects with best practices using `crab init`
- 🛠 **Modern Tooling**: Pre-configured integration with:
  - [`uv`](https://github.com/astral-sh/uv) for fast package management
  - [`ruff`](https://github.com/astral-sh/ruff) for linting and formatting
  - [`mypy`](https://github.com/python/mypy) for type checking
  - [`pytest`](https://github.com/pytest-dev/pytest) for testing
  - [`pre-commit`](https://github.com/pre-commit/pre-commit) for git hooks
- ⚙️ **PEP-Compliant**: Uses `pyproject.toml` for configuration
- 🔄 **Git Integration**: Automatic git repository initialization
- 📦 **Dependency Management**: Simple commands to add, remove, and update packages

## Installation

```bash
pip install rcrab
```

## Quick Start

1. Create a new project

```bash
crab init my_project
cd my_project
```

2. Add dependencies:

```bash
uv add pandas numpy
```

3. Run code quality tools:

```bash
make lint
make fix
```

4. Run test

```bash
make test
```

### Configuration

Crab uses pyproject.toml for project configuration. Default settings are automatically created during project initialization.

Example configuration:

```toml
[tool.crab]
template = "basic"
venv-directory = ".venv"

[tool.crab.paths]
source = "src"
tests = "tests"
docs = "docs"

[tool.crab.lint]
enabled-tools = ["ruff", "mypy"]
```
