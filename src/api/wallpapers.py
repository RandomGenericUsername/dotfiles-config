# src/api/wallpapers.py
"""Python API for wallpaper management."""
from pathlib import Path
from typing import List, Optional

from src.services.wallpapers_service import WallpapersService


class Wallpapers:
    """Python API for wallpaper management.

    Example:
        wallpapers = Wallpapers()
        wallpapers.list()
        wallpapers.add(Path("~/Pictures/bg.png"))
    """

    def __init__(self, archive_path: Optional[Path] = None) -> None:
        """Initialize Wallpapers API.

        Args:
            archive_path: Path to wallpapers archive. If None, uses default location.
        """
        if archive_path is None:
            archive_path = self._default_archive_path()
        self._service = WallpapersService(archive_path)

    @staticmethod
    def _default_archive_path() -> Path:
        """Get the default archive path.

        Returns:
            Path to assets/wallpapers/wallpapers.tar.gz
        """
        package_dir = Path(__file__).parent.parent
        return package_dir.parent / "assets" / "wallpapers" / "wallpapers.tar.gz"

    def list(self) -> List[str]:
        """List all wallpapers in the archive.

        Returns:
            List of wallpaper filenames

        Raises:
            ArchiveNotFoundError: If archive doesn't exist
        """
        return self._service.list_wallpapers()

    def add(
        self,
        path: Path,
        *,
        force: bool = False,
        validate: bool = True
    ) -> None:
        """Add a wallpaper to the archive.

        Args:
            path: Path to wallpaper image
            force: Overwrite if exists
            validate: Validate image extension

        Raises:
            WallpaperNotFoundError: If path doesn't exist
            InvalidImageError: If not a valid image (when validate=True)
        """
        self._service.add_wallpaper(path, overwrite=force, validate_extension=validate)

    def extract(self, output_path: Path) -> Path:
        """Extract all wallpapers to directory.

        Args:
            output_path: Target directory

        Returns:
            Path to extracted wallpapers directory
        """
        return self._service.extract_wallpapers(output_path)
