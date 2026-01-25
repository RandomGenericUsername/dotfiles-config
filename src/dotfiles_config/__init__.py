from dotfiles_packages import Packages
from dotfiles_packages import (
    PackageRole,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
)
from dotfiles_wallpapers import Wallpapers
from dotfiles_wallpapers import (
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
)
from dotfiles_icon_templates import IconTemplates
from dotfiles_icon_templates import (
    IconTemplateError,
    CategoryNotFoundError,
    IconNotFoundError,
    IconInfo,
)
from dotfiles_config.cli import app


def main() -> None:
    """Run the CLI."""
    app()


__all__ = [
    # Packages
    "Packages",
    "PackageRole",
    "PackagesError",
    "PlaybookNotFoundError",
    "AnsibleError",
    "AnsibleNotFoundError",
    # Wallpapers
    "Wallpapers",
    "WallpaperError",
    "ArchiveNotFoundError",
    "WallpaperNotFoundError",
    "InvalidImageError",
    # Icon Templates
    "IconTemplates",
    "IconTemplateError",
    "CategoryNotFoundError",
    "IconNotFoundError",
    "IconInfo",
    # CLI
    "app",
    "main",
]


