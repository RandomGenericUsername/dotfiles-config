# dotfiles-packages/src/dotfiles_packages/cli/commands/list.py
"""List command for packages CLI."""
import sys
from typing import List

import typer

from dotfiles_packages.services.packages_service import (
    PackagesService,
    PackagesError,
    PlaybookNotFoundError,
)


def list_packages():
    """List available packages (roles) and their tags from the Ansible playbook."""
    service = PackagesService()

    try:
        roles = service.list_packages()

        if not roles:
            typer.echo("No roles found in the playbook.")
            return

        typer.echo("\nAvailable packages (roles):\n")
        for role in roles:
            tags_str = f"[{', '.join(role.tags)}]" if role.tags else "[no tags]"
            typer.echo(f"  • {role.name:<20} {tags_str}")

        typer.echo(f"\nTotal: {len(roles)} role(s)")
        typer.echo("\nUsage: dotfiles-packages install --tags <tag1,tag2>")

    except PlaybookNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except PackagesError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
