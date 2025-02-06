from pathlib import Path

import typer

from src.crab.core import TemplateRenderer
from src.crab.integrations.uv import create_venv

app = typer.Typer()


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project"),
    template: str = typer.Option("basic", help="Template to use"),
    venv: bool = typer.Option(False, help="Create a virtual environment with uv"),
    author: str = typer.Option("Anonymous", prompt=True),
) -> None:
    """Initialize a new Python project."""
    target_dir = Path.cwd() / project_name
    renderer = TemplateRenderer(template_name=template)

    # Render template files
    renderer.render(
        target_dir,
        {
            "project_name": project_name,
            "author": author,
        },
    )

    # Create venv if requested
    try:
        if venv:
            create_venv(target_dir / ".venv")  # Default venv path
    except (RuntimeError, FileExistsError) as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Project initialized at {target_dir}!")
