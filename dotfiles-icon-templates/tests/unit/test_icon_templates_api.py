# tests/unit/test_icon_templates_api.py
"""Unit tests for IconTemplates API."""
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from dotfiles_icon_templates.api.icon_templates import IconTemplates
from dotfiles_icon_templates.services.icon_templates_service import IconInfo


class TestIconTemplatesAPI:
    """Tests for IconTemplates API class."""

    def test_initialization(self):
        """Test IconTemplates initialization."""
        icons = IconTemplates()
        assert icons._service is not None

    def test_initialization_custom_path(self, tmp_path):
        """Test initialization with custom path."""
        icons = IconTemplates(data_dir=tmp_path)
        assert icons._service.data_dir == tmp_path

    def test_categories_delegates(self):
        """Test categories method delegates to service."""
        icons = IconTemplates()
        
        with patch.object(icons._service, 'categories', return_value=['cat1', 'cat2']):
            result = icons.categories()
            
            assert result == ['cat1', 'cat2']

    def test_list_delegates(self):
        """Test list method delegates to service."""
        icons = IconTemplates()
        
        with patch.object(icons._service, 'list', return_value=['icon1.svg', 'icon2.svg']):
            result = icons.list()
            
            assert result == ['icon1.svg', 'icon2.svg']

    def test_list_with_category(self):
        """Test list with category filter."""
        icons = IconTemplates()
        
        with patch.object(icons._service, 'list', return_value=['icon1.svg']):
            result = icons.list(category='cat1')
            
            assert result == ['icon1.svg']
            icons._service.list.assert_called_once_with('cat1')

    def test_show_delegates(self, tmp_path):
        """Test show method delegates to service."""
        icons = IconTemplates()
        icon_info = IconInfo(name='icon.svg', category='cat1', path=tmp_path / 'icon.svg')
        
        with patch.object(icons._service, 'show', return_value=icon_info):
            result = icons.show('icon.svg')
            
            assert result == icon_info

    def test_copy_delegates(self, tmp_path):
        """Test copy method delegates to service."""
        icons = IconTemplates()
        dest = tmp_path / 'dest'
        
        with patch.object(icons._service, 'copy', return_value=['icon1.svg']):
            result = icons.copy(dest)
            
            assert result == ['icon1.svg']

    def test_copy_with_filters(self, tmp_path):
        """Test copy with category and icons filters."""
        icons = IconTemplates()
        dest = tmp_path / 'dest'
        
        with patch.object(icons._service, 'copy', return_value=['icon1.svg']):
            result = icons.copy(dest, category='cat1', icons=['icon1.svg'])
            
            assert result == ['icon1.svg']
            icons._service.copy.assert_called_once()
