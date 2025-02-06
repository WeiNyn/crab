# Developement

## Project Design

### **1. Core Architecture**

- **Language**: Python (to natively integrate with Python tooling and simplify plugin/extensions later).
- **CLI Framework**: Use [`typer`](https://typer.tiangolo.com/) for clean CLI abstractions.
- **Packaging**: Build a single binary with [`shiv`](https://shiv.readthedocs.io/) or [`PyInstaller`](https://pyinstaller.org/).
- **Modular Design**:
  - **Core Engine**: Configuration parsing, logging, error handling.
  - **Subcommands**: Separate modules for `init`, `add`, `test`, `lint`, `build`, etc.
  - **Template System**: Predefined boilerplates (Jinja2 templates for dynamic scaffolding).
  - **Integration Layer**: Wrappers for `uv`, `pytest`, `ruff`, etc.

---

### **2. Tech Stack**

| Component           | Tool(s)                                                                 |
|----------------------|-------------------------------------------------------------------------|
| Package Management   | `uv` (via CLI invocation)                                               |
| Testing              | `pytest` (with plugins: coverage, parametrize)                          |
| Linting/Formatting   | `ruff` (primary), `mypy`, `isort`, `black`                              |
| Pre-commit Hooks     | `pre-commit` framework                                                  |
| Build/Publish        | `hatch`, `build`, `twine`                                               |
| Templating           | Jinja2                                                                  |
| Config Management    | `pyproject.toml` (PEP 621) + `crab.toml` for project-specific settings  |

---

### **3. Step-by-Step Implementation Plan**

#### **Stage 0: Setup & Scaffolding**

1. **Initialize Crab Project**:
   - Create a Python project with `poetry` or `uv`.
   - Set up CI/CD (GitHub Actions) for testing/linting.
   - Define CLI structure with `typer`.
2. **Configuration System**:
   - Design `crab.toml` to store project-specific settings (e.g., ignored lints, custom test paths).
   - Merge with `pyproject.toml` for PEP-compliance.

#### **Stage 1: Project Initialization (`crab init`)**

- **Templates**:
  - Generate `src/`, `tests/`, `docs/`, and config files (`pyproject.toml`, `.pre-commit-config.yaml`, `README.md`).
  - Inject project name, author, and dependencies into templates.
- **Post-init Setup**:
  - Run `uv pip install -r requirements.txt` (or `uv venv` for virtualenv).
  - Install pre-commit hooks via `pre-commit install`.

#### **Stage 2: Dependency Management (`crab add/remove/update`)**

- Wrap `uv` commands:
  - `crab add requests` → `uv pip install requests` + update `pyproject.toml`.
  - Add flags for dev-dependencies (`--dev`), environment constraints, etc.

#### **Stage 3: Code Quality & CI**

- **Linting**:
  - `crab lint`: Run `ruff`, `mypy`, and `pylint` in sequence.
  - `crab fix`: Auto-fix with `ruff --fix` and `isort`.
- **Testing**:
  - `crab test`: Execute `pytest` with project-specific config (e.g., coverage, xdist).
- **Pre-commit**:
  - Auto-generate `.pre-commit-config.yaml` with recommended hooks (ruff, mypy, etc.).

#### **Stage 4: Build & Publish (`crab build/publish`)**

- Use `build` to create wheels/sdists.
- Integrate `twine` for PyPI uploads (with auth support via environment variables/keyring).

#### **Stage 5: Advanced Features**

- **Dependency Upgrades**: `crab upgrade --all` (leverage `uv`’s upcoming upgrade features).
- **Architecture Analysis**:
  - Generate dependency graphs with `pydeps` or `pyreverse`.
  - Enforce layered architecture rules (e.g., "no imports from `web` to `data`").

---

### **4. Milestones & Timeline**

| Milestone              | Deliverables                                  | Timeline (Weeks) |
|-------------------------|-----------------------------------------------|------------------|
| MVP (Core CLI + Init)   | `init`, `add`, `lint`, `test`                 | 3-4              |
| Beta (Build/Publish)    | `build`, `publish`, pre-commit integration    | 2                |
| Stable 1.0              | Error handling, docs, Windows/Mac support     | 2                |
| Post-1.0 (Enhancements) | Plugins, architecture analysis, auto-updates  | Ongoing          |

---

### **5. Challenges & Mitigation**

- **Tool Compatibility**: Test across Python 3.8+ and major OSes.
- **Performance**: Optimize subprocess calls (e.g., parallelize `ruff` and `mypy`).
- **User Experience**: Provide clear error messages and `--verbose` logging.
- **Community Adoption**: Publish to PyPI, write tutorials, and engage Python forums.

---

### **6. Example Workflow**

```bash
# Create a project
crab init my_project --venv
cd my_project

# Add dependencies
crab add pandas numpy
crab add --dev pytest

# Auto-format and lint
crab fix
crab lint

# Test and publish
crab test
crab build
crab publish
```

---

By focusing on composability and leveraging existing tools under the hood, **Crab** can become the "batteries-included" CLI Python developers need. Start small, iterate fast, and build momentum with early adopters!
