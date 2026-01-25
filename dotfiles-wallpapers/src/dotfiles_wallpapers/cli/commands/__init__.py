# dotfiles-wallpapers/src/dotfiles_wallpapers/cli/commands/__init__.py
"""CLI commands for dotfiles-wallpapers."""
from dotfiles_wallpapers.cli.commands.list import list_wallpapers
from dotfiles_wallpapers.cli.commands.add import add_wallpaper
from dotfiles_wallpapers.cli.commands.extract import extract_wallpapers

__all__ = ["list_wallpapers", "add_wallpaper", "extract_wallpapers"]
