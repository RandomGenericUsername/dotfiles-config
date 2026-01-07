# tests/unit/test_wallpapers_service_comprehensive.py
"""Comprehensive tests for edge cases and documented behavior."""
import tarfile
from pathlib import Path

import pytest

from src.services.wallpapers_service import (
    WallpapersService,
)


class TestHiddenFilesAndDirectories:
    """Tests for hidden files and directory filtering."""

    def test_list_filters_hidden_files(self, temp_dir: Path) -> None:
        """List excludes files starting with dot (hidden files)."""
        archive_path = temp_dir / "test.tar.gz"

        # Create archive with hidden and normal files
        with tarfile.open(archive_path, "w:gz") as tar:
            # Add normal file
            normal = temp_dir / "visible.png"
            normal.write_bytes(b"content")
            tar.add(normal, arcname="visible.png")

            # Add hidden file
            hidden = temp_dir / ".hidden.png"
            hidden.write_bytes(b"content")
            tar.add(hidden, arcname=".hidden.png")

        service = WallpapersService(archive_path)
        wallpapers = service.list_wallpapers()

        assert "visible.png" in wallpapers
        assert ".hidden.png" not in wallpapers

    def test_list_filters_directories(self, temp_dir: Path) -> None:
        """List only returns files, not directories."""
        archive_path = temp_dir / "test.tar.gz"

        # Create archive with a directory and a file
        with tarfile.open(archive_path, "w:gz") as tar:
            # Add a file
            file_path = temp_dir / "image.png"
            file_path.write_bytes(b"content")
            tar.add(file_path, arcname="image.png")

            # Add directory info (common in tar archives)
            dir_info = tarfile.TarInfo(name="subdir/")
            dir_info.type = tarfile.DIRTYPE
            tar.addfile(dir_info)

        service = WallpapersService(archive_path)
        wallpapers = service.list_wallpapers()

        assert "image.png" in wallpapers
        assert "subdir/" not in wallpapers
        assert len(wallpapers) == 1


class TestMultipleImageFormats:
    """Tests for handling multiple image formats in the same archive."""

    def test_add_multiple_different_formats(
        self, temp_dir: Path, nonexistent_archive: Path
    ) -> None:
        """Add multiple wallpapers with different image formats."""
        service = WallpapersService(nonexistent_archive)

        # Create images with different extensions
        formats = ["jpg", "jpeg", "png", "gif", "webp", "bmp"]
        for fmt in formats:
            image = temp_dir / f"wallpaper.{fmt}"
            image.write_bytes(b"content")
            service.add_wallpaper(image)

        wallpapers = service.list_wallpapers()
        assert len(wallpapers) == len(formats)
        for fmt in formats:
            assert f"wallpaper.{fmt}" in wallpapers


