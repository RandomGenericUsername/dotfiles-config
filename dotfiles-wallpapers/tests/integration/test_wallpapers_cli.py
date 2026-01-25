# tests/integration/test_wallpapers_cli.py
"""Integration tests for Wallpapers CLI."""
import tarfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from dotfiles_wallpapers.cli import app


runner = CliRunner()


class TestWallpapersListCommand:
    """Tests for wallpapers list command."""

    def test_list_command_success(self):
        """Test list command with wallpapers."""
        with patch('dotfiles_wallpapers.cli.commands.list.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.list_wallpapers.return_value = ['bg1.jpg', 'bg2.png']
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 0
            assert "bg1.jpg" in result.stdout
            assert "bg2.png" in result.stdout
            assert "2" in result.stdout

    def test_list_command_empty(self):
        """Test list command with no wallpapers."""
        with patch('dotfiles_wallpapers.cli.commands.list.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.list_wallpapers.return_value = []
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 0
            assert "No wallpapers" in result.stdout

    def test_list_command_archive_not_found(self):
        """Test list command when archive doesn't exist."""
        with patch('dotfiles_wallpapers.cli.commands.list.WallpapersService') as mock_service_class:
            from dotfiles_wallpapers.services.wallpapers_service import ArchiveNotFoundError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.list_wallpapers.side_effect = ArchiveNotFoundError("Not found")
            
            result = runner.invoke(app, ["list"])
            
            assert result.exit_code == 1


class TestWallpapersAddCommand:
    """Tests for wallpapers add command."""

    def test_add_command_success(self, tmp_path):
        """Test add command success."""
        source = tmp_path / "test.jpg"
        source.write_text("image")
        
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            result = runner.invoke(app, ["add", str(source)])
            
            assert result.exit_code == 0
            assert "Successfully added" in result.stdout
            assert "test.jpg" in result.stdout

    def test_add_command_with_force(self, tmp_path):
        """Test add command with force flag."""
        source = tmp_path / "test.jpg"
        source.write_text("image")
        
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            result = runner.invoke(app, ["add", str(source), "--force"])
            
            assert result.exit_code == 0
            mock_service.add_wallpaper.assert_called_once()

    def test_add_command_with_no_validate(self, tmp_path):
        """Test add command with no-validate flag."""
        source = tmp_path / "custom.xyz"
        source.write_text("image")
        
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            result = runner.invoke(app, ["add", str(source), "--no-validate"])
            
            assert result.exit_code == 0

    def test_add_command_file_not_found(self):
        """Test add command with non-existent file."""
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            from dotfiles_wallpapers.services.wallpapers_service import WallpaperNotFoundError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.add_wallpaper.side_effect = WallpaperNotFoundError("Not found")
            
            # Use a fake path that will pass the typer exists check
            result = runner.invoke(app, ["add", "/nonexistent/file.jpg"], catch_exceptions=False)

    def test_add_command_invalid_extension(self, tmp_path):
        """Test add command with invalid extension."""
        source = tmp_path / "document.txt"
        source.write_text("content")
        
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            from dotfiles_wallpapers.services.wallpapers_service import InvalidImageError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.add_wallpaper.side_effect = InvalidImageError("Invalid extension")
            
            result = runner.invoke(app, ["add", str(source)])
            
            assert result.exit_code == 1

    def test_add_command_duplicate_error(self, tmp_path):
        """Test add command with duplicate wallpaper."""
        source = tmp_path / "test.jpg"
        source.write_text("image")
        
        with patch('dotfiles_wallpapers.cli.commands.add.WallpapersService') as mock_service_class:
            from dotfiles_wallpapers.services.wallpapers_service import WallpaperError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.add_wallpaper.side_effect = WallpaperError("Already exists")
            
            result = runner.invoke(app, ["add", str(source)])
            
            assert result.exit_code == 1


class TestWallpapersExtractCommand:
    """Tests for wallpapers extract command."""

    def test_extract_command_success(self, tmp_path):
        """Test extract command success."""
        output_dir = tmp_path / "output"
        
        with patch('dotfiles_wallpapers.cli.commands.extract.WallpapersService') as mock_service_class:
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            
            result_path = output_dir / "wallpapers"
            mock_service.extract_wallpapers.return_value = result_path
            
            result = runner.invoke(app, ["extract", str(output_dir)])
            
            assert result.exit_code == 0
            assert "Extracted" in result.stdout

    def test_extract_command_archive_not_found(self):
        """Test extract command when archive doesn't exist."""
        with patch('dotfiles_wallpapers.cli.commands.extract.WallpapersService') as mock_service_class:
            from dotfiles_wallpapers.services.wallpapers_service import ArchiveNotFoundError
            mock_service = MagicMock()
            mock_service_class.return_value = mock_service
            mock_service.extract_wallpapers.side_effect = ArchiveNotFoundError("Not found")
            
            result = runner.invoke(app, ["extract", "/tmp/output"])
            
            assert result.exit_code == 1
