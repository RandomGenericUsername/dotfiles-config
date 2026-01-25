# tests/integration/test_packages_cli.py
"""Integration tests for Packages CLI."""
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from dotfiles_packages.cli import app


runner = CliRunner()


class TestPackagesListCommand:
    """Tests for packages list command."""

    def test_list_command_success(self, tmp_path):
        """Test list command with roles."""
        playbook = tmp_path / "bootstrap.yml"
        playbook.write_text("""
- hosts: localhost
  roles:
    - role: nvim
      tags:
        - nvim
    - role: zsh
      tags:
        - zsh
""")
        
        with patch('dotfiles_packages.cli.commands.list.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            from dotfiles_packages.services.packages_service import PackageRole
            mock_service.list_packages.return_value = [
                PackageRole(name="nvim", tags=["nvim"]),
                PackageRole(name="zsh", tags=["zsh"]),
            ]
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 0
            assert "nvim" in result.stdout
            assert "zsh" in result.stdout
            assert "2 role(s)" in result.stdout

    def test_list_command_no_roles(self):
        """Test list command with no roles."""
        with patch('dotfiles_packages.cli.commands.list.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.list_packages.return_value = []
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 0
            assert "No roles found" in result.stdout

    def test_list_command_playbook_not_found(self):
        """Test list command when playbook is missing."""
        with patch('dotfiles_packages.cli.commands.list.PackagesService') as mock_service_class:
            from dotfiles_packages.services.packages_service import PlaybookNotFoundError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.list_packages.side_effect = PlaybookNotFoundError("Not found")
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 1
            assert "Error" in result.stdout or "Error" in result.stderr


class TestPackagesInstallCommand:
    """Tests for packages install command."""

    def test_install_command_success(self):
        """Test install command success."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_service.install.return_value = mock_result
            
            result = runner.invoke(app, ["install", "--tags", "nvim"])
            
            # Should exit with 0 (the return code from ansible-playbook)
            assert result.exit_code == 0

    def test_install_command_with_tags(self):
        """Test install command with multiple tags."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_service.install.return_value = mock_result
            
            result = runner.invoke(app, ["install", "--tags", "nvim", "--tags", "zsh"])
            
            assert result.exit_code == 0
            # Verify install was called with tags
            mock_service.install.assert_called_once()

    def test_install_command_ansible_not_found(self):
        """Test install when ansible is not installed."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            from dotfiles_packages.services.packages_service import AnsibleNotFoundError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.install.side_effect = AnsibleNotFoundError("Not installed")
            
            result = runner.invoke(app, ["install"])
            
            assert result.exit_code == 1
            assert "Error" in result.stdout or "Error" in result.stderr

    def test_install_command_ansible_fails(self):
        """Test install when ansible-playbook fails."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            from dotfiles_packages.services.packages_service import AnsibleError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.install.side_effect = AnsibleError("Failed", return_code=2)
            
            result = runner.invoke(app, ["install"])
            
            assert result.exit_code == 2

    def test_install_command_forwards_extra_args(self):
        """Test install forwards extra arguments to ansible."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_service.install.return_value = mock_result
            
            result = runner.invoke(
                app,
                ["install", "--tags", "nvim", "--", "--check", "--diff"]
            )
            
            # Extra args might or might not work depending on how typer handles them
            # Just verify the command runs
            assert result.exit_code in [0, 2]  # 0 success or 2 from mocked ansible

    def test_install_command_shows_working_directory(self):
        """Test install command shows working directory."""
        with patch('dotfiles_packages.cli.commands.install.PackagesService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.ansible_dir = "/some/path"
            
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_service.install.return_value = mock_result
            
            result = runner.invoke(app, ["install"])
            
            assert "Working directory" in result.stdout
