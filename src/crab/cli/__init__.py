import os
import subprocess
from pathlib import Path

import typer

from crab.core import TemplateRenderer
from crab.integrations.uv import install_dependencies

app = typer.Typer()


@app.command(name="hello")
def hello() -> None:
    typer.echo("Hello, world!")


@app.command(name="init")
def init(
    project_name: str = typer.Argument(..., help="Name of the project"),
    template: str = typer.Option("basic", help="Template to use"),
    author: str = typer.Option("Anonymous", prompt=True),
    setup_git: bool = typer.Option(True, help="Initialize git repository"),
) -> None:
    """Initialize a new Python project."""
    target_dir = Path.cwd() / project_name
    typer.secho("🚀 Creating new project ", nl=False, bold=True)
    typer.secho(f"'{project_name}'", fg=typer.colors.BLUE, nl=False, bold=True)
    typer.secho(" using template ", nl=False, bold=True)
    typer.secho(f"'{template}'", fg=typer.colors.BLUE, bold=True)

    # Initialize template renderer
    try:
        typer.secho("📝 Loading template...", fg=typer.colors.YELLOW)
        renderer = TemplateRenderer(template_name=template)
    except Exception as e:
        typer.secho(f"❌ Error loading template: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # Render template files
    try:
        typer.secho("🔨 Generating project files...", fg=typer.colors.YELLOW)
        renderer.render(
            target_dir,
            {
                "project_name": project_name,
                "author": author,
            },
        )
    except Exception as e:
        typer.secho(f"❌ Error rendering template: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # Change to project directory for remaining operations
    os.chdir(target_dir)

    # Initialize git repository if requested
    if setup_git:
        typer.secho("📦 Initializing git repository...", fg=typer.colors.YELLOW)
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            typer.secho("✅ Git repository initialized!", fg=typer.colors.GREEN)
        except subprocess.CalledProcessError as e:
            typer.secho(
                f"❌ Error initializing git repository: {e}",
                fg=typer.colors.RED,
                err=True,
            )
            typer.secho("⚠️  Continuing without git...", fg=typer.colors.YELLOW)
        except FileNotFoundError:
            typer.secho(
                "⚠️  Git not found. Skipping git initialization...",
                fg=typer.colors.YELLOW,
            )

    # Install dependencies if requested
    typer.secho("📥 Installing dependencies...", fg=typer.colors.YELLOW)
    try:
        install_dependencies(target_dir)

        # Install pre-commit hooks if git is initialized
        if setup_git and Path(".git").exists():
            typer.secho("🔗 Installing pre-commit hooks...", fg=typer.colors.YELLOW)
            try:
                subprocess.run(
                    ["uvx", "pre-commit", "install"],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                typer.secho(
                    f"❌ Error installing pre-commit hooks: {e.stderr.decode()}",
                    fg=typer.colors.RED,
                    err=True,
                )
                raise typer.Exit(code=1)
            typer.secho("✅ Pre-commit hooks installed!", fg=typer.colors.GREEN)

        typer.secho("✅ Dependencies installed!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(
            f"❌ Error installing dependencies: {e}", fg=typer.colors.RED, err=True
        )
        typer.secho(
            "⚠️  You may need to install dependencies manually.",
            fg=typer.colors.YELLOW,
        )

    typer.secho(
        "\n✨ Project initialized successfully! ", fg=typer.colors.GREEN, nl=False
    )
    typer.secho(f"📁 Location: {target_dir}", fg=typer.colors.BLUE)
