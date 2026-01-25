# dotfiles-icon-templates/src/dotfiles_icon_templates/services/icon_templates_service.py
"""Service layer for icon template management."""
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from dotfiles_icon_templates.constants import PACKAGE_ROOT


class IconTemplateError(Exception):
    """Base exception for icon template operations."""


class CategoryNotFoundError(IconTemplateError):
    """Raised when a category doesn't exist."""


class IconNotFoundError(IconTemplateError):
    """Raised when an icon doesn't exist."""


@dataclass
class IconInfo:
    """Information about an icon template."""

    name: str
    category: str
    path: Path
    variants: List[str] = None

    def __post_init__(self):
        """Initialize variants as empty list if None."""
        if self.variants is None:
            self.variants = []


class IconTemplatesService:
    """Service for managing icon templates."""

    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize IconTemplatesService.

        Args:
            data_dir: Path to data directory containing icon categories
        """
        if data_dir is None:
            # Default to dotfiles-icon-templates/data
            data_dir = PACKAGE_ROOT / "data"

        self.data_dir = data_dir

    def _ensure_data_dir_exists(self) -> None:
        """Raise IconTemplateError if data directory doesn't exist."""
        if not self.data_dir.exists():
            raise IconTemplateError(
                f"Data directory not found: {self.data_dir}"
            )

    def categories(self) -> List[str]:
        """Get list of available categories.

        Returns:
            List of category directory names

        Raises:
            IconTemplateError: If data directory doesn't exist
        """
        self._ensure_data_dir_exists()

        categories = []
        for item in self.data_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                categories.append(item.name)

        return sorted(categories)

    def list(self, category: Optional[str] = None) -> List[str]:
        """List icons, optionally filtered by category.

        Args:
            category: Optional category to filter by

        Returns:
            List of icon filenames

        Raises:
            IconTemplateError: If data directory doesn't exist
            CategoryNotFoundError: If category doesn't exist
        """
        self._ensure_data_dir_exists()

        if category is None:
            # Return all icons from all categories
            all_icons = []
            for cat in self.categories():
                cat_path = self.data_dir / cat
                for icon_file in cat_path.iterdir():
                    if icon_file.is_file() and not icon_file.name.startswith("."):
                        all_icons.append(icon_file.name)
            return sorted(all_icons)
        else:
            # Return icons from specific category
            cat_path = self.data_dir / category
            if not cat_path.exists():
                raise CategoryNotFoundError(f"Category not found: {category}")

            icons = []
            for icon_file in cat_path.iterdir():
                if icon_file.is_file() and not icon_file.name.startswith("."):
                    icons.append(icon_file.name)

            return sorted(icons)

    def show(self, icon_name: str) -> IconInfo:
        """Get details about a specific icon.

        Args:
            icon_name: Name of the icon

        Returns:
            IconInfo object with icon details

        Raises:
            IconTemplateError: If data directory doesn't exist
            IconNotFoundError: If icon not found
        """
        self._ensure_data_dir_exists()

        # Search for icon in all categories
        for cat_dir in self.data_dir.iterdir():
            if not cat_dir.is_dir() or cat_dir.name.startswith("."):
                continue

            icon_path = cat_dir / icon_name
            if icon_path.exists():
                return IconInfo(
                    name=icon_name,
                    category=cat_dir.name,
                    path=icon_path,
                    variants=[],
                )

        raise IconNotFoundError(f"Icon not found: {icon_name}")

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
            IconTemplateError: If data directory doesn't exist or target not writable
            CategoryNotFoundError: If category doesn't exist
            IconNotFoundError: If specific icon not found
        """
        self._ensure_data_dir_exists()

        # Ensure target directory exists
        target_path = target_path.resolve()
        target_path.mkdir(parents=True, exist_ok=True)

        copied = []

        if icons:
            # Copy specific icons
            for icon_name in icons:
                icon_info = self.show(icon_name)
                dest = target_path / icon_name
                shutil.copy2(icon_info.path, dest)
                copied.append(icon_name)
        elif category:
            # Copy all icons from category
            if not (self.data_dir / category).exists():
                raise CategoryNotFoundError(f"Category not found: {category}")

            cat_path = self.data_dir / category
            for icon_file in cat_path.iterdir():
                if icon_file.is_file() and not icon_file.name.startswith("."):
                    dest = target_path / icon_file.name
                    shutil.copy2(icon_file, dest)
                    copied.append(icon_file.name)
        else:
            # Copy all icons
            for cat_dir in self.data_dir.iterdir():
                if not cat_dir.is_dir() or cat_dir.name.startswith("."):
                    continue

                for icon_file in cat_dir.iterdir():
                    if icon_file.is_file() and not icon_file.name.startswith("."):
                        dest = target_path / icon_file.name
                        shutil.copy2(icon_file, dest)
                        copied.append(icon_file.name)

        return sorted(copied)
