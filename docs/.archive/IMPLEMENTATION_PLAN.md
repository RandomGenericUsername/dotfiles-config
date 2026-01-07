# Implementation Plan: Assets Wallpapers CLI Commands

## Overview

Add a nested command structure to the CLI:
```
config assets wallpapers add <path>      # Add wallpaper to archive
config assets wallpapers extract <path>  # Extract wallpapers to path/wallpapers/
config assets wallpapers list            # List wallpapers in archive (bonus)
```

## Architecture

### Directory Structure (Final State)

```
src/
├── main.py                          # Updated: register assets app
├── commands/
│   ├── __init__.py
│   ├── dummy.py
│   ├── install_packages.py
│   └── assets/                      # NEW: assets command group
│       ├── __init__.py              # Assets Typer sub-app
│       └── wallpapers/              # NEW: wallpapers subcommand group
│           ├── __init__.py          # Wallpapers Typer sub-app with commands
│           └── service.py           # Core wallpaper logic (testable)
│
tests/                               # NEW: test directory
├── __init__.py
├── conftest.py                      # Shared fixtures
├── unit/
│   ├── __init__.py
│   └── test_wallpapers_service.py   # Unit tests for service layer
└── integration/
    ├── __init__.py
    └── test_wallpapers_cli.py       # CLI integration tests
```

### Design Decisions

1. **Separation of Concerns**: Core tar.gz logic lives in `service.py`, CLI layer in `__init__.py`
2. **Nested Typer Apps**: Use `app.add_typer()` for command groups
3. **Dependency Injection**: Service receives archive path, making it testable
4. **Path Resolution**: Archive path resolved relative to package location using `__file__`

---

## Phase 1: Test Infrastructure Setup

### Step 1.1: Add Test Dependencies to pyproject.toml

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### Step 1.2: Create Test Directory Structure

