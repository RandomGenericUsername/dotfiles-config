# dotfiles-wallpapers/src/dotfiles_wallpapers/cli/commands/add.py
"""Add command for wallpapers CLI."""
from pathlib import Path

import typer

from dotfiles_wallpapers.constants import PACKAGE_ROOT
from dotfiles_wallpapers.services.wallpapers_service import (
    WallpapersService,
    WallpaperError,
)


def get_default_archive_path() -> Path:
    """Get the default archive path."""
    return PACKAGE_ROOT / "wallpapers.tar.gz"


def add_wallpaper(
    path: Path = typer.Argument(
        ...,
        help="Path to the wallpaper image to add",
        exists=True,
        readable=True,
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite if wallpaper with same name exists",
    ),
    no_validate: bool = typer.Option(
        False,
        "--no-validate",
        help="Skip image extension validation",
    ),
) -> None:
    """Add a wallpaper to the archive."""
    service = WallpapersService(get_default_archive_path())
    try:
        service.add_wallpaper(
            path,
            overwrite=force,
            validate_extension=not no_validate,
        )
        typer.echo(f"Successfully added '{path.name}' to wallpapers archive")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
