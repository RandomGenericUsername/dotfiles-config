# dotfiles-packages/src/dotfiles_packages/cli/commands/install.py
"""Install command for packages CLI."""
import sys
from typing import List, Optional

import typer

from dotfiles_packages.services.packages_service import (
    PackagesService,
    PackagesError,
    AnsibleNotFoundError,
    AnsibleError,
)


def install(
    ctx: typer.Context,
    tags: Optional[List[str]] = typer.Option(None, "--tags", help="Ansible tags to run"),
):
    """Install packages using Ansible playbook.

    All parameters are forwarded to ansible-playbook command.
    """
    service = PackagesService()

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
