# dotfiles-icon-templates/src/dotfiles_icon_templates/cli/commands/list.py
"""List command for icon templates CLI."""
from typing import Optional

import typer

from dotfiles_icon_templates.services.icon_templates_service import (
    IconTemplatesService,
    IconTemplateError,
    CategoryNotFoundError,
)


def get_service() -> IconTemplatesService:
    """Create a service with default data directory."""
    return IconTemplatesService()


def list_icons(
    category: Optional[str] = typer.Option(
        None,
        "--category",
        "-c",
        help="Filter by category"
    )
) -> None:
    """List available icon templates."""
    service = get_service()

    try:
        if category:
            # List icons in specific category
            icons = service.list(category)
            typer.echo(f"\nIcons in '{category}':\n")
            if not icons:
                typer.echo("No icons in this category")
                return
            for icon_name in icons:
                typer.echo(f"  • {icon_name}")
            typer.echo(f"\nTotal: {len(icons)} icon(s)")
        else:
            # List categories
            categories = service.categories()
            typer.echo("\nAvailable icon categories:\n")
            if not categories:
                typer.echo("No categories found")
                return
            
            total_icons = 0
            for cat in categories:
                icons = service.list(cat)
                icon_count = len(icons)
                total_icons += icon_count
                typer.echo(f"  • {cat:<20} ({icon_count} icons)")
            
            typer.echo(f"\nTotal: {len(categories)} categories, {total_icons} icons")

    except CategoryNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except IconTemplateError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
