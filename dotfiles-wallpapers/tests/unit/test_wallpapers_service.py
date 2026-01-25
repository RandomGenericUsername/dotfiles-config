# tests/unit/test_wallpapers_service.py
"""Unit tests for WallpapersService."""
import tarfile
from pathlib import Path

import pytest

from dotfiles_wallpapers.services.wallpapers_service import (
    WallpapersService,
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
)


class TestWallpapersServiceInit:
    """Tests for WallpapersService initialization."""

    def test_init_with_custom_path(self, tmp_path):
        """Test initialization with custom archive path."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        assert service.archive_path == archive_path


class TestIsValidImageExtension:
    """Tests for is_valid_image_extension class method."""

    def test_valid_extensions(self):
        """Test valid image extensions."""
        valid = ["image.jpg", "image.jpeg", "image.png", "image.gif", "image.bmp", "image.webp", "image.tiff", "image.tif"]
        for filename in valid:
            assert WallpapersService.is_valid_image_extension(filename)

    def test_invalid_extensions(self):
        """Test invalid extensions."""
        invalid = ["image.txt", "image.pdf", "image.doc", "image.svg", "noextension"]
        for filename in invalid:
            assert not WallpapersService.is_valid_image_extension(filename)

    def test_case_insensitive(self):
        """Test extension matching is case insensitive."""
        assert WallpapersService.is_valid_image_extension("image.JPG")
        assert WallpapersService.is_valid_image_extension("image.PnG")


class TestWallpapersServiceListWallpapers:
    """Tests for list_wallpapers method."""

    def test_list_archive_not_found(self, tmp_path):
        """Test list_wallpapers when archive doesn't exist."""
        archive_path = tmp_path / "nonexistent.tar.gz"
        service = WallpapersService(archive_path)
        
        with pytest.raises(ArchiveNotFoundError):
            service.list_wallpapers()

    def test_list_empty_archive(self, tmp_path):
        """Test list_wallpapers with empty archive."""
        archive_path = tmp_path / "empty.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            pass
        
        service = WallpapersService(archive_path)
        wallpapers = service.list_wallpapers()
        
        assert wallpapers == []

    def test_list_with_files(self, tmp_path):
        """Test list_wallpapers with files."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        
        # Create archive with test files
        with tarfile.open(archive_path, "w:gz") as tar:
            for filename in ["bg1.jpg", "bg2.png", "bg3.jpg"]:
                file_path = tmp_path / filename
                file_path.write_text("dummy")
                tar.add(file_path, arcname=filename)
        
        service = WallpapersService(archive_path)
        wallpapers = service.list_wallpapers()
        
        assert len(wallpapers) == 3
        assert "bg1.jpg" in wallpapers
        assert "bg2.png" in wallpapers
        assert "bg3.jpg" in wallpapers

    def test_list_excludes_hidden_files(self, tmp_path):
        """Test list_wallpapers excludes hidden files."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        
        with tarfile.open(archive_path, "w:gz") as tar:
            for filename in ["bg1.jpg", ".hidden.jpg"]:
                file_path = tmp_path / filename
                file_path.write_text("dummy")
                tar.add(file_path, arcname=filename)
        
        service = WallpapersService(archive_path)
        wallpapers = service.list_wallpapers()
        
        assert len(wallpapers) == 1
        assert wallpapers[0] == "bg1.jpg"


class TestWallpapersServiceAddWallpaper:
    """Tests for add_wallpaper method."""

    def test_add_wallpaper_file_not_found(self, tmp_path):
        """Test add_wallpaper with non-existent source file."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        nonexistent = tmp_path / "nonexistent.jpg"
        with pytest.raises(WallpaperNotFoundError):
            service.add_wallpaper(nonexistent)

    def test_add_wallpaper_invalid_extension(self, tmp_path):
        """Test add_wallpaper with invalid extension."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        invalid_file = tmp_path / "document.txt"
        invalid_file.write_text("content")
        
        with pytest.raises(InvalidImageError):
            service.add_wallpaper(invalid_file)

    def test_add_wallpaper_skip_validation(self, tmp_path):
        """Test add_wallpaper with validation disabled."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        invalid_file = tmp_path / "custom.xyz"
        invalid_file.write_text("content")
        
        # Should not raise with validate_extension=False
        service.add_wallpaper(invalid_file, validate_extension=False)
        assert archive_path.exists()

    def test_add_wallpaper_creates_archive(self, tmp_path):
        """Test add_wallpaper creates archive if it doesn't exist."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        source_file = tmp_path / "test.jpg"
        source_file.write_text("image")
        
        assert not archive_path.exists()
        service.add_wallpaper(source_file)
        assert archive_path.exists()

    def test_add_wallpaper_duplicate_without_force(self, tmp_path):
        """Test add_wallpaper rejects duplicate without force."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        source_file = tmp_path / "test.jpg"
        source_file.write_text("image")
        
        service.add_wallpaper(source_file)
        
        # Try to add again without force
        with pytest.raises(WallpaperError) as exc:
            service.add_wallpaper(source_file, overwrite=False)
        
        assert "already exists" in str(exc.value)

    def test_add_wallpaper_duplicate_with_force(self, tmp_path):
        """Test add_wallpaper allows duplicate with force."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        service = WallpapersService(archive_path)
        
        source_file = tmp_path / "test.jpg"
        source_file.write_text("image1")
        
        service.add_wallpaper(source_file)
        
        # Modify source and add with force
        source_file.write_text("image2")
        service.add_wallpaper(source_file, overwrite=True)
        
        # Verify it was updated
        wallpapers = service.list_wallpapers()
        assert len(wallpapers) == 1


class TestWallpapersServiceExtractWallpapers:
    """Tests for extract_wallpapers method."""

    def test_extract_archive_not_found(self, tmp_path):
        """Test extract_wallpapers when archive doesn't exist."""
        archive_path = tmp_path / "nonexistent.tar.gz"
        service = WallpapersService(archive_path)
        
        with pytest.raises(ArchiveNotFoundError):
            service.extract_wallpapers(tmp_path / "output")

    def test_extract_creates_subdirectory(self, tmp_path):
        """Test extract_wallpapers creates wallpapers subdirectory."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        
        # Create archive with a file
        with tarfile.open(archive_path, "w:gz") as tar:
            file_path = tmp_path / "test.jpg"
            file_path.write_text("image")
            tar.add(file_path, arcname="test.jpg")
        
        service = WallpapersService(archive_path)
        output_dir = tmp_path / "output"
        
        result = service.extract_wallpapers(output_dir)
        
        assert result == output_dir / "wallpapers"
        assert (output_dir / "wallpapers" / "test.jpg").exists()

    def test_extract_creates_output_directory(self, tmp_path):
        """Test extract_wallpapers creates output directory."""
        archive_path = tmp_path / "wallpapers.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            pass
        
        service = WallpapersService(archive_path)
        output_dir = tmp_path / "nonexistent" / "nested"
        
        service.extract_wallpapers(output_dir)
        
        assert (output_dir / "wallpapers").exists()
