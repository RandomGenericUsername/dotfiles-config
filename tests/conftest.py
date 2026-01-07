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
