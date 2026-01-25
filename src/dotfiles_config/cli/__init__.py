# src/dotfiles_config/cli/__init__.py
"""Root CLI for dotfiles-config."""
import typer

from dotfiles_packages.cli import app as packages_app
from dotfiles_wallpapers.cli import app as wallpapers_app
from dotfiles_icon_templates.cli import app as icon_templates_app

app = typer.Typer(help="Dotfiles configuration management")

# Add subcommands
app.add_typer(packages_app, name="packages", help="Manage system packages")
app.add_typer(wallpapers_app, name="wallpapers", help="Manage wallpaper assets")
app.add_typer(icon_templates_app, name="icon-templates", help="Manage icon templates")

__all__ = ["app"]
