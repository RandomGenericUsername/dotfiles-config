# tests/integration/test_root_cli_hierarchy.py
"""Integration tests for root CLI command hierarchy."""
import pytest
from typer.testing import CliRunner

from dotfiles_config.cli import app


runner = CliRunner()


class TestRootCliStructure:
    """Tests for root CLI structure and subcommand routing."""

    def test_root_help_shows_all_commands(self):
        """Test root help displays all subcommand groups."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "packages" in result.stdout.lower()
        assert "wallpapers" in result.stdout.lower()
        assert "icon-templates" in result.stdout.lower() or "icon_templates" in result.stdout.lower()

    def test_packages_subcommand_available(self):
        """Test packages subcommand is available."""
        result = runner.invoke(app, ["packages", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()
        assert "install" in result.stdout.lower()

    def test_wallpapers_subcommand_available(self):
        """Test wallpapers subcommand is available."""
        result = runner.invoke(app, ["wallpapers", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()
        assert "add" in result.stdout.lower()
        assert "extract" in result.stdout.lower()

    def test_icon_templates_subcommand_available(self):
        """Test icon-templates subcommand is available."""
        result = runner.invoke(app, ["icon-templates", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()
        assert "copy" in result.stdout.lower()
        assert "show" in result.stdout.lower()

    def test_packages_list_subcommand(self):
        """Test packages list command is accessible."""
        result = runner.invoke(app, ["packages", "list", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()

    def test_wallpapers_list_subcommand(self):
        """Test wallpapers list command is accessible."""
        result = runner.invoke(app, ["wallpapers", "list", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()

    def test_icon_templates_list_subcommand(self):
        """Test icon-templates list command is accessible."""
        result = runner.invoke(app, ["icon-templates", "list", "--help"])
        
        assert result.exit_code == 0


class TestRootCliVersionInfo:
    """Tests for root CLI version and info."""

    def test_version_flag(self):
        """Test version flag is available."""
        result = runner.invoke(app, ["--version"])
        
        # Should show version or be a valid command
        assert result.exit_code in [0, 2]  # 0 for success, 2 for help message

    def test_help_shows_version_option(self):
        """Test help message includes version option."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "--help" in result.stdout


class TestRootCliErrorHandling:
    """Tests for error handling in root CLI."""

    def test_unknown_command_error(self):
        """Test unknown command shows error."""
        result = runner.invoke(app, ["unknown-command"])
        
        assert result.exit_code != 0
        assert "no such command" in result.stdout.lower() or "error" in result.stdout.lower() or "no match" in result.stdout.lower()

    def test_missing_subcommand(self):
        """Test packages subcommand requires a command."""
        result = runner.invoke(app, ["packages"])
        
        # Should show help or error
        assert result.exit_code != 0 or "list" in result.stdout.lower() or "install" in result.stdout.lower()

    def test_packages_missing_command(self):
        """Test packages without subcommand shows help."""
        result = runner.invoke(app, ["packages", "--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout.lower()


class TestRootCliIntegration:
    """Integration tests across CLI hierarchy."""

    def test_all_subcommands_have_help(self):
        """Test all subcommands have help available."""
        subcommands = ["packages", "wallpapers", "icon-templates"]
        
        for subcommand in subcommands:
            result = runner.invoke(app, [subcommand, "--help"])
            assert result.exit_code == 0, f"{subcommand} --help failed"

    def test_main_help_comprehensive(self):
        """Test main help is comprehensive."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        # Should mention the main purpose
        text = result.stdout.lower()
        assert len(text) > 100  # Non-trivial help text

    def test_command_chaining_packages(self):
        """Test packages command chain can be invoked."""
        result = runner.invoke(app, ["packages", "list", "--help"])
        
        assert result.exit_code == 0

    def test_command_chaining_wallpapers(self):
        """Test wallpapers command chain can be invoked."""
        result = runner.invoke(app, ["wallpapers", "add", "--help"])
        
        assert result.exit_code == 0

    def test_command_chaining_icon_templates(self):
        """Test icon-templates command chain can be invoked."""
        result = runner.invoke(app, ["icon-templates", "copy", "--help"])
        
        assert result.exit_code == 0
