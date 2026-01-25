# dotfiles-wallpapers/src/dotfiles_wallpapers/services/wallpapers_service.py
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
                    tar.extractall(tmp_path, filter='data')

            # Copy new wallpaper (overwrites if exists)
            shutil.copy2(wallpaper_path, tmp_path / filename)

            # Create new archive
            # Ensure parent directory exists
            self.archive_path.parent.mkdir(parents=True, exist_ok=True)

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
            tar.extractall(wallpapers_dir, filter='data')

        return wallpapers_dir
