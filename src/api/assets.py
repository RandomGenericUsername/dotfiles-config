# src/api/assets.py
"""Python API for asset management."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.wallpapers import Wallpapers


class Assets:
    """Python API for asset management.

    Example:
        assets = Assets()
        assets.wallpapers.list()
    """

    def __init__(self) -> None:
        """Initialize Assets API."""
        self._wallpapers: "Wallpapers | None" = None

    @property
    def wallpapers(self) -> "Wallpapers":
        """Access wallpaper management functionality.

        Returns:
            Wallpapers API instance
        """
        if self._wallpapers is None:
            from src.api.wallpapers import Wallpapers

            self._wallpapers = Wallpapers()
        return self._wallpapers