class TestArchivePreservation:
    """Tests to ensure existing wallpapers aren't lost during operations."""

    def test_add_preserves_existing_wallpapers(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Adding a new wallpaper preserves all existing ones."""
        service = WallpapersService(sample_archive)

        # Get original wallpapers
        original_wallpapers = service.list_wallpapers()
        original_count = len(original_wallpapers)

        # Add new wallpaper
        new_image = temp_dir / "additional.png"
        new_image.write_bytes(b"new content")
        service.add_wallpaper(new_image)

        # Verify all original wallpapers still exist
        updated_wallpapers = service.list_wallpapers()
        assert len(updated_wallpapers) == original_count + 1
        for original in original_wallpapers:
            assert original in updated_wallpapers


class TestServiceDefaultBehavior:
    """Tests for service layer default parameter values."""

    def test_add_default_overwrites_duplicate(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add with default parameters (no args) overwrites duplicates."""
        # Create file with same name as existing wallpaper
        duplicate = temp_dir / "test_wallpaper.png"
        duplicate.write_bytes(b"different content")

        service = WallpapersService(sample_archive)

        # Should not raise because default overwrite=True
        service.add_wallpaper(duplicate)

        wallpapers = service.list_wallpapers()
        assert wallpapers.count("test_wallpaper.png") == 1

    def test_add_default_validates_extension(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add with default parameters validates file extension."""
        from src.services.wallpapers_service import InvalidImageError

        text_file = temp_dir / "not_an_image.txt"
        text_file.write_text("content")

        service = WallpapersService(sample_archive)

        # Should raise because default validate_extension=True
        with pytest.raises(InvalidImageError):
            service.add_wallpaper(text_file)


class TestValidationEdgeCases:
    """Tests for edge cases in filename validation."""

    def test_validates_multiple_dots_in_filename(self) -> None:
        """Validation handles filenames with multiple dots correctly."""
        # Should use the last extension
        assert WallpapersService.is_valid_image_extension("my.photo.final.png") is True
        assert WallpapersService.is_valid_image_extension("backup.v2.txt") is False

    def test_validates_mixed_case_extensions(self) -> None:
        """Validation is case-insensitive."""
        assert WallpapersService.is_valid_image_extension("image.PNG") is True
        assert WallpapersService.is_valid_image_extension("image.JpEg") is True
        assert WallpapersService.is_valid_image_extension("image.Gif") is True


class TestExtractBehavior:
    """Tests for extract operation behavior."""

    def test_extract_multiple_times_to_same_location(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extracting multiple times to the same location works."""
        service = WallpapersService(sample_archive)

        # Extract first time
        result1 = service.extract_wallpapers(temp_dir)
        files1 = list(result1.iterdir())

        # Extract second time (should overwrite)
        result2 = service.extract_wallpapers(temp_dir)
        files2 = list(result2.iterdir())

        # Should have same files
        assert len(files1) == len(files2)
        assert result1 == result2

    def test_extract_returns_path_with_correct_name(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extract returns path ending with 'wallpapers' directory name."""
        service = WallpapersService(sample_archive)
        result = service.extract_wallpapers(temp_dir)

        assert result.name == "wallpapers"
        assert result.parent == temp_dir


class TestFilenameHandling:
    """Tests for how filenames are handled during add operations."""

    def test_add_preserves_original_filename(
        self, nonexistent_archive: Path, temp_dir: Path
    ) -> None:
        """Add preserves the original filename from the source path."""
        # Create file with specific name
        source = temp_dir / "my-custom-wallpaper-2024.png"
        source.write_bytes(b"content")

        service = WallpapersService(nonexistent_archive)
        service.add_wallpaper(source)

        wallpapers = service.list_wallpapers()
        assert "my-custom-wallpaper-2024.png" in wallpapers

    def test_add_uses_basename_not_full_path(
        self, nonexistent_archive: Path, temp_dir: Path
    ) -> None:
        """Add stores only the filename, not the full directory path."""
        # Create nested directory structure
        nested = temp_dir / "deep" / "nested" / "path"
        nested.mkdir(parents=True)
        image = nested / "wallpaper.png"
        image.write_bytes(b"content")

        service = WallpapersService(nonexistent_archive)
        service.add_wallpaper(image)

        wallpapers = service.list_wallpapers()
        # Should only have the filename, not the path
        assert wallpapers == ["wallpaper.png"]


class TestArchiveFormatBehavior:
    """Tests for tar.gz archive format specifics."""

    def test_archive_is_compressed_gzip(
        self, nonexistent_archive: Path, sample_image: Path
    ) -> None:
        """Created archive is in gzip-compressed tar format."""
        service = WallpapersService(nonexistent_archive)
        service.add_wallpaper(sample_image)

        # Verify it's a valid gzip tar archive
        assert tarfile.is_tarfile(nonexistent_archive)
        with tarfile.open(nonexistent_archive, "r:gz") as tar:
            members = tar.getmembers()
            assert len(members) >= 1

    def test_add_creates_parent_directories(self, temp_dir: Path, sample_image: Path) -> None:
        """Add creates parent directories for archive if they don't exist."""
        # Archive path with non-existent parent directories
        archive_path = temp_dir / "level1" / "level2" / "level3" / "archive.tar.gz"

        service = WallpapersService(archive_path)
        service.add_wallpaper(sample_image)

        assert archive_path.exists()
        assert archive_path.parent.exists()
