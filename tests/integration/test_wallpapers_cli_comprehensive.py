# tests/integration/test_wallpapers_cli_comprehensive.py
"""Comprehensive integration tests for CLI edge cases and behaviors."""
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from src.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI test runner."""
    return CliRunner()


class TestAddCommandFlags:
    """Tests for add command flag combinations and behaviors."""

    def test_add_short_force_flag_works(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Add command accepts -f as shorthand for --force."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "-f", str(sample_image)]
            )

        assert result.exit_code == 0
        assert "Successfully added" in result.output

    def test_add_force_and_no_validate_together(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Add command accepts both --force and --no-validate flags."""
        # Create a non-image file with same name as existing wallpaper
        duplicate_text = temp_dir / "test_wallpaper.png"
        duplicate_text.write_text("not an image but named like one")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app,
                [
                    "assets",
                    "wallpapers",
                    "add",
                    "--force",
                    "--no-validate",
                    str(duplicate_text),
                ],
            )

        assert result.exit_code == 0


class TestListCommandOutput:
    """Tests for list command output formatting."""

    def test_list_shows_count_in_output(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """List output includes the count of wallpapers."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        # Output should show "(1)" for 1 wallpaper
        assert "(1)" in result.output

    def test_list_output_is_sorted(
        self,
        cli_runner: CliRunner,
        temp_dir: Path,
    ) -> None:
        """List displays wallpapers in sorted order."""
        # Create archive with multiple wallpapers
        import tarfile

        archive_path = temp_dir / "test.tar.gz"
        names = ["zebra.png", "apple.png", "middle.png"]

        with tarfile.open(archive_path, "w:gz") as tar:
            for name in names:
                file_path = temp_dir / name
                file_path.write_bytes(b"content")
                tar.add(file_path, arcname=name)

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=archive_path,
        ):
            result = cli_runner.invoke(app, ["assets", "wallpapers", "list"])

        assert result.exit_code == 0
        # Verify sorted order in output
        lines = result.output.strip().split("\n")
        wallpaper_lines = [line.strip() for line in lines if line.strip().startswith("-")]
        assert wallpaper_lines == ["- apple.png", "- middle.png", "- zebra.png"]


class TestExtractCommandBehavior:
    """Tests for extract command edge cases."""

    def test_extract_shows_count_in_output(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract output shows count of extracted wallpapers."""
        output_dir = temp_dir / "output"

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(output_dir)]
            )

        assert result.exit_code == 0
        assert "Extracted 1 wallpaper(s)" in result.output

    def test_extract_shows_destination_path(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Extract output shows the destination path."""
        output_dir = temp_dir / "output"

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "extract", str(output_dir)]
            )

        assert result.exit_code == 0
        assert "wallpapers" in result.output
        assert str(output_dir) in result.output or "output" in result.output


class TestErrorMessageQuality:
    """Tests for helpful error messages."""

    def test_add_nonexistent_shows_helpful_error(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
    ) -> None:
        """Add with nonexistent file shows clear error message."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", "/fake/path/image.png"]
            )

        assert result.exit_code != 0
        assert "Error" in result.output

    def test_duplicate_error_mentions_force_flag(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        sample_image: Path,
    ) -> None:
        """Duplicate error message mentions --force flag."""
        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(sample_image)]
            )

        assert result.exit_code == 1
        assert "--force" in result.output or "force" in result.output.lower()

    def test_invalid_extension_error_is_clear(
        self,
        cli_runner: CliRunner,
        sample_archive: Path,
        temp_dir: Path,
    ) -> None:
        """Invalid extension error clearly states the problem."""
        text_file = temp_dir / "document.txt"
        text_file.write_text("content")

        with patch(
            "src.commands.assets.wallpapers.get_default_archive_path",
            return_value=sample_archive,
        ):
            result = cli_runner.invoke(
                app, ["assets", "wallpapers", "add", str(text_file)]
            )

        assert result.exit_code == 1
        assert "extension" in result.output.lower()


class TestCommandArgumentValidation:
    """Tests for Typer argument validation."""

    def test_add_requires_path_argument(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Add command requires a path argument."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "add"])

        assert result.exit_code != 0
        # Typer should show usage/error about missing argument

    def test_extract_requires_path_argument(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Extract command requires a path argument."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "extract"])

        assert result.exit_code != 0
        # Typer should show usage/error about missing argument


class TestHelpMessages:
    """Tests for help message content and quality."""

    def test_add_help_describes_force_flag(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Add help shows description of --force flag."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "add", "--help"])

        assert result.exit_code == 0
        assert "--force" in result.output
        assert "overwrite" in result.output.lower()

    def test_add_help_describes_no_validate_flag(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Add help shows description of --no-validate flag."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "add", "--help"])

        assert result.exit_code == 0
        assert "--no-validate" in result.output
        assert "validation" in result.output.lower()

    def test_add_help_shows_short_flag(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Add help shows -f as short form of --force."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "add", "--help"])

        assert result.exit_code == 0
        assert "-f" in result.output

    def test_extract_help_describes_behavior(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Extract help describes what the command does."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "extract", "--help"])

        assert result.exit_code == 0
        assert "extract" in result.output.lower() or "Extract" in result.output

    def test_list_help_describes_behavior(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """List help describes what the command does."""
        result = cli_runner.invoke(app, ["assets", "wallpapers", "list", "--help"])

        assert result.exit_code == 0
        assert "list" in result.output.lower() or "List" in result.output


class TestDefaultArchivePath:
    """Tests for default archive path behavior."""

    def test_commands_use_default_archive_path_location(
        self,
        cli_runner: CliRunner,
    ) -> None:
        """Verify the default archive path is in assets/wallpapers/."""
        from src.commands.assets.wallpapers import get_default_archive_path

        default_path = get_default_archive_path()

        # Should be in the assets/wallpapers directory
        assert default_path.name == "wallpapers.tar.gz"
        assert default_path.parent.name == "wallpapers"
        assert default_path.parent.parent.name == "assets"
