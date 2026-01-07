# tests/unit/test_wallpapers_service.py
"""Unit tests for wallpapers service layer."""
import tarfile
from pathlib import Path

import pytest

from src.services.wallpapers_service import (
    WallpapersService,
    WallpaperError,
    WallpaperNotFoundError,
    ArchiveNotFoundError,
    InvalidImageError,
)


class TestWallpapersServiceInit:
    """Tests for WallpapersService initialization."""

    def test_init_with_valid_archive(self, sample_archive: Path) -> None:
        """Service initializes with existing archive path."""
        service = WallpapersService(sample_archive)
        assert service.archive_path == sample_archive

    def test_init_with_nonexistent_archive(self, nonexistent_archive: Path) -> None:
        """Service initializes even if archive doesn't exist yet."""
        service = WallpapersService(nonexistent_archive)
        assert service.archive_path == nonexistent_archive


class TestWallpapersServiceList:
    """Tests for listing wallpapers."""

    def test_list_wallpapers_in_archive(self, sample_archive: Path) -> None:
        """List returns wallpaper names from archive."""
        service = WallpapersService(sample_archive)
        wallpapers = service.list_wallpapers()
        assert "test_wallpaper.png" in wallpapers

    def test_list_empty_archive(self, empty_archive: Path) -> None:
        """List returns empty list for empty archive."""
        service = WallpapersService(empty_archive)
        wallpapers = service.list_wallpapers()
        assert wallpapers == []

    def test_list_nonexistent_archive_raises(self, nonexistent_archive: Path) -> None:
        """List raises ArchiveNotFoundError if archive doesn't exist."""
        service = WallpapersService(nonexistent_archive)
        with pytest.raises(ArchiveNotFoundError):
            service.list_wallpapers()


