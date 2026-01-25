# tests/integration/test_icon_templates_cli.py
"""Integration tests for IconTemplates CLI."""
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dotfiles_icon_templates.cli import app
from dotfiles_icon_templates.services.icon_templates_service import IconTemplatesService


runner = CliRunner()


@pytest.fixture
def data_with_icons(tmp_path):
    """Create temporary data directory with test icons."""
    (tmp_path / "screenshot-tool").mkdir()
    (tmp_path / "screenshot-tool" / "screenshot.svg").write_text("<svg></svg>")
    
    (tmp_path / "status-bar").mkdir()
    (tmp_path / "status-bar" / "battery.svg").write_text("<svg></svg>")
    (tmp_path / "status-bar" / "network.svg").write_text("<svg></svg>")
    
    (tmp_path / "wlogout").mkdir()
    (tmp_path / "wlogout" / "shutdown.svg").write_text("<svg></svg>")
    
    return tmp_path


class TestIconTemplatesListCommand:
    """Tests for icon templates list command."""

    def test_list_all(self, data_with_icons, monkeypatch):
        """Test listing all icons."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        result = runner.invoke(app, ["list"])
        
        assert result.exit_code == 0
        assert "screenshot.svg" in result.stdout
        assert "battery.svg" in result.stdout
        assert "network.svg" in result.stdout
        assert "shutdown.svg" in result.stdout

    def test_list_by_category(self, data_with_icons, monkeypatch):
        """Test listing icons in specific category."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        result = runner.invoke(app, ["list", "--category", "status-bar"])
        
        assert result.exit_code == 0
        assert "battery.svg" in result.stdout
        assert "network.svg" in result.stdout
        assert "screenshot.svg" not in result.stdout
        assert "shutdown.svg" not in result.stdout

    def test_list_category_not_found(self, data_with_icons, monkeypatch):
        """Test list with non-existent category."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        result = runner.invoke(app, ["list", "--category", "nonexistent"])
        
        assert result.exit_code != 0
        assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()

    def test_list_help(self):
        """Test list command help."""
        result = runner.invoke(app, ["list", "--help"])
        
        assert result.exit_code == 0
        assert "--category" in result.stdout


class TestIconTemplatesCopyCommand:
    """Tests for icon templates copy command."""

    def test_copy_all(self, data_with_icons, tmp_path, monkeypatch):
        """Test copying all icons."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        dest = tmp_path / "output"
        
        result = runner.invoke(app, ["copy", str(dest)])
        
        assert result.exit_code == 0
        assert (dest / "screenshot.svg").exists()
        assert (dest / "battery.svg").exists()

    def test_copy_by_category(self, data_with_icons, tmp_path, monkeypatch):
        """Test copying icons from category."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        dest = tmp_path / "output"
        
        result = runner.invoke(app, ["copy", str(dest), "--category", "status-bar"])
        
        assert result.exit_code == 0
        assert (dest / "battery.svg").exists()
        assert (dest / "network.svg").exists()
        assert not (dest / "screenshot.svg").exists()

    def test_copy_with_icons_filter(self, data_with_icons, tmp_path, monkeypatch):
        """Test copying specific icons."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        dest = tmp_path / "output"
        
        result = runner.invoke(
            app,
            ["copy", str(dest), "--icons", "battery.svg", "--icons", "shutdown.svg"]
        )
        
        assert result.exit_code == 0
        assert (dest / "battery.svg").exists()
        assert (dest / "shutdown.svg").exists()
        assert not (dest / "screenshot.svg").exists()

    def test_copy_icon_not_found(self, data_with_icons, tmp_path, monkeypatch):
        """Test copy with non-existent icon."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        dest = tmp_path / "output"
        
        result = runner.invoke(app, ["copy", str(dest), "--icons", "nonexistent.svg"])
        
        assert result.exit_code != 0
        assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()

    def test_copy_help(self):
        """Test copy command help."""
        result = runner.invoke(app, ["copy", "--help"])
        
        assert result.exit_code == 0
        assert "--category" in result.stdout
        assert "--icons" in result.stdout


class TestIconTemplatesShowCommand:
    """Tests for icon templates show command."""

    def test_show_icon(self, data_with_icons, monkeypatch):
        """Test showing icon information."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        result = runner.invoke(app, ["show", "battery.svg"])
        
        assert result.exit_code == 0
        assert "battery.svg" in result.stdout
        assert "status-bar" in result.stdout

    def test_show_icon_not_found(self, data_with_icons, monkeypatch):
        """Test showing non-existent icon."""
        monkeypatch.setattr(
            IconTemplatesService,
            '__init__',
            lambda self, **kwargs: setattr(self, 'data_dir', data_with_icons) or None
        )
        
        result = runner.invoke(app, ["show", "nonexistent.svg"])
        
        assert result.exit_code != 0
        assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()

    def test_show_help(self):
        """Test show command help."""
        result = runner.invoke(app, ["show", "--help"])
        
        assert result.exit_code == 0


class TestIconTemplatesRootCommand:
    """Tests for root icon templates command."""

    def test_root_help(self):
        """Test root help shows all commands."""
        result = runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "list" in result.stdout
        assert "copy" in result.stdout
        assert "show" in result.stdout
