# src/api/config.py
"""Main configuration management class."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.assets import Assets
    from src.api.packages import Packages


class Config:
    """Main configuration management class.

    Provides unified access to all dotfiles configuration modules.

    Example:
        from src import Config

        cfg = Config()
        cfg.assets.wallpapers.list()
        cfg.packages.install(tags=["nvim"])
    """

    def __init__(self) -> None:
        """Initialize Config."""
        self._assets: "Assets | None" = None
        self._packages: "Packages | None" = None

    @property
    def assets(self) -> "Assets":
        """Access asset management functionality.

        Returns:
            Assets API instance
        """
        if self._assets is None:
            from src.api.assets import Assets

            self._assets = Assets()
        return self._assets

    @property
    def packages(self) -> "Packages":
        """Access package management functionality.

        Returns:
            Packages API instance
        """
        if self._packages is None:
            from src.api.packages import Packages

            self._packages = Packages()
        return self._packages
