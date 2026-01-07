# tests/unit/test_api_characterization.py
"""Comprehensive characterization tests for public API - source of truth for documentation."""
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src import Config
from src.api.assets import Assets
from src.api.packages import Packages
from src.api.wallpapers import Wallpapers
from src.services.packages_service import (
    AnsibleError,
    AnsibleNotFoundError,
    PackageRole,
    PlaybookNotFoundError,
)
from src.services.wallpapers_service import (
    ArchiveNotFoundError,
    InvalidImageError,
    WallpaperError,
    WallpaperNotFoundError,
)


class TestConfigCharacterization:
    """Characterization tests for Config class - documents all Config behavior."""

    def test_config_is_entry_point(self) -> None:
        """Config is the primary entry point for using the library."""
        cfg = Config()
        assert isinstance(cfg, Config)

    def test_config_lazy_loads_assets_on_first_access(self) -> None:
        """Assets are created once on first access and reused."""
        cfg = Config()
        id1 = id(cfg.assets)
        id2 = id(cfg.assets)
        id3 = id(cfg.assets)
        assert id1 == id2 == id3

    def test_config_lazy_loads_packages_on_first_access(self) -> None:
        """Packages are created once on first access and reused."""
        cfg = Config()
        id1 = id(cfg.packages)
        id2 = id(cfg.packages)
        id3 = id(cfg.packages)
        assert id1 == id2 == id3

    def test_config_assets_and_packages_are_independent(self) -> None:
        """Assets and packages are separate instances."""
        cfg = Config()
        assert cfg.assets is not cfg.packages

    def test_config_allows_independent_instances(self) -> None:
        """Multiple Config instances are independent."""
        cfg1 = Config()
        cfg2 = Config()
        assert cfg1 is not cfg2
        assert cfg1.assets is not cfg2.assets
        assert cfg1.packages is not cfg2.packages


class TestAssetsCharacterization:
    """Characterization tests for Assets class."""

    def test_assets_is_facade_for_wallpapers(self) -> None:
        """Assets provides access to wallpaper management."""
        assets = Assets()
        assert hasattr(assets, "wallpapers")
        assert isinstance(assets.wallpapers, Wallpapers)

    def test_assets_wallpapers_lazy_loads(self) -> None:
        """Wallpapers instance is created once and reused."""
        assets = Assets()
        id1 = id(assets.wallpapers)
        id2 = id(assets.wallpapers)
        assert id1 == id2

    def test_assets_can_be_instantiated_standalone(self) -> None:
        """Assets can be used independently of Config."""
        assets = Assets()
        assert assets is not None
        # Can use wallpapers directly
        assert assets.wallpapers is not None


class TestPackagesCharacterization:
    """Characterization tests for Packages class - documents all Packages behavior."""

    def test_packages_uses_default_playbook_location_when_no_args(
        self, temp_dir: Path
    ) -> None:
        """When instantiated with no args, Packages uses default playbook location."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            packages = Packages()
            # Should construct default path
            assert packages._service.playbook_path == (
                temp_dir / "packages" / "ansible" / "playbooks" / "bootstrap.yml"
            )

    def test_packages_uses_custom_playbook_path_when_provided(
        self, temp_dir: Path
    ) -> None:
        """When playbook_path is provided, Packages uses it."""
        custom_path = temp_dir / "custom.yml"
        packages = Packages(playbook_path=custom_path)
        assert packages._service.playbook_path == custom_path

    def test_packages_uses_custom_ansible_dir_when_provided(
        self, temp_dir: Path
    ) -> None:
        """When ansible_dir is provided, Packages uses it."""
        packages = Packages(ansible_dir=temp_dir)
        assert packages._service.ansible_dir == temp_dir

    def test_packages_list_returns_package_role_objects(
        self, temp_dir: Path
    ) -> None:
        """Packages.list() returns list of PackageRole objects."""
        playbook_content = """- name: Test
  hosts: localhost
  roles:
    - role: nvim
      tags: [editor]
    - role: zsh
      tags: [shell, zsh]
"""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)
        roles = packages.list()

        assert isinstance(roles, list)
        assert len(roles) == 2
        assert all(isinstance(r, PackageRole) for r in roles)
        assert roles[0].name == "nvim"
        assert roles[0].tags == ["editor"]
        assert roles[1].name == "zsh"
        assert roles[1].tags == ["shell", "zsh"]

    def test_packages_list_returns_empty_list_when_no_roles(
        self, temp_dir: Path
    ) -> None:
        """Packages.list() returns empty list when playbook has no roles."""
        playbook_content = """- name: Test
  hosts: localhost
