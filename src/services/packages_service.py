# src/services/packages_service.py
"""Service layer for package management."""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


class PackagesError(Exception):
    """Base exception for package operations."""


class PlaybookNotFoundError(PackagesError):
    """Raised when playbook file doesn't exist."""


class AnsibleError(PackagesError):
    """Raised when Ansible command fails."""

    def __init__(self, message: str, return_code: int = 1):
        """Initialize AnsibleError with message and return code."""
        super().__init__(message)
        self.return_code = return_code


class AnsibleNotFoundError(PackagesError):
    """Raised when Ansible is not installed."""


@dataclass
class PackageRole:
    """Represents a package role from the playbook."""

    name: str
    tags: List[str]


class PackagesService:
    """Service for managing system packages via Ansible."""

    def __init__(
        self,
        playbook_path: Optional[Path] = None,
        ansible_dir: Optional[Path] = None,
    ):
        """Initialize PackagesService.

        Args:
            playbook_path: Path to Ansible playbook (defaults to packages/ansible/playbooks/bootstrap.yml)
            ansible_dir: Path to ansible directory (defaults to packages/ansible)
        """
        if playbook_path is None:
            project_root = Path.cwd()
            playbook_path = project_root / "packages" / "ansible" / "playbooks" / "bootstrap.yml"

        if ansible_dir is None:
            ansible_dir = playbook_path.parent.parent

        self.playbook_path = playbook_path
        self.ansible_dir = ansible_dir

    def list_packages(self) -> List[PackageRole]:
        """List available package roles with their tags.

        Returns:
            List of PackageRole objects with name and tags

        Raises:
            PlaybookNotFoundError: If playbook file doesn't exist
        """
        if not self.playbook_path.exists():
            raise PlaybookNotFoundError(f"Playbook not found at {self.playbook_path}")

        with open(self.playbook_path, "r") as f:
            playbook_data = yaml.safe_load(f)

        roles = []
        if playbook_data:
            for play in playbook_data:
                if "roles" in play:
                    for role_entry in play["roles"]:
                        if isinstance(role_entry, dict):
                            role_name = role_entry.get("role", "unknown")
                            role_tags = role_entry.get("tags", [])
                        elif isinstance(role_entry, str):
                            role_name = role_entry
                            role_tags = []
                        else:
                            continue

                        roles.append(PackageRole(name=role_name, tags=role_tags))

        return roles

    def install(
        self,
        tags: Optional[List[str]] = None,
        extra_args: Optional[List[str]] = None,
    ) -> subprocess.CompletedProcess:
        """Install packages using Ansible playbook.

        Args:
            tags: List of Ansible tags to run
            extra_args: Additional arguments to pass to ansible-playbook

        Returns:
            CompletedProcess from subprocess.run

        Raises:
            AnsibleNotFoundError: If ansible-playbook command is not found
            AnsibleError: If ansible-playbook execution fails
        """
        cmd = ["ansible-playbook", str(self.playbook_path)]

        if tags:
            cmd.extend(["--tags", ",".join(tags)])

        if extra_args:
            cmd.extend(extra_args)

        try:
            result = subprocess.run(
                cmd,
                cwd=self.ansible_dir,
                check=True,
            )
            return result
        except FileNotFoundError as e:
            raise AnsibleNotFoundError(
                "ansible-playbook command not found. Please install Ansible."
            ) from e
        except subprocess.CalledProcessError as e:
            raise AnsibleError(f"Error running ansible-playbook: {e}", return_code=e.returncode) from e
