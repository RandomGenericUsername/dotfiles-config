# dotfiles-icon-templates/src/dotfiles_icon_templates/cli/commands/show.py
"""Show command for icon templates CLI."""
import typer

from dotfiles_icon_templates.services.icon_templates_service import (
    IconTemplatesService,
    IconTemplateError,
    IconNotFoundError,
)


def get_service() -> IconTemplatesService:
    """Create a service with default data directory."""
    return IconTemplatesService()


def show_icon(
    name: str = typer.Argument(
        ...,
        help="Icon name to show details for"
    )
) -> None:
    """Show details about an icon template."""
    service = get_service()

    try:
        icon_info = service.show(name)

        typer.echo(f"\nIcon: {icon_info.name}\n")
        typer.echo(f"  Category:  {icon_info.category}")
        typer.echo(f"  Path:      {icon_info.path}")
        
        if icon_info.variants:
            variants_str = ", ".join(icon_info.variants)
            typer.echo(f"  Variants:  {variants_str}")
        
        typer.echo()

    except IconNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except IconTemplateError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
