# dotfiles-icon-templates/src/dotfiles_icon_templates/api/icon_templates.py
"""Python API for icon template management."""
from pathlib import Path
from typing import List, Optional

from dotfiles_icon_templates.services.icon_templates_service import (
    IconTemplatesService,
    IconInfo,
)


class IconTemplates:
    """Python API for icon template management.

    Example:
        icons = IconTemplates()
        icons.list()
        icons.copy(Path("~/.config/icons"))
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        """Initialize IconTemplates API.

        Args:
            data_dir: Path to data directory containing icon categories
        """
        self._service = IconTemplatesService(data_dir)

    def categories(self) -> List[str]:
        """Get list of available categories.

        Returns:
            List of category names
        """
        return self._service.categories()

    def list(self, category: Optional[str] = None) -> List[str]:
        """List icons, optionally filtered by category.

        Args:
            category: Optional category to filter by

        Returns:
            List of icon filenames

        Raises:
            CategoryNotFoundError: If category doesn't exist
        """
        return self._service.list(category)

    def show(self, icon_name: str) -> IconInfo:
        """Get details about a specific icon.

        Args:
            icon_name: Name of the icon

        Returns:
            IconInfo object with icon details

        Raises:
            IconNotFoundError: If icon not found
        """
        return self._service.show(icon_name)

    def copy(
        self,
        target_path: Path,
        category: Optional[str] = None,
        icons: Optional[List[str]] = None,
    ) -> List[str]:
        """Copy icons to target directory.

        Args:
            target_path: Destination directory
            category: Optional category filter
            icons: Optional list of specific icon names

        Returns:
            List of copied icon filenames

        Raises:
            CategoryNotFoundError: If category doesn't exist
            IconNotFoundError: If specific icon not found
        """
        return self._service.copy(target_path, category, icons)
