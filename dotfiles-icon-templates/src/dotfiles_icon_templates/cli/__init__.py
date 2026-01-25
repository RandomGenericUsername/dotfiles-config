# dotfiles-icon-templates/src/dotfiles_icon_templates/cli/__init__.py
"""CLI for dotfiles-icon-templates."""
import typer

from dotfiles_icon_templates.cli.commands.list import list_icons
from dotfiles_icon_templates.cli.commands.copy import copy_icons
from dotfiles_icon_templates.cli.commands.show import show_icon

app = typer.Typer(help="Manage icon templates")

app.command("list")(list_icons)
app.command("copy")(copy_icons)
app.command("show")(show_icon)

__all__ = ["app"]