Create empty files:
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/unit/__init__.py`
- `tests/integration/__init__.py`

### Step 1.3: Create conftest.py with Fixtures

```python
# tests/conftest.py
import tarfile
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample image file for testing."""
    image_path = temp_dir / "test_wallpaper.png"
    # Create a minimal valid PNG (1x1 transparent pixel)
    # PNG header + IHDR + IDAT + IEND
    png_bytes = (
        b'\x89PNG\r\n\x1a\n'  # PNG signature
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'  # 1x1 RGBA
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
        b'\r\n-\xb4'
        b'\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    image_path.write_bytes(png_bytes)
    return image_path


@pytest.fixture
def sample_archive(temp_dir: Path, sample_image: Path) -> Path:
    """Create a sample tar.gz archive with one wallpaper."""
    archive_path = temp_dir / "wallpapers.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(sample_image, arcname=sample_image.name)
    return archive_path


@pytest.fixture
def empty_archive(temp_dir: Path) -> Path:
    """Create an empty tar.gz archive."""
    archive_path = temp_dir / "wallpapers.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        pass  # Create empty archive
    return archive_path


@pytest.fixture
def nonexistent_archive(temp_dir: Path) -> Path:
    """Return path to a nonexistent archive."""
    return temp_dir / "nonexistent.tar.gz"
```

### Step 1.4: Update Makefile

Add test target to `Makefile`:

```makefile
test:
	uv run pytest -v

test-cov:
	uv run pytest -v --cov=src --cov-report=term-missing

install-dev:
	uv pip install -e ".[dev]"
```

---

## Phase 2: Wallpapers Service Layer (TDD)

### Step 2.1: Write Unit Tests First

Create `tests/unit/test_wallpapers_service.py`:

```python
# tests/unit/test_wallpapers_service.py
"""Unit tests for wallpapers service layer."""
import tarfile
from pathlib import Path

import pytest

from src.commands.assets.wallpapers.service import (
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
```

### Step 2.2: Implement the Service Layer

Create `src/commands/assets/__init__.py`:

```python
# src/commands/assets/__init__.py
"""Assets command group."""
from typer import Typer

from src.commands.assets.wallpapers import wallpapers_app

assets_app = Typer(help="Manage dotfiles assets")
assets_app.add_typer(wallpapers_app, name="wallpapers")
```

Create `src/commands/assets/wallpapers/__init__.py`:

```python
# src/commands/assets/wallpapers/__init__.py
"""Wallpapers subcommand group."""
from pathlib import Path

import typer

from src.commands.assets.wallpapers.service import (
    WallpapersService,
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
)

wallpapers_app = typer.Typer(help="Manage wallpaper assets")


def get_default_archive_path() -> Path:
    """Get the default archive path relative to this package."""
    package_dir = Path(__file__).parent
    # Navigate up to config root, then to assets/wallpapers
    config_root = package_dir.parent.parent.parent.parent
    return config_root / "assets" / "wallpapers" / "wallpapers.tar.gz"


def get_service() -> WallpapersService:
    """Create a WallpapersService with the default archive path."""
    return WallpapersService(get_default_archive_path())


@wallpapers_app.command("add")
def add_wallpaper(
    path: Path = typer.Argument(
        ...,
        help="Path to the wallpaper image to add",
        exists=True,
        readable=True,
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite if wallpaper with same name exists",
    ),
    no_validate: bool = typer.Option(
        False,
        "--no-validate",
        help="Skip image extension validation",
    ),
) -> None:
    """Add a wallpaper to the archive."""
    service = get_service()
    try:
        service.add_wallpaper(
            path,
            overwrite=force,
            validate_extension=not no_validate,
        )
        typer.echo(f"Successfully added '{path.name}' to wallpapers archive")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@wallpapers_app.command("extract")
def extract_wallpapers(
    path: Path = typer.Argument(
        ...,
        help="Directory where wallpapers will be extracted (creates 'wallpapers' subdirectory)",
    ),
) -> None:
    """Extract all wallpapers to the specified directory."""
    service = get_service()
    try:
        result_path = service.extract_wallpapers(path)
        wallpapers = list(result_path.iterdir())
        typer.echo(f"Extracted {len(wallpapers)} wallpaper(s) to {result_path}")
    except ArchiveNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@wallpapers_app.command("list")
def list_wallpapers() -> None:
    """List all wallpapers in the archive."""
    service = get_service()
    try:
        wallpapers = service.list_wallpapers()
        if not wallpapers:
            typer.echo("No wallpapers in archive")
            return
        typer.echo(f"Wallpapers in archive ({len(wallpapers)}):")
        for name in sorted(wallpapers):
            typer.echo(f"  - {name}")
    except ArchiveNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
```

Create `src/commands/assets/wallpapers/service.py`:

```python
# src/commands/assets/wallpapers/service.py
"""Core wallpaper management service."""
import shutil
import tarfile
import tempfile
from pathlib import Path
from typing import List


class WallpaperError(Exception):
    """Base exception for wallpaper operations."""

    pass


class ArchiveNotFoundError(WallpaperError):
    """Raised when the wallpaper archive doesn't exist."""

    pass


class WallpaperNotFoundError(WallpaperError):
    """Raised when a wallpaper file doesn't exist."""

    pass


class InvalidImageError(WallpaperError):
    """Raised when a file is not a valid image."""

    pass


