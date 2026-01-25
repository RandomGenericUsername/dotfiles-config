# dotfiles-icon-templates/src/dotfiles_icon_templates/cli/commands/__init__.py
"""CLI commands for dotfiles-icon-templates."""
from dotfiles_icon_templates.cli.commands.list import list_icons
from dotfiles_icon_templates.cli.commands.copy import copy_icons
from dotfiles_icon_templates.cli.commands.show import show_icon

__all__ = ["list_icons", "copy_icons", "show_icon"]
