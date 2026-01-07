# src/commands/assets/__init__.py
"""Assets command group."""
from typer import Typer

from src.commands.assets.wallpapers import wallpapers_app

assets_app = Typer(help="Manage dotfiles assets")
assets_app.add_typer(wallpapers_app, name="wallpapers")