class WallpapersService:
    """Service for managing wallpapers in a tar.gz archive."""

    VALID_EXTENSIONS = frozenset(
        ["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "tif"]
    )

    def __init__(self, archive_path: Path) -> None:
        """Initialize the service with the archive path.

        Args:
            archive_path: Path to the wallpapers.tar.gz archive
        """
        self.archive_path = archive_path

    @classmethod
    def is_valid_image_extension(cls, filename: str) -> bool:
        """Check if a filename has a valid image extension.

        Args:
            filename: The filename to check

        Returns:
            True if the extension is a recognized image format
        """
        if "." not in filename:
            return False
        extension = filename.rsplit(".", 1)[-1].lower()
        return extension in cls.VALID_EXTENSIONS

    def _ensure_archive_exists(self) -> None:
        """Raise ArchiveNotFoundError if archive doesn't exist."""
        if not self.archive_path.exists():
            raise ArchiveNotFoundError(
                f"Archive not found: {self.archive_path}"
            )

    def list_wallpapers(self) -> List[str]:
        """List all wallpaper names in the archive.

        Returns:
            List of wallpaper filenames

        Raises:
            ArchiveNotFoundError: If archive doesn't exist
        """
        self._ensure_archive_exists()

        with tarfile.open(self.archive_path, "r:gz") as tar:
            # Filter out directories, only return files
            return [
                member.name
                for member in tar.getmembers()
                if member.isfile() and not member.name.startswith(".")
            ]

    def add_wallpaper(
        self,
        wallpaper_path: Path,
        overwrite: bool = True,
        validate_extension: bool = True,
    ) -> None:
        """Add a wallpaper to the archive.

        Args:
            wallpaper_path: Path to the wallpaper file
            overwrite: If True, replace existing wallpaper with same name
            validate_extension: If True, validate file has image extension

        Raises:
            WallpaperNotFoundError: If wallpaper file doesn't exist
            InvalidImageError: If file doesn't have valid image extension
            WallpaperError: If wallpaper exists and overwrite=False
        """
        # Resolve path (handles relative paths)
        wallpaper_path = wallpaper_path.resolve()

        if not wallpaper_path.exists():
            raise WallpaperNotFoundError(
                f"Wallpaper file not found: {wallpaper_path}"
            )

        filename = wallpaper_path.name

        if validate_extension and not self.is_valid_image_extension(filename):
            raise InvalidImageError(
                f"File does not have a valid image extension: {filename}"
            )

        # Check for duplicates if archive exists
        if self.archive_path.exists():
            existing = self.list_wallpapers()
            if filename in existing and not overwrite:
                raise WallpaperError(
                    f"Wallpaper '{filename}' already exists in archive. "
                    "Use --force to overwrite."
                )

        # Create or update archive
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)

            # Extract existing files if archive exists
            if self.archive_path.exists():
                with tarfile.open(self.archive_path, "r:gz") as tar:
                    tar.extractall(tmp_path)

            # Copy new wallpaper (overwrites if exists)
            shutil.copy2(wallpaper_path, tmp_path / filename)

            # Create new archive
            with tarfile.open(self.archive_path, "w:gz") as tar:
                for file_path in tmp_path.iterdir():
                    if file_path.is_file() and not file_path.name.startswith("."):
                        tar.add(file_path, arcname=file_path.name)

    def extract_wallpapers(self, output_path: Path) -> Path:
        """Extract all wallpapers to a directory.

        Creates a 'wallpapers' subdirectory in the output path.

        Args:
            output_path: Parent directory for extraction

        Returns:
            Path to the 'wallpapers' subdirectory containing extracted files

        Raises:
            ArchiveNotFoundError: If archive doesn't exist
        """
        self._ensure_archive_exists()

        # Create the wallpapers subdirectory
        wallpapers_dir = output_path / "wallpapers"
        wallpapers_dir.mkdir(parents=True, exist_ok=True)

        # Extract files
        with tarfile.open(self.archive_path, "r:gz") as tar:
            tar.extractall(wallpapers_dir)

        return wallpapers_dir
