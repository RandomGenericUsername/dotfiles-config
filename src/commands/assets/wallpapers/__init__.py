# src/commands/assets/wallpapers/__init__.py
"""Wallpapers subcommand group."""
from pathlib import Path

import typer

from src.services.wallpapers_service import (
    WallpapersService,
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
)

wallpapers_app = typer.Typer(help="Manage wallpaper assets")


def get_default_archive_path() -> Path:
    """Get the default archive path relative to this package."""
    package_dir = Path(__file__).parent
    # Navigate up to config root, then to assets/wallpapers
    config_root = package_dir.parent.parent.parent.parent
    return config_root / "assets" / "wallpapers" / "wallpapers.tar.gz"


def get_service() -> WallpapersService:
    """Create a WallpapersService with the default archive path."""
    return WallpapersService(get_default_archive_path())


@wallpapers_app.command("add")
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
    service = get_service()
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


@wallpapers_app.command("extract")
def extract_wallpapers(
    path: Path = typer.Argument(
        ...,
        help="Directory where wallpapers will be extracted (creates 'wallpapers' subdirectory)",
    ),
) -> None:
    """Extract all wallpapers to the specified directory."""
    service = get_service()
    try:
        result_path = service.extract_wallpapers(path)
        wallpapers = list(result_path.iterdir())
        typer.echo(f"Extracted {len(wallpapers)} wallpaper(s) to {result_path}")
    except ArchiveNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@wallpapers_app.command("list")
def list_wallpapers() -> None:
    """List all wallpapers in the archive."""
    service = get_service()
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
