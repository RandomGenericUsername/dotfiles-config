# tests/unit/test_api.py
"""Unit tests for public API classes."""
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.api.assets import Assets
from src.api.config import Config
from src.api.packages import Packages
from src.api.wallpapers import Wallpapers
from src.services.packages_service import PackageRole


class TestConfigClass:
    """Tests for the Config class."""

    def test_config_can_be_instantiated(self) -> None:
        """Config class can be instantiated."""
        cfg = Config()
        assert cfg is not None

    def test_config_has_assets_attribute(self) -> None:
        """Config instance has assets attribute."""
        cfg = Config()
        assert hasattr(cfg, "assets")

    def test_config_has_packages_attribute(self) -> None:
        """Config instance has packages attribute."""
        cfg = Config()
        assert hasattr(cfg, "packages")

    def test_config_assets_is_assets_instance(self) -> None:
        """Config.assets returns Assets instance."""
        cfg = Config()
        assert isinstance(cfg.assets, Assets)

    def test_config_packages_is_packages_instance(self) -> None:
        """Config.packages returns Packages instance."""
        cfg = Config()
        assert isinstance(cfg.packages, Packages)

    def test_config_assets_lazy_loads(self) -> None:
        """Config lazily loads assets on first access."""
        cfg = Config()
        assets1 = cfg.assets
        assets2 = cfg.assets
        assert assets1 is assets2


class TestAssetsClass:
    """Tests for the Assets class."""

    def test_assets_can_be_instantiated(self) -> None:
        """Assets class can be instantiated."""
        assets = Assets()
        assert assets is not None

    def test_assets_has_wallpapers_attribute(self) -> None:
        """Assets instance has wallpapers attribute."""
        assets = Assets()
        assert hasattr(assets, "wallpapers")

    def test_assets_wallpapers_is_wallpapers_instance(self) -> None:
        """Assets.wallpapers returns Wallpapers instance."""
        assets = Assets()
        assert isinstance(assets.wallpapers, Wallpapers)

    def test_assets_wallpapers_lazy_loads(self) -> None:
        """Assets lazily loads wallpapers on first access."""
        assets = Assets()
        wallpapers1 = assets.wallpapers
        wallpapers2 = assets.wallpapers
        assert wallpapers1 is wallpapers2


class TestPackagesClass:
    """Tests for the Packages class."""

    def test_packages_can_be_instantiated(self) -> None:
        """Packages class can be instantiated."""
        packages = Packages()
        assert packages is not None

    def test_packages_list_returns_list(self, temp_dir: Path) -> None:
        """Packages.list() returns list of PackageRole objects."""
        playbook_content = """- name: Test Playbook
  hosts: localhost
  roles:
    - role: nvim
      tags: [editor]
"""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)
        roles = packages.list()

        assert isinstance(roles, list)
        assert len(roles) == 1
        assert isinstance(roles[0], PackageRole)
        assert roles[0].name == "nvim"
        assert roles[0].tags == ["editor"]

    def test_packages_install_runs_command(self, temp_dir: Path) -> None:
        """Packages.install() runs ansible-playbook command."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = packages.install()

            assert mock_run.called
            assert result.returncode == 0

    def test_packages_install_with_tags(self, temp_dir: Path) -> None:
        """Packages.install() accepts tags parameter."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install(tags=["nvim", "zsh"])

            call_args = mock_run.call_args[0][0]
            assert "--tags" in call_args
            tags_index = call_args.index("--tags")
            assert call_args[tags_index + 1] == "nvim,zsh"

    def test_packages_install_with_extra_args(self, temp_dir: Path) -> None:
        """Packages.install() accepts extra_args parameter."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install(extra_args=["--ask-become-pass"])

            call_args = mock_run.call_args[0][0]
            assert "--ask-become-pass" in call_args


class TestWallpapersAPIClass:
    """Tests for the Wallpapers API class."""

    def test_wallpapers_can_be_instantiated(self) -> None:
        """Wallpapers class can be instantiated."""
        wallpapers = Wallpapers()
        assert wallpapers is not None

    def test_wallpapers_list_returns_list(self, sample_archive: Path) -> None:
        """Wallpapers.list() returns list of wallpaper names."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.list()

        assert isinstance(result, list)
        assert "test_wallpaper.png" in result

    def test_wallpapers_add_success(self, temp_dir: Path, sample_image: Path) -> None:
        """Wallpapers.add() adds wallpaper to archive."""
        archive_path = temp_dir / "test.tar.gz"
        wallpapers = Wallpapers(archive_path=archive_path)

        wallpapers.add(sample_image)

        assert archive_path.exists()
        result = wallpapers.list()
        assert "test_wallpaper.png" in result

    def test_wallpapers_add_with_force(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.add() with force=True overwrites existing."""
        duplicate = temp_dir / "test_wallpaper.png"
        duplicate.write_bytes(b"new content")

        wallpapers = Wallpapers(archive_path=sample_archive)
        wallpapers.add(duplicate, force=True)

        # Should succeed without error
        result = wallpapers.list()
        assert "test_wallpaper.png" in result

    def test_wallpapers_add_without_validation(
        self, temp_dir: Path
    ) -> None:
        """Wallpapers.add() with validate=False skips extension check."""
        archive_path = temp_dir / "test.tar.gz"
        text_file = temp_dir / "file.txt"
        text_file.write_text("content")

        wallpapers = Wallpapers(archive_path=archive_path)
        wallpapers.add(text_file, validate=False)

        assert archive_path.exists()
        result = wallpapers.list()
        assert "file.txt" in result

    def test_wallpapers_extract_returns_path(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() returns path to extracted files."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.extract(temp_dir)

        assert isinstance(result, Path)
        assert result.name == "wallpapers"
        assert result.exists()
        assert (result / "test_wallpaper.png").exists()