```

---

## Phase 3: CLI Integration Tests (TDD)

### Step 3.1: Write CLI Integration Tests

Create `tests/integration/test_wallpapers_cli.py`:

```python
# tests/integration/test_wallpapers_cli.py
"""Integration tests for wallpapers CLI commands."""
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from src.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI test runner."""
    return CliRunner()


class TestWallpapersAddCommand:
    """Tests for 'config assets wallpapers add' command."""

    def test_add_shows_in_help(self, cli_runner: CliRunner) -> None:
        """Add command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "add" in result.output

    def test_add_wallpaper_success(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add wallpaper successfully."""
        new_image = temp_dir / "new.png"
        new_image.write_bytes(b"png content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(new_image)]
            )

        assert result.exit_code == 0
        assert "Successfully added" in result.output

    def test_add_nonexistent_file_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """Add nonexistent file shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "/nonexistent/file.png"]
            )

        assert result.exit_code != 0

    def test_add_duplicate_without_force_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Add duplicate without --force shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(sample_image)]
            )

        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_add_duplicate_with_force_succeeds(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Add duplicate with --force succeeds."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "--force", str(sample_image)]
            )

        assert result.exit_code == 0
        assert "Successfully added" in result.output

    def test_add_invalid_extension_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add non-image file shows error."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("text content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(text_file)]
            )

        assert result.exit_code == 1
        assert "valid image extension" in result.output

    def test_add_no_validate_allows_any_file(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add with --no-validate allows non-image files."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("text content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app,
                ["assets", "wallpapers", "add", "--no-validate", str(text_file)],
            )

        assert result.exit_code == 0


