# src/api/__init__.py
"""Public API for dotfiles configuration."""
from src.api.assets import Assets
from src.api.config import Config
from src.api.packages import Packages
from src.api.wallpapers import Wallpapers

__all__ = ["Config", "Assets", "Packages", "Wallpapers"]
