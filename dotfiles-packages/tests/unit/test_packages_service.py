# tests/unit/test_packages_service.py
"""Unit tests for PackagesService."""
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from dotfiles_packages.services.packages_service import (
    PackagesService,
    PackageRole,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
)


class TestPackageRole:
    """Tests for PackageRole dataclass."""

    def test_package_role_creation(self):
        """Test creating a PackageRole."""
        role = PackageRole(name="nvim", tags=["nvim", "editor"])
        assert role.name == "nvim"
        assert role.tags == ["nvim", "editor"]

    def test_package_role_empty_tags(self):
        """Test PackageRole with empty tags."""
        role = PackageRole(name="base", tags=[])
        assert role.name == "base"
        assert role.tags == []


class TestPackagesServiceInit:
    """Tests for PackagesService initialization."""

    def test_init_with_defaults(self):
        """Test initialization with default paths."""
        service = PackagesService()
        assert service.playbook_path.name == "bootstrap.yml"
        assert service.ansible_dir.name == "ansible"

    def test_init_with_custom_paths(self):
        """Test initialization with custom paths."""
        custom_playbook = Path("/custom/playbook.yml")
        custom_ansible_dir = Path("/custom/ansible")
        
        service = PackagesService(
            playbook_path=custom_playbook,
            ansible_dir=custom_ansible_dir
        )
        
        assert service.playbook_path == custom_playbook
        assert service.ansible_dir == custom_ansible_dir


class TestPackagesServiceListPackages:
    """Tests for list_packages method."""

    def test_list_packages_not_found(self, tmp_path):
        """Test list_packages when playbook doesn't exist."""
        playbook = tmp_path / "nonexistent.yml"
        service = PackagesService(playbook_path=playbook)
        
        with pytest.raises(PlaybookNotFoundError):
            service.list_packages()

    def test_list_packages_empty(self, tmp_path):
        """Test list_packages with empty playbook."""
        playbook = tmp_path / "empty.yml"
        playbook.write_text("")
        
        service = PackagesService(playbook_path=playbook)
        roles = service.list_packages()
        
        assert roles == []

    def test_list_packages_single_role(self, tmp_path):
        """Test list_packages with single role."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("""
- hosts: localhost
  roles:
    - role: nvim
      tags:
        - nvim
        - editor
""")
        
        service = PackagesService(playbook_path=playbook)
        roles = service.list_packages()
        
        assert len(roles) == 1
        assert roles[0].name == "nvim"
        assert roles[0].tags == ["nvim", "editor"]

    def test_list_packages_multiple_roles(self, tmp_path):
        """Test list_packages with multiple roles."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("""
- hosts: localhost
  roles:
    - role: nvim
      tags:
        - nvim
    - role: zsh
      tags:
        - zsh
        - shell
    - base
""")
        
        service = PackagesService(playbook_path=playbook)
        roles = service.list_packages()
        
        assert len(roles) == 3
        assert roles[0].name == "nvim"
        assert roles[1].name == "zsh"
        assert roles[2].name == "base"
        assert roles[2].tags == []

    def test_list_packages_no_roles(self, tmp_path):
        """Test list_packages when playbook has no roles."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("""
- hosts: localhost
  vars:
    some_var: value
""")
        
        service = PackagesService(playbook_path=playbook)
        roles = service.list_packages()
        
        assert roles == []


class TestPackagesServiceInstall:
    """Tests for install method."""

    def test_install_success(self, tmp_path):
        """Test successful installation."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            result = service.install()
            
            assert result == mock_result
            mock_run.assert_called_once()

    def test_install_with_tags(self, tmp_path):
        """Test install with tags."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            service.install(tags=["nvim", "zsh"])
            
            call_args = mock_run.call_args
            cmd = call_args[0][0]
            assert "--tags" in cmd
            assert "nvim,zsh" in cmd

    def test_install_with_extra_args(self, tmp_path):
        """Test install with extra arguments."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        with patch('subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result
            
            service.install(extra_args=["--check", "--ask-become-pass"])
            
            call_args = mock_run.call_args
            cmd = call_args[0][0]
            assert "--check" in cmd
            assert "--ask-become-pass" in cmd

    def test_install_ansible_not_found(self, tmp_path):
        """Test install when ansible-playbook is not found."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        with patch('subprocess.run', side_effect=FileNotFoundError()):
            with pytest.raises(AnsibleNotFoundError):
                service.install()

    def test_install_ansible_fails(self, tmp_path):
        """Test install when ansible-playbook fails."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        error = subprocess.CalledProcessError(1, "ansible-playbook")
        with patch('subprocess.run', side_effect=error):
            with pytest.raises(AnsibleError):
                service.install()

    def test_install_ansible_error_has_return_code(self, tmp_path):
        """Test AnsibleError contains return code."""
        playbook = tmp_path / "playbook.yml"
        playbook.write_text("- hosts: localhost\n  roles: []")
        
        service = PackagesService(playbook_path=playbook)
        
        error = subprocess.CalledProcessError(42, "ansible-playbook")
        with patch('subprocess.run', side_effect=error):
            with pytest.raises(AnsibleError) as exc_info:
                service.install()
            
            assert exc_info.value.return_code == 42