class TestWallpapersExtractCommand:
    """Tests for 'config assets wallpapers extract' command."""

    def test_extract_shows_in_help(self, cli_runner: CliRunner) -> None:
        """Extract command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "extract" in result.output

    def test_extract_creates_wallpapers_dir(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract creates wallpapers subdirectory."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(output_dir)]
            )

        assert result.exit_code == 0
        assert (output_dir / "wallpapers").is_dir()
        assert "Extracted" in result.output

    def test_extract_missing_archive_fails(
        self,
        cli_runner: CliRunner,
        nonexistent_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract with missing archive shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=nonexistent_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(temp_dir)]
            )

        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestWallpapersListCommand:
    """Tests for 'config assets wallpapers list' command."""

    def test_list_shows_in_help(self, cli_runner: CliRunner) -> None:
        """List command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_list_shows_wallpapers(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """List displays wallpaper names."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        assert "test_wallpaper.png" in result.output

    def test_list_empty_archive(
        self,
        cli_runner: CliRunner,
        empty_archive: Path,
    ) -> None:
        """List shows message for empty archive."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=empty_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        assert "No wallpapers" in result.output


class TestCommandHierarchy:
    """Tests for the command hierarchy structure."""

    def test_assets_command_exists(self, cli_runner: CliRunner) -> None:
        """Assets command is registered."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "assets" in result.output

    def test_assets_wallpapers_command_exists(self, cli_runner: CliRunner) -> None:
        """Wallpapers subcommand is registered under assets."""
        result = cli_runner.invoke(app, ["assets", "--help"])
        assert result.exit_code == 0
        assert "wallpapers" in result.output

    def test_full_command_path_works(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """Full command path 'assets wallpapers list' works."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])
        assert result.exit_code == 0
```

### Step 3.2: Update main.py to Register Assets Command

Update `src/main.py`:

```python
from typer import Typer

from src.commands.dummy import dummy
from src.commands.install_packages import install_packages
from src.commands.assets import assets_app

app = Typer(help="Dotfiles configuration management CLI")

# Register command groups
app.add_typer(assets_app, name="assets")

# Register individual commands
app.command(
    "install-packages",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Install packages using Ansible playbook",
)(install_packages)
app.command(help="A dummy command that prints a message")(dummy)


def main():
    app()


if __name__ == "__main__":
    main()
```

---

## Phase 4: Implementation Checklist

Execute in this order, running tests after each step:

### Step 4.1: Setup Test Infrastructure
- [ ] Update `pyproject.toml` with test dependencies
- [ ] Create test directory structure
- [ ] Create `tests/conftest.py` with fixtures
- [ ] Update `Makefile` with test targets
- [ ] Run: `make install-dev` to install test dependencies
- [ ] Verify: `uv run pytest --collect-only` shows no errors

### Step 4.2: Create Package Structure
- [ ] Create `src/commands/assets/__init__.py` (empty initially)
- [ ] Create `src/commands/assets/wallpapers/__init__.py` (empty initially)
- [ ] Create `src/commands/assets/wallpapers/service.py` (empty class stubs)
- [ ] Verify: No import errors

### Step 4.3: Implement Service Layer (TDD)
- [ ] Write `tests/unit/test_wallpapers_service.py`
- [ ] Run tests: `uv run pytest tests/unit/` - expect all failures
- [ ] Implement exception classes in `service.py`
- [ ] Implement `WallpapersService.__init__`
- [ ] Implement `is_valid_image_extension` (run tests, some should pass)
- [ ] Implement `list_wallpapers` (run tests)
- [ ] Implement `add_wallpaper` (run tests)
- [ ] Implement `extract_wallpapers` (run tests)
- [ ] Verify: All unit tests pass

### Step 4.4: Implement CLI Layer (TDD)
- [ ] Write `tests/integration/test_wallpapers_cli.py`
- [ ] Run tests: `uv run pytest tests/integration/` - expect all failures
- [ ] Implement `src/commands/assets/__init__.py` with assets_app
- [ ] Implement `src/commands/assets/wallpapers/__init__.py` with commands
- [ ] Update `src/main.py` to register assets_app
- [ ] Verify: All integration tests pass

### Step 4.5: Manual Verification
- [ ] Run: `config --help` - verify "assets" appears
- [ ] Run: `config assets --help` - verify "wallpapers" appears
- [ ] Run: `config assets wallpapers --help` - verify add/extract/list appear
- [ ] Run: `config assets wallpapers list` - verify it works with real archive
- [ ] Run: `config assets wallpapers add <test-image>` - verify add works
- [ ] Run: `config assets wallpapers extract /tmp/test` - verify extraction

### Step 4.6: Full Test Suite
- [ ] Run: `uv run pytest -v` - all tests pass
- [ ] Run: `uv run pytest --cov=src` - verify coverage

---

## Error Handling Summary

| Error | Exception | CLI Exit Code | User Message |
|-------|-----------|---------------|--------------|
| Archive not found | `ArchiveNotFoundError` | 1 | "Archive not found: {path}" |
| Wallpaper file not found | `WallpaperNotFoundError` | 1 | "Wallpaper file not found: {path}" |
| Invalid image extension | `InvalidImageError` | 1 | "File does not have a valid image extension" |
| Duplicate without --force | `WallpaperError` | 1 | "Wallpaper '{name}' already exists. Use --force" |

---

## CLI Usage Examples (Final)

```bash
# List all wallpapers
config assets wallpapers list

# Add a wallpaper
config assets wallpapers add ~/Pictures/mountain.jpg

# Add with force (overwrite existing)
config assets wallpapers add --force ~/Pictures/mountain.jpg

# Add non-image file (skip validation)
config assets wallpapers add --no-validate ~/Documents/wallpaper-list.txt

# Extract to directory (creates /tmp/output/wallpapers/)
config assets wallpapers extract /tmp/output

# Help
config assets wallpapers --help
config assets wallpapers add --help
```

---

## Notes for Implementation

1. **Import Order**: Python imports should be absolute from `src.` prefix
2. **Path Resolution**: Always use `.resolve()` for relative paths before operations
3. **Tar Safety**: Use `extractall` carefully - this is safe since we control the archive
4. **Temp Directory**: Always use `tempfile.TemporaryDirectory()` context manager
5. **Error Messages**: Include the path in error messages for debugging
6. **Exit Codes**: Use `raise typer.Exit(1)` for error exits, not `sys.exit()`
