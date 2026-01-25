# tests/unit/test_wallpapers_api.py
"""Unit tests for Wallpapers API."""
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from dotfiles_wallpapers.api.wallpapers import Wallpapers


class TestWallpapersAPI:
    """Tests for Wallpapers API class."""

    def test_wallpapers_initialization_default(self):
        """Test Wallpapers initialization with defaults."""
        wallpapers = Wallpapers()
        assert wallpapers._service is not None

    def test_wallpapers_initialization_custom(self, tmp_path):
        """Test Wallpapers initialization with custom path."""
        archive = tmp_path / "custom.tar.gz"
        wallpapers = Wallpapers(archive_path=archive)
        assert wallpapers._service.archive_path == archive

    def test_list_delegates_to_service(self):
        """Test list method delegates to service."""
        wallpapers = Wallpapers()
        
        with patch.object(wallpapers._service, 'list_wallpapers', return_value=['bg1.jpg', 'bg2.png']):
            result = wallpapers.list()
            
            assert result == ['bg1.jpg', 'bg2.png']

    def test_add_delegates_to_service(self, tmp_path):
        """Test add method delegates to service."""
        wallpapers = Wallpapers()
        source = tmp_path / "test.jpg"
        source.write_text("image")
        
        with patch.object(wallpapers._service, 'add_wallpaper') as mock_add:
            wallpapers.add(source, force=True, validate=False)
            
            mock_add.assert_called_once()
            call_kwargs = mock_add.call_args[1]
            assert call_kwargs['overwrite'] is True
            assert call_kwargs['validate_extension'] is False

    def test_extract_delegates_to_service(self, tmp_path):
        """Test extract method delegates to service."""
        wallpapers = Wallpapers()
        output = tmp_path / "output"
        
        mock_result = tmp_path / "result"
        with patch.object(wallpapers._service, 'extract_wallpapers', return_value=mock_result):
            result = wallpapers.extract(output)
            
            assert result == mock_result

    def test_add_with_defaults(self, tmp_path):
        """Test add with default parameters."""
        wallpapers = Wallpapers()
        source = tmp_path / "test.jpg"
        source.write_text("image")
        
        with patch.object(wallpapers._service, 'add_wallpaper') as mock_add:
            wallpapers.add(source)
            
            call_kwargs = mock_add.call_args[1]
            assert call_kwargs['overwrite'] is False
            assert call_kwargs['validate_extension'] is True
