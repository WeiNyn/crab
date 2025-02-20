"""Test cases for the template renderer."""

from pathlib import Path

import jinja2
import pytest

from crab.core.template import TemplateRenderer


@pytest.fixture
def mock_template_dir(temp_dir: Path) -> Path:
    """Create a mock template directory with test templates."""
    template_dir = temp_dir / "templates" / "test_template"
    template_dir.mkdir(parents=True)

    # Create a simple template file
    (template_dir / "{{ project_name }}.py.j2").write_text(
        """
# {{ project_name }} by {{ author }}
VERSION = "{{ version }}"
    """.strip()
    )

    # Create a nested template
    nested_dir = template_dir / "{{ project_name }}" / "src"
    nested_dir.mkdir(parents=True)
    (nested_dir / "__init__.py.j2").write_text(
        """
\"\"\"{{ project_name }} - {{ description }}\"\"\"

__version__ = "{{ version }}"
__author__ = "{{ author }}"
    """.strip()
    )

    return template_dir


@pytest.fixture
def mock_template_loader(
    mock_template_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Mock the template loader to use our test templates."""

    def mock_loader(path: str) -> jinja2.FileSystemLoader:
        return jinja2.FileSystemLoader(mock_template_dir.parent)

    monkeypatch.setattr("jinja2.FileSystemLoader", mock_loader)


def test_template_rendering(temp_dir: Path, mock_template_loader: None) -> None:
    """Test basic template rendering."""
    renderer = TemplateRenderer(template_name="test_template")
    target_dir = temp_dir / "output"

    context = {
        "project_name": "test-project",
        "author": "Test Author",
        "version": "0.1.0",
        "description": "A test project",
    }

    renderer.render(target_dir, context)

    # Check root level template
    root_file = target_dir / "test-project.py"
    assert root_file.exists()
    content = root_file.read_text()
    assert "test-project by Test Author" in content
    assert 'VERSION = "0.1.0"' in content

    # Check nested template
    init_file = target_dir / "test-project" / "src" / "__init__.py"
    assert init_file.exists()
    content = init_file.read_text()
    assert "test-project - A test project" in content
    assert '__version__ = "0.1.0"' in content
    assert '__author__ = "Test Author"' in content


def test_template_not_found(temp_dir: Path, mock_template_loader: None) -> None:
    """Test handling of non-existent template."""
    with pytest.raises(Exception, match="Template.*not found"):
        TemplateRenderer(template_name="nonexistent")


def test_invalid_context(temp_dir: Path, mock_template_loader: None) -> None:
    """Test rendering with missing context variables."""
    renderer = TemplateRenderer(template_name="test_template")
    target_dir = temp_dir / "output"

    # Missing required context variables
    context = {
        "project_name": "test-project",
        # missing author and version
    }

    with pytest.raises(jinja2.UndefinedError):
        renderer.render(target_dir, context)


def test_existing_output_directory(temp_dir: Path, mock_template_loader: None) -> None:
    """Test rendering to an existing directory."""
    renderer = TemplateRenderer(template_name="test_template")
    target_dir = temp_dir / "output"
    target_dir.mkdir()

    context = {
        "project_name": "test-project",
        "author": "Test Author",
        "version": "0.1.0",
        "description": "A test project",
    }

    # Should not raise an exception
    renderer.render(target_dir, context)
    assert target_dir.exists()
