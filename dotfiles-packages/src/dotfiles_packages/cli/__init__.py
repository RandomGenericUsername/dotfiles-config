# dotfiles-packages/src/dotfiles_packages/cli/__init__.py
"""CLI for dotfiles-packages."""
import typer

from dotfiles_packages.cli.commands.list import list_packages
from dotfiles_packages.cli.commands.install import install

app = typer.Typer(help="Manage system packages")

app.command("list")(list_packages)
app.command("install", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(install)

__all__ = ["app"]
