# tests/unit/test_packages_api.py
"""Unit tests for Packages API."""
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from dotfiles_packages.api.packages import Packages
from dotfiles_packages.services.packages_service import PackageRole


class TestPackagesAPI:
    """Tests for Packages API class."""

    def test_packages_initialization(self):
        """Test Packages initialization."""
        packages = Packages()
        assert packages._service is not None

    def test_packages_initialization_custom_paths(self, tmp_path):
        """Test Packages initialization with custom paths."""
        playbook = tmp_path / "playbook.yml"
        ansible_dir = tmp_path / "ansible"
        
        packages = Packages(playbook_path=playbook, ansible_dir=ansible_dir)
        assert packages._service.playbook_path == playbook
        assert packages._service.ansible_dir == ansible_dir

    def test_list_delegates_to_service(self):
        """Test list method delegates to service."""
        packages = Packages()
        
        mock_role = PackageRole(name="nvim", tags=["nvim"])
        
        with patch.object(packages._service, 'list_packages', return_value=[mock_role]):
            result = packages.list()
            
            assert result == [mock_role]
            assert result[0].name == "nvim"

    def test_install_delegates_to_service(self):
        """Test install method delegates to service."""
        packages = Packages()
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        
        with patch.object(packages._service, 'install', return_value=mock_result):
            result = packages.install(tags=["nvim"])
            
            assert result == mock_result

    def test_install_forwards_extra_args(self):
        """Test install forwards extra arguments."""
        packages = Packages()
        
        mock_result = MagicMock()
        
        with patch.object(packages._service, 'install', return_value=mock_result) as mock_install:
            packages.install(tags=["nvim"], extra_args=["--check"])
            
            mock_install.assert_called_once()
            call_kwargs = mock_install.call_args[1]
            assert call_kwargs['tags'] == ["nvim"]
            assert call_kwargs['extra_args'] == ["--check"]

    def test_list_empty_result(self):
        """Test list when service returns empty."""
        packages = Packages()
        
        with patch.object(packages._service, 'list_packages', return_value=[]):
            result = packages.list()
            
            assert result == []
