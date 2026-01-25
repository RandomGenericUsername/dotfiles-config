# dotfiles-wallpapers/src/dotfiles_wallpapers/cli/commands/list.py
"""List command for wallpapers CLI."""
from pathlib import Path

import typer

from dotfiles_wallpapers.constants import PACKAGE_ROOT
from dotfiles_wallpapers.services.wallpapers_service import (
    WallpapersService,
    ArchiveNotFoundError,
)


def get_default_archive_path() -> Path:
    """Get the default archive path."""
    return PACKAGE_ROOT / "wallpapers.tar.gz"


def list_wallpapers() -> None:
    """List all wallpapers in the archive."""
    service = WallpapersService(get_default_archive_path())
    try:
        wallpapers = service.list_wallpapers()
        if not wallpapers:
            typer.echo("No wallpapers in archive")
            return
        typer.echo(f"Wallpapers in archive ({len(wallpapers)}):")
        for name in sorted(wallpapers):
            typer.echo(f"  - {name}")
    except ArchiveNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
