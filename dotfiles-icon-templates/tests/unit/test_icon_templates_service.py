# tests/unit/test_icon_templates_service.py
"""Unit tests for IconTemplatesService."""
from pathlib import Path
import shutil

import pytest

from dotfiles_icon_templates.services.icon_templates_service import (
    IconTemplatesService,
    IconInfo,
    IconTemplateError,
    CategoryNotFoundError,
    IconNotFoundError,
)


class TestIconTemplatesServiceInit:
    """Tests for IconTemplatesService initialization."""

    def test_init_with_custom_path(self, tmp_path):
        """Test initialization with custom data path."""
        service = IconTemplatesService(data_dir=tmp_path)
        assert service.data_dir == tmp_path


class TestIconTemplatesServiceCategories:
    """Tests for categories method."""

    def test_categories_with_dirs(self, tmp_path):
        """Test listing categories."""
        (tmp_path / "cat1").mkdir()
        (tmp_path / "cat2").mkdir()
        (tmp_path / ".hidden").mkdir()
        
        service = IconTemplatesService(data_dir=tmp_path)
        categories = service.categories()
        
        assert len(categories) == 2
        assert "cat1" in categories
        assert "cat2" in categories
        assert ".hidden" not in categories

    def test_categories_no_data_dir(self, tmp_path):
        """Test categories when data dir doesn't exist."""
        nonexistent = tmp_path / "nonexistent"
        service = IconTemplatesService(data_dir=nonexistent)
        
        with pytest.raises(IconTemplateError):
            service.categories()

    def test_categories_empty(self, tmp_path):
        """Test categories with empty data directory."""
        service = IconTemplatesService(data_dir=tmp_path)
        categories = service.categories()
        assert categories == []


class TestIconTemplatesServiceList:
    """Tests for list method."""

    def test_list_all_icons(self, tmp_path):
        """Test listing all icons."""
        (tmp_path / "cat1").mkdir()
        (tmp_path / "cat1" / "icon1.svg").write_text("svg")
        (tmp_path / "cat1" / "icon2.svg").write_text("svg")
        (tmp_path / "cat2").mkdir()
        (tmp_path / "cat2" / "icon3.svg").write_text("svg")
        
        service = IconTemplatesService(data_dir=tmp_path)
        icons = service.list()
        
        assert len(icons) == 3
        assert "icon1.svg" in icons
        assert "icon2.svg" in icons
        assert "icon3.svg" in icons

    def test_list_by_category(self, tmp_path):
        """Test listing icons in category."""
        (tmp_path / "cat1").mkdir()
        (tmp_path / "cat1" / "icon1.svg").write_text("svg")
        (tmp_path / "cat1" / "icon2.svg").write_text("svg")
        (tmp_path / "cat2").mkdir()
        (tmp_path / "cat2" / "icon3.svg").write_text("svg")
        
        service = IconTemplatesService(data_dir=tmp_path)
        icons = service.list(category="cat1")
        
        assert len(icons) == 2
        assert "icon1.svg" in icons
        assert "icon2.svg" in icons
        assert "icon3.svg" not in icons

    def test_list_category_not_found(self, tmp_path):
        """Test list with non-existent category."""
        (tmp_path / "cat1").mkdir()
        
        service = IconTemplatesService(data_dir=tmp_path)
        
        with pytest.raises(CategoryNotFoundError):
            service.list(category="nonexistent")

    def test_list_excludes_hidden_files(self, tmp_path):
        """Test list excludes hidden files."""
        (tmp_path / "cat1").mkdir()
        (tmp_path / "cat1" / "icon.svg").write_text("svg")
        (tmp_path / "cat1" / ".hidden.svg").write_text("svg")
        
        service = IconTemplatesService(data_dir=tmp_path)
        icons = service.list(category="cat1")
        
        assert len(icons) == 1
        assert "icon.svg" in icons


