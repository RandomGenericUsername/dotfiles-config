# tests/integration/test_wallpapers_cli.py
"""Integration tests for wallpapers CLI commands."""
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from src.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI test runner."""
    return CliRunner()


class TestWallpapersAddCommand:
    """Tests for 'config assets wallpapers add' command."""

    def test_add_shows_in_help(self, cli_runner: CliRunner) -> None:
        """Add command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "add" in result.output

    def test_add_wallpaper_success(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add wallpaper successfully."""
        new_image = temp_dir / "new.png"
        new_image.write_bytes(b"png content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(new_image)]
            )

        assert result.exit_code == 0
        assert "Successfully added" in result.output

    def test_add_nonexistent_file_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """Add nonexistent file shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "/nonexistent/file.png"]
            )

        assert result.exit_code != 0

    def test_add_duplicate_without_force_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Add duplicate without --force shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(sample_image)]
            )

        assert result.exit_code == 1
        assert "already exists" in result.output

    def test_add_duplicate_with_force_succeeds(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Add duplicate with --force succeeds."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "--force", str(sample_image)]
            )

        assert result.exit_code == 0
        assert "Successfully added" in result.output

    def test_add_invalid_extension_fails(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add non-image file shows error."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("text content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(text_file)]
            )

        assert result.exit_code == 1
        assert "valid image extension" in result.output

    def test_add_no_validate_allows_any_file(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add with --no-validate allows non-image files."""
        text_file = temp_dir / "readme.txt"
        text_file.write_text("text content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app,
                ["assets", "wallpapers", "add", "--no-validate", str(text_file)],
            )

        assert result.exit_code == 0


class TestWallpapersExtractCommand:
    """Tests for 'config assets wallpapers extract' command."""

    def test_extract_shows_in_help(self, cli_runner: CliRunner) -> None:
        """Extract command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "extract" in result.output

    def test_extract_creates_wallpapers_dir(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract creates wallpapers subdirectory."""
        output_dir = temp_dir / "output"
        output_dir.mkdir()

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(output_dir)]
            )

        assert result.exit_code == 0
        assert (output_dir / "wallpapers").is_dir()
        assert "Extracted" in result.output

    def test_extract_missing_archive_fails(
        self,
        cli_runner: CliRunner,
        nonexistent_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract with missing archive shows error."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=nonexistent_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(temp_dir)]
            )

        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestWallpapersListCommand:
    """Tests for 'config assets wallpapers list' command."""

    def test_list_shows_in_help(self, cli_runner: CliRunner) -> None:
        """List command appears in wallpapers help."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_list_shows_wallpapers(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """List displays wallpaper names."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        assert "test_wallpaper.png" in result.output

    def test_list_empty_archive(
        self,
        cli_runner: CliRunner,
        empty_archive: Path,
    ) -> None:
        """List shows message for empty archive."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=empty_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        assert "No wallpapers" in result.output


class TestCommandHierarchy:
    """Tests for the command hierarchy structure."""

    def test_assets_command_exists(self, cli_runner: CliRunner) -> None:
        """Assets command is registered."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "assets" in result.output

    def test_assets_wallpapers_command_exists(self, cli_runner: CliRunner) -> None:
        """Wallpapers subcommand is registered under assets."""
        result = cli_runner.invoke(app, ["assets", "--help"])
        assert result.exit_code == 0
        assert "wallpapers" in result.output

    def test_full_command_path_works(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """Full command path 'assets wallpapers list' works."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])
        assert result.exit_code == 0
