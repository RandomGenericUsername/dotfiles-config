# dotfiles-wallpapers/src/dotfiles_wallpapers/cli/commands/extract.py
"""Extract command for wallpapers CLI."""
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


def extract_wallpapers(
    path: Path = typer.Argument(
        ...,
        help="Directory where wallpapers will be extracted (creates 'wallpapers' subdirectory)",
    ),
) -> None:
    """Extract all wallpapers to the specified directory."""
    service = WallpapersService(get_default_archive_path())
    try:
        result_path = service.extract_wallpapers(path)
        wallpapers = list(result_path.iterdir())
        typer.echo(f"Extracted {len(wallpapers)} wallpaper(s) to {result_path}")
    except ArchiveNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