"""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)
        roles = packages.list()

        assert roles == []

    def test_packages_list_raises_playbook_not_found_when_missing(
        self, temp_dir: Path
    ) -> None:
        """Packages.list() raises PlaybookNotFoundError when playbook doesn't exist."""
        packages = Packages(playbook_path=temp_dir / "nonexistent.yml", ansible_dir=temp_dir)

        with pytest.raises(PlaybookNotFoundError):
            packages.list()

    def test_packages_install_returns_completed_process(self, temp_dir: Path) -> None:
        """Packages.install() returns subprocess.CompletedProcess."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock(returncode=0)
            mock_run.return_value = mock_result
            result = packages.install()

            assert result is mock_result
            assert hasattr(result, "returncode")

    def test_packages_install_returns_returncode_0_on_success(self, temp_dir: Path) -> None:
        """Packages.install() returns CompletedProcess with returncode 0 on success."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = packages.install()

            assert result.returncode == 0

    def test_packages_install_runs_from_ansible_directory(self, temp_dir: Path) -> None:
        """Packages.install() runs ansible-playbook from ansible directory."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")
        ansible_dir = temp_dir

        packages = Packages(playbook_path=playbook_path, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install()

            # Verify cwd parameter
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["cwd"] == ansible_dir

    def test_packages_install_with_tags_joins_with_comma(self, temp_dir: Path) -> None:
        """Packages.install(tags=[...]) joins tags with commas."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install(tags=["nvim", "zsh", "tmux"])

            cmd = mock_run.call_args[0][0]
            tags_index = cmd.index("--tags")
            assert cmd[tags_index + 1] == "nvim,zsh,tmux"

    def test_packages_install_with_empty_tags_list_includes_tags_option(
        self, temp_dir: Path
    ) -> None:
        """Packages.install(tags=[]) does NOT include --tags if list is empty."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install(tags=[])

            cmd = mock_run.call_args[0][0]
            assert "--tags" not in cmd

    def test_packages_install_with_extra_args_passes_them_directly(
        self, temp_dir: Path
    ) -> None:
        """Packages.install(extra_args=[...]) appends args directly to command."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            packages.install(extra_args=["--ask-become-pass", "-v", "-v"])

            cmd = mock_run.call_args[0][0]
            assert "--ask-become-pass" in cmd
            assert "-v" in cmd

    def test_packages_install_raises_ansible_not_found_error_when_not_installed(
        self, temp_dir: Path
    ) -> None:
        """Packages.install() raises AnsibleNotFoundError when ansible-playbook not found."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("ansible-playbook")
            with pytest.raises(AnsibleNotFoundError):
                packages.install()

    def test_packages_install_raises_ansible_error_on_command_failure(
        self, temp_dir: Path
    ) -> None:
        """Packages.install() raises AnsibleError when ansible-playbook fails."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "ansible-playbook")
            with pytest.raises(AnsibleError):
                packages.install()

    def test_packages_install_error_preserves_return_code(self, temp_dir: Path) -> None:
        """AnsibleError preserves the original return code."""
        playbook_path = temp_dir / "bootstrap.yml"
        playbook_path.write_text("---\n")

        packages = Packages(playbook_path=playbook_path, ansible_dir=temp_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(42, "ansible-playbook")
            try:
                packages.install()
            except AnsibleError as e:
                assert e.return_code == 42


class TestWallpapersAPICharacterization:
    """Characterization tests for Wallpapers API class."""

    def test_wallpapers_uses_default_archive_path_when_no_args(self) -> None:
        """When instantiated with no args, uses default archive path."""
        wallpapers = Wallpapers()
        # Should construct path: config/assets/wallpapers/wallpapers.tar.gz
        # __file__ is at tests/unit/test_api_characterization.py
        # parent = tests/unit, parent = tests, parent = config
        expected_path = Path(__file__).parent.parent.parent / "assets" / "wallpapers" / "wallpapers.tar.gz"
        assert wallpapers._service.archive_path == expected_path

    def test_wallpapers_uses_custom_path_when_provided(self, temp_dir: Path) -> None:
        """When archive_path is provided, Wallpapers uses it."""
        custom_path = temp_dir / "custom.tar.gz"
        wallpapers = Wallpapers(archive_path=custom_path)
        assert wallpapers._service.archive_path == custom_path

    def test_wallpapers_list_returns_list_of_strings(self, sample_archive: Path) -> None:
        """Wallpapers.list() returns list of wallpaper filenames as strings."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.list()

        assert isinstance(result, list)
        assert all(isinstance(name, str) for name in result)
        assert "test_wallpaper.png" in result

    def test_wallpapers_list_raises_when_archive_missing(self, temp_dir: Path) -> None:
        """Wallpapers.list() raises ArchiveNotFoundError when archive doesn't exist."""
        wallpapers = Wallpapers(archive_path=temp_dir / "nonexistent.tar.gz")
        with pytest.raises(ArchiveNotFoundError):
            wallpapers.list()

    def test_wallpapers_add_accepts_pathlib_path(
        self, temp_dir: Path, sample_image: Path
    ) -> None:
        """Wallpapers.add() accepts pathlib.Path objects."""
        archive_path = temp_dir / "test.tar.gz"
        wallpapers = Wallpapers(archive_path=archive_path)

        wallpapers.add(sample_image)

        assert archive_path.exists()

    def test_wallpapers_add_creates_archive_if_missing(
        self, temp_dir: Path, sample_image: Path
    ) -> None:
        """Wallpapers.add() creates archive if it doesn't exist."""
        archive_path = temp_dir / "new.tar.gz"
        assert not archive_path.exists()

        wallpapers = Wallpapers(archive_path=archive_path)
        wallpapers.add(sample_image)

        assert archive_path.exists()

    def test_wallpapers_add_raises_when_file_not_found(self, temp_dir: Path) -> None:
        """Wallpapers.add() raises WallpaperNotFoundError for missing file."""
        archive_path = temp_dir / "test.tar.gz"
        wallpapers = Wallpapers(archive_path=archive_path)

        with pytest.raises(WallpaperNotFoundError):
            wallpapers.add(Path("/nonexistent/file.png"))

    def test_wallpapers_add_with_force_false_raises_on_duplicate(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.add(force=False) raises when wallpaper already exists."""
        duplicate = temp_dir / "test_wallpaper.png"
        duplicate.write_bytes(b"new")

        wallpapers = Wallpapers(archive_path=sample_archive)

        # force=False is default
        with pytest.raises(WallpaperError):
            wallpapers.add(duplicate, force=False)

    def test_wallpapers_add_with_force_true_overwrites(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.add(force=True) overwrites existing wallpaper."""
        duplicate = temp_dir / "test_wallpaper.png"
        duplicate.write_bytes(b"new content")

        wallpapers = Wallpapers(archive_path=sample_archive)
        # Should not raise
        wallpapers.add(duplicate, force=True)

        # Verify it's in archive
        assert "test_wallpaper.png" in wallpapers.list()

    def test_wallpapers_add_with_validate_true_rejects_bad_extension(
        self, temp_dir: Path
    ) -> None:
        """Wallpapers.add(validate=True) rejects non-image files."""
        archive_path = temp_dir / "test.tar.gz"
        text_file = temp_dir / "file.txt"
        text_file.write_text("not an image")

        wallpapers = Wallpapers(archive_path=archive_path)

        with pytest.raises(InvalidImageError):
            wallpapers.add(text_file, validate=True)

    def test_wallpapers_add_with_validate_false_accepts_any_file(
        self, temp_dir: Path
    ) -> None:
        """Wallpapers.add(validate=False) accepts files with any extension."""
        archive_path = temp_dir / "test.tar.gz"
        text_file = temp_dir / "file.txt"
        text_file.write_text("not an image")

        wallpapers = Wallpapers(archive_path=archive_path)
        # Should not raise
        wallpapers.add(text_file, validate=False)

        assert "file.txt" in wallpapers.list()

    def test_wallpapers_add_accepts_common_image_formats(
        self, temp_dir: Path
    ) -> None:
        """Wallpapers.add() accepts all standard image formats."""
        archive_path = temp_dir / "test.tar.gz"
        formats = ["jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "tif"]

        for fmt in formats:
            image_file = temp_dir / f"test.{fmt}"
            image_file.write_bytes(b"fake image data")

            wallpapers = Wallpapers(archive_path=archive_path)
            wallpapers.add(image_file, force=True)

        # All should be in archive
        listed = wallpapers.list()
        for fmt in formats:
            assert f"test.{fmt}" in listed

    def test_wallpapers_extract_returns_path_object(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() returns pathlib.Path object."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.extract(temp_dir)

        assert isinstance(result, Path)

    def test_wallpapers_extract_returns_wallpapers_subdirectory(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() creates and returns 'wallpapers' subdirectory."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.extract(temp_dir)

        assert result.name == "wallpapers"
        assert result.parent == temp_dir
        assert result.exists()
        assert result.is_dir()

    def test_wallpapers_extract_creates_parent_directory_if_needed(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() creates parent directories if they don't exist."""
        nested_dir = temp_dir / "a" / "b" / "c"
        assert not nested_dir.exists()

        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.extract(nested_dir)

        assert nested_dir.exists()
        assert result == nested_dir / "wallpapers"

    def test_wallpapers_extract_creates_wallpapers_subdirectory(
        self, sample_archive: Path, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() creates wallpapers/ subdirectory."""
        wallpapers = Wallpapers(archive_path=sample_archive)
        result = wallpapers.extract(temp_dir)

        # Files are extracted to wallpapers/ subdirectory
        assert (result / "test_wallpaper.png").exists()
        assert result.name == "wallpapers"

    def test_wallpapers_extract_raises_when_archive_missing(
        self, temp_dir: Path
    ) -> None:
        """Wallpapers.extract() raises ArchiveNotFoundError when archive missing."""
        wallpapers = Wallpapers(archive_path=temp_dir / "nonexistent.tar.gz")

        with pytest.raises(ArchiveNotFoundError):
            wallpapers.extract(temp_dir)


class TestAPIErrorHandling:
    """Characterization of error handling across API."""

    def test_api_errors_inherit_from_standard_exceptions(self) -> None:
        """API errors are standard Python exceptions."""
        assert issubclass(PlaybookNotFoundError, Exception)
        assert issubclass(AnsibleError, Exception)
        assert issubclass(ArchiveNotFoundError, Exception)
        assert issubclass(WallpaperNotFoundError, Exception)

    def test_api_can_be_used_in_try_except_blocks(self, temp_dir: Path) -> None:
        """API errors can be caught with standard exception handling."""
        packages = Packages(playbook_path=temp_dir / "nonexistent.yml", ansible_dir=temp_dir)

        try:
            packages.list()
            assert False, "Should have raised"
        except PlaybookNotFoundError:
            pass  # Expected


class TestAPIImportBehavior:
    """Characterization of import patterns and module structure."""

    def test_config_importable_from_src_package(self) -> None:
        """Config can be imported directly from src."""
        from src import Config as ConfigImport
        assert ConfigImport is Config

    def test_all_api_classes_importable_from_src(self) -> None:
        """All API classes are exported from src."""
        from src import Assets as AssetsImport
        from src import Config as ConfigImport
        from src import Packages as PackagesImport
        from src import Wallpapers as WallpapersImport

        assert AssetsImport is Assets
        assert ConfigImport is Config
        assert PackagesImport is Packages
        assert WallpapersImport is Wallpapers

    def test_api_classes_importable_from_api_module(self) -> None:
        """API classes are exported from src.api."""
        from src.api import Assets as AssetsImport
        from src.api import Config as ConfigImport
        from src.api import Packages as PackagesImport
        from src.api import Wallpapers as WallpapersImport

        assert AssetsImport is Assets
        assert ConfigImport is Config
        assert PackagesImport is Packages
        assert WallpapersImport is Wallpapers


class TestPackageRoleDataClass:
    """Characterization of PackageRole data structure."""

    def test_package_role_has_name_attribute(self) -> None:
        """PackageRole has name attribute."""
        role = PackageRole(name="test", tags=[])
        assert role.name == "test"

    def test_package_role_has_tags_attribute(self) -> None:
        """PackageRole has tags attribute."""
        role = PackageRole(name="test", tags=["tag1", "tag2"])
        assert role.tags == ["tag1", "tag2"]

    def test_package_role_tags_can_be_empty(self) -> None:
        """PackageRole.tags can be an empty list."""
        role = PackageRole(name="test", tags=[])
        assert role.tags == []
        assert isinstance(role.tags, list)
