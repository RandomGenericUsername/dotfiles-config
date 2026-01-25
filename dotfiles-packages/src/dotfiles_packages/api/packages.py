# dotfiles-packages/src/dotfiles_packages/api/packages.py
"""Python API for package management."""
import subprocess
from pathlib import Path
from typing import List, Optional

from dotfiles_packages.services.packages_service import PackagesService, PackageRole


class Packages:
    """Python API for package management.

    Example:
        packages = Packages()
        packages.list()
        packages.install(tags=["nvim"])
    """

    def __init__(
        self,
        playbook_path: Optional[Path] = None,
        ansible_dir: Optional[Path] = None,
    ) -> None:
        """Initialize Packages API.

        Args:
            playbook_path: Path to Ansible playbook
            ansible_dir: Path to ansible directory
        """
        self._service = PackagesService(playbook_path, ansible_dir)

    def list(self) -> List[PackageRole]:
        """List available packages and their tags.

        Returns:
            List of PackageRole objects with name and tags
        """
        return self._service.list_packages()

    def install(
        self,
        tags: Optional[List[str]] = None,
        extra_args: Optional[List[str]] = None,
    ) -> subprocess.CompletedProcess:
        """Install packages using Ansible.

        Args:
            tags: List of tags to filter roles
            extra_args: Additional ansible-playbook arguments

        Returns:
            CompletedProcess from subprocess.run
        """
        return self._service.install(tags=tags, extra_args=extra_args)
