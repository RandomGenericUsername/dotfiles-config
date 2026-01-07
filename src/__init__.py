# src/__init__.py
"""Dotfiles Configuration Management.

Usage:
    from src import Config

    cfg = Config()
    cfg.assets.wallpapers.list()
    cfg.packages.list()
"""

from src.api import Assets, Config, Packages, Wallpapers

__all__ = ["Config", "Assets", "Packages", "Wallpapers"]
