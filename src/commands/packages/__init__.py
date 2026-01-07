# src/commands/packages/__init__.py
"""Packages command group."""
import sys
from typing import List, Optional

import typer

from src.services.packages_service import (
    PackagesService,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleNotFoundError,
    AnsibleError,
)

packages_app = typer.Typer(help="Manage system packages")


def get_service() -> PackagesService:
    """Create and return a PackagesService instance."""
    return PackagesService()


@packages_app.command("install", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def install(
    ctx: typer.Context,
    tags: Optional[List[str]] = typer.Option(None, "--tags", help="Ansible tags to run"),
):
    """
    Install packages using Ansible playbook.

    All parameters are forwarded to ansible-playbook command.
    """
    service = get_service()

    try:
        typer.echo(f"Running: ansible-playbook {' '.join([f'--tags {t}' for t in (tags or [])])} {' '.join(ctx.args or [])}")
        typer.echo(f"Working directory: {service.ansible_dir}")
        result = service.install(tags=tags, extra_args=ctx.args if ctx.args else None)
        sys.exit(result.returncode)
    except AnsibleNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except AnsibleError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(e.return_code)
    except PackagesError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)


@packages_app.command("list")
def list_packages():
    """
    List available packages (roles) and their tags from the Ansible playbook.
    """
    service = get_service()

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
        typer.echo("\nUsage: config packages install --tags <tag1,tag2>")

    except PlaybookNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except PackagesError as e:
        typer.echo(f"Error: {e}", err=True)
        sys.exit(1)
