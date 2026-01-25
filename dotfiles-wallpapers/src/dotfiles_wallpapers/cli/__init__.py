# dotfiles-wallpapers/src/dotfiles_wallpapers/cli/__init__.py
"""CLI for dotfiles-wallpapers."""
import typer

from dotfiles_wallpapers.cli.commands.list import list_wallpapers
from dotfiles_wallpapers.cli.commands.add import add_wallpaper
from dotfiles_wallpapers.cli.commands.extract import extract_wallpapers

app = typer.Typer(help="Manage wallpaper assets")

app.command("list")(list_wallpapers)
app.command("add")(add_wallpaper)
app.command("extract")(extract_wallpapers)

__all__ = ["app"]