class TestWallpapersServiceAdd:
    """Tests for adding wallpapers."""

    def test_add_wallpaper_to_existing_archive(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add new wallpaper to existing archive."""
        # Create a new image to add
        new_image = temp_dir / "new_wallpaper.jpg"
        new_image.write_bytes(b"fake jpg content")  # Content doesn't matter for test

        service = WallpapersService(sample_archive)
        service.add_wallpaper(new_image)

        # Verify it was added
        wallpapers = service.list_wallpapers()
        assert "new_wallpaper.jpg" in wallpapers
        assert "test_wallpaper.png" in wallpapers  # Original still there

    def test_add_wallpaper_creates_archive_if_missing(
        self, nonexistent_archive: Path, sample_image: Path
    ) -> None:
        """Add creates archive if it doesn't exist."""
        service = WallpapersService(nonexistent_archive)
        service.add_wallpaper(sample_image)

        assert nonexistent_archive.exists()
        wallpapers = service.list_wallpapers()
        assert "test_wallpaper.png" in wallpapers

    def test_add_nonexistent_file_raises(self, sample_archive: Path) -> None:
        """Add raises WallpaperNotFoundError for missing file."""
        service = WallpapersService(sample_archive)
        with pytest.raises(WallpaperNotFoundError):
            service.add_wallpaper(Path("/nonexistent/wallpaper.png"))

    def test_add_overwrites_existing_wallpaper(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add replaces wallpaper with same name when overwrite=True."""
        # Create file with same name but different content
        duplicate = temp_dir / "subfolder" / "test_wallpaper.png"
        duplicate.parent.mkdir()
        duplicate.write_bytes(b"new content")

        service = WallpapersService(sample_archive)
        service.add_wallpaper(duplicate, overwrite=True)

        # Should still have exactly one wallpaper with that name
        wallpapers = service.list_wallpapers()
        assert wallpapers.count("test_wallpaper.png") == 1

    def test_add_duplicate_without_overwrite_raises(
        self, sample_archive: Path, sample_image: Path
    ) -> None:
        """Add raises error for duplicate when overwrite=False."""
        service = WallpapersService(sample_archive)
        with pytest.raises(WallpaperError, match="already exists"):
            service.add_wallpaper(sample_image, overwrite=False)

    def test_add_validates_image_extension(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add raises InvalidImageError for non-image files by default."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("not an image")

        service = WallpapersService(sample_archive)
        with pytest.raises(InvalidImageError):
            service.add_wallpaper(text_file)

    def test_add_allows_skip_validation(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Add accepts non-image files when validate=False."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("not an image")

        service = WallpapersService(sample_archive)
        service.add_wallpaper(text_file, validate_extension=False)

        wallpapers = service.list_wallpapers()
        assert "readme.txt" in wallpapers

    def test_add_handles_relative_path(
        self, sample_archive: Path, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Add works with relative paths."""
        new_image = temp_dir / "relative_test.png"
        new_image.write_bytes(b"content")

        monkeypatch.chdir(temp_dir)

        service = WallpapersService(sample_archive)
        service.add_wallpaper(Path("relative_test.png"))

        wallpapers = service.list_wallpapers()
        assert "relative_test.png" in wallpapers


class TestWallpapersServiceExtract:
    """Tests for extracting wallpapers."""

    def test_extract_creates_wallpapers_subdirectory(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extract creates 'wallpapers' subdirectory in target."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        service = WallpapersService(sample_archive)
        result_path = service.extract_wallpapers(output_dir)

        expected_path = output_dir / "wallpapers"
        assert result_path == expected_path
        assert expected_path.is_dir()

    def test_extract_places_files_in_subdirectory(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extract places wallpaper files in the wallpapers subdirectory."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        service = WallpapersService(sample_archive)
        result_path = service.extract_wallpapers(output_dir)

        extracted_file = result_path / "test_wallpaper.png"
        assert extracted_file.exists()

    def test_extract_creates_parent_directory(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extract creates parent directory if it doesn't exist."""
        output_dir = temp_dir / "nonexistent" / "nested" / "path"

        service = WallpapersService(sample_archive)
        result_path = service.extract_wallpapers(output_dir)

        assert result_path.is_dir()
        assert (result_path / "test_wallpaper.png").exists()

    def test_extract_empty_archive(
        self, empty_archive: Path, temp_dir: Path
    ) -> None:
        """Extract empty archive creates empty wallpapers directory."""
        output_dir = temp_dir / "output"

        service = WallpapersService(empty_archive)
        result_path = service.extract_wallpapers(output_dir)

        assert result_path.is_dir()
        assert list(result_path.iterdir()) == []

    def test_extract_nonexistent_archive_raises(
        self, nonexistent_archive: Path, temp_dir: Path
    ) -> None:
        """Extract raises ArchiveNotFoundError if archive doesn't exist."""
        service = WallpapersService(nonexistent_archive)
        with pytest.raises(ArchiveNotFoundError):
            service.extract_wallpapers(temp_dir)

    def test_extract_returns_list_of_extracted_files(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Extract returns the path to wallpapers directory."""
        service = WallpapersService(sample_archive)
        result = service.extract_wallpapers(temp_dir)

        assert isinstance(result, Path)
        assert result.name == "wallpapers"


class TestWallpapersServiceValidation:
    """Tests for image validation."""

    @pytest.mark.parametrize(
        "filename",
        [
            "image.jpg",
            "image.jpeg",
            "image.png",
            "image.gif",
            "image.bmp",
            "image.webp",
            "image.tiff",
            "image.tif",
            "IMAGE.JPG",  # Case insensitive
            "IMAGE.PNG",
        ],
    )
    def test_valid_image_extensions(self, filename: str) -> None:
        """Recognized image extensions are valid."""
        assert WallpapersService.is_valid_image_extension(filename) is True

    @pytest.mark.parametrize(
        "filename",
        [
            "document.txt",
            "script.py",
            "archive.tar.gz",
            "video.mp4",
            "noextension",
        ],
    )
    def test_invalid_image_extensions(self, filename: str) -> None:
        """Non-image extensions are invalid."""
        assert WallpapersService.is_valid_image_extension(filename) is False
