# dotfiles-icon-templates/src/dotfiles_icon_templates/cli/commands/copy.py
"""Copy command for icon templates CLI."""
from pathlib import Path
from typing import List, Optional

import typer

from dotfiles_icon_templates.services.icon_templates_service import (
    IconTemplatesService,
    IconTemplateError,
    CategoryNotFoundError,
    IconNotFoundError,
)


def get_service() -> IconTemplatesService:
    """Create a service with default data directory."""
    return IconTemplatesService()


def copy_icons(
    target: Path = typer.Argument(
        ...,
        help="Target directory where icons will be copied"
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Copy only icons from this category"
    ),
    icons: Optional[str] = typer.Option(
        None,
        "--icons",
        "-i",
        help="Comma-separated list of specific icon names to copy"
    ),
) -> None:
    """Copy icon templates to target directory."""
    service = get_service()

    try:
        # Parse icons if provided
        icon_list = None
        if icons:
            icon_list = [name.strip() for name in icons.split(",")]

        copied = service.copy(target, category=category, icons=icon_list)

        if not copied:
            typer.echo("No icons copied")
            return

        typer.echo(f"Copied {len(copied)} icon(s) to {target.resolve()}")

    except (CategoryNotFoundError, IconNotFoundError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except IconTemplateError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