class TestIconTemplatesServiceShow:
    """Tests for show method."""

    def test_show_icon_found(self, tmp_path):
        """Test showing icon details."""
        (tmp_path / "cat1").mkdir()
        icon_path = tmp_path / "cat1" / "icon.svg"
        icon_path.write_text("svg")
        
        service = IconTemplatesService(data_dir=tmp_path)
        info = service.show("icon.svg")
        
        assert info.name == "icon.svg"
        assert info.category == "cat1"
        assert info.path == icon_path

    def test_show_icon_not_found(self, tmp_path):
        """Test showing non-existent icon."""
        (tmp_path / "cat1").mkdir()
        
        service = IconTemplatesService(data_dir=tmp_path)
        
        with pytest.raises(IconNotFoundError):
            service.show("nonexistent.svg")

    def test_show_data_dir_not_found(self, tmp_path):
        """Test show when data dir doesn't exist."""
        nonexistent = tmp_path / "nonexistent"
        service = IconTemplatesService(data_dir=nonexistent)
        
        with pytest.raises(IconTemplateError):
            service.show("icon.svg")


class TestIconTemplatesServiceCopy:
    """Tests for copy method."""

    def test_copy_all_icons(self, tmp_path):
        """Test copying all icons."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        (src_dir / "cat1" / "icon1.svg").write_text("svg1")
        (src_dir / "cat2").mkdir(parents=True)
        (src_dir / "cat2" / "icon2.svg").write_text("svg2")
        
        dest_dir = tmp_path / "dest"
        
        service = IconTemplatesService(data_dir=src_dir)
        copied = service.copy(dest_dir)
        
        assert len(copied) == 2
        assert "icon1.svg" in copied
        assert "icon2.svg" in copied
        assert (dest_dir / "icon1.svg").exists()
        assert (dest_dir / "icon2.svg").exists()

    def test_copy_by_category(self, tmp_path):
        """Test copying icons from category."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        (src_dir / "cat1" / "icon1.svg").write_text("svg1")
        (src_dir / "cat2").mkdir(parents=True)
        (src_dir / "cat2" / "icon2.svg").write_text("svg2")
        
        dest_dir = tmp_path / "dest"
        
        service = IconTemplatesService(data_dir=src_dir)
        copied = service.copy(dest_dir, category="cat1")
        
        assert len(copied) == 1
        assert "icon1.svg" in copied
        assert (dest_dir / "icon1.svg").exists()
        assert not (dest_dir / "icon2.svg").exists()

    def test_copy_specific_icons(self, tmp_path):
        """Test copying specific icons."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        (src_dir / "cat1" / "icon1.svg").write_text("svg1")
        (src_dir / "cat1" / "icon2.svg").write_text("svg2")
        
        dest_dir = tmp_path / "dest"
        
        service = IconTemplatesService(data_dir=src_dir)
        copied = service.copy(dest_dir, icons=["icon1.svg"])
        
        assert len(copied) == 1
        assert "icon1.svg" in copied
        assert (dest_dir / "icon1.svg").exists()
        assert not (dest_dir / "icon2.svg").exists()

    def test_copy_creates_dest_dir(self, tmp_path):
        """Test copy creates destination directory."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        (src_dir / "cat1" / "icon1.svg").write_text("svg1")
        
        dest_dir = tmp_path / "dest" / "nested"
        assert not dest_dir.exists()
        
        service = IconTemplatesService(data_dir=src_dir)
        service.copy(dest_dir)
        
        assert dest_dir.exists()

    def test_copy_icon_not_found(self, tmp_path):
        """Test copy with non-existent specific icon."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        (src_dir / "cat1" / "icon1.svg").write_text("svg1")
        
        dest_dir = tmp_path / "dest"
        
        service = IconTemplatesService(data_dir=src_dir)
        
        with pytest.raises(IconNotFoundError):
            service.copy(dest_dir, icons=["nonexistent.svg"])

    def test_copy_category_not_found(self, tmp_path):
        """Test copy with non-existent category."""
        src_dir = tmp_path / "src"
        (src_dir / "cat1").mkdir(parents=True)
        
        dest_dir = tmp_path / "dest"
        
        service = IconTemplatesService(data_dir=src_dir)
        
        with pytest.raises(CategoryNotFoundError):
            service.copy(dest_dir, category="nonexistent")
