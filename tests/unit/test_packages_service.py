# tests/unit/test_packages_service.py
"""Unit tests for packages service layer."""
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from src.services.packages_service import (
    PackagesService,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
    PackageRole,
)


@pytest.fixture
def playbook_dir(temp_dir: Path) -> Path:
    """Create an ansible playbook directory structure."""
    playbook_path = temp_dir / "packages" / "ansible" / "playbooks"
    playbook_path.mkdir(parents=True)
    return playbook_path


@pytest.fixture
def sample_playbook(playbook_dir: Path) -> Path:
    """Create a sample Ansible playbook with roles."""
    playbook_content = """- name: Test Playbook
  hosts: localhost
  gather_facts: true
  roles:
    - role: nvim
      tags: [nvim]
    - role: zsh
      tags: [zsh, shell]
    - tmux
"""
    playbook_path = playbook_dir / "bootstrap.yml"
    playbook_path.write_text(playbook_content)
    return playbook_path


class TestPackagesServiceInit:
    """Tests for PackagesService initialization."""

    def test_init_with_default_paths(self, temp_dir: Path) -> None:
        """Service initializes with default paths."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            service = PackagesService()
            assert service.playbook_path == temp_dir / "packages" / "ansible" / "playbooks" / "bootstrap.yml"
            assert service.ansible_dir == temp_dir / "packages" / "ansible"

    def test_init_with_custom_playbook_path(self, sample_playbook: Path) -> None:
        """Service initializes with custom playbook path."""
        service = PackagesService(playbook_path=sample_playbook)
        assert service.playbook_path == sample_playbook

    def test_init_with_custom_ansible_dir(self, playbook_dir: Path) -> None:
        """Service initializes with custom ansible directory."""
        service = PackagesService(ansible_dir=playbook_dir.parent)
        assert service.ansible_dir == playbook_dir.parent


class TestPackagesServiceList:
    """Tests for listing packages."""

    def test_list_returns_roles_with_tags(self, sample_playbook: Path) -> None:
        """List returns roles with their tags."""
        service = PackagesService(playbook_path=sample_playbook)
        roles = service.list_packages()

        assert len(roles) == 3
        assert roles[0].name == "nvim"
        assert roles[0].tags == ["nvim"]
        assert roles[1].name == "zsh"
        assert roles[1].tags == ["zsh", "shell"]
        assert roles[2].name == "tmux"
        assert roles[2].tags == []

    def test_list_handles_role_without_tags(self, playbook_dir: Path) -> None:
        """List handles roles without tags gracefully."""
        playbook_content = """- name: Test Playbook
  hosts: localhost
  roles:
    - role: base
"""
        playbook_path = playbook_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        service = PackagesService(playbook_path=playbook_path)
        roles = service.list_packages()

        assert len(roles) == 1
        assert roles[0].name == "base"
        assert roles[0].tags == []

    def test_list_handles_string_role_format(self, playbook_dir: Path) -> None:
        """List handles simple string role format."""
        playbook_content = """- name: Test Playbook
  hosts: localhost
  roles:
    - simple_role
"""
        playbook_path = playbook_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        service = PackagesService(playbook_path=playbook_path)
        roles = service.list_packages()

        assert len(roles) == 1
        assert roles[0].name == "simple_role"
        assert roles[0].tags == []

    def test_list_handles_dict_role_format(self, playbook_dir: Path) -> None:
        """List handles dict role format with role key."""
        playbook_content = """- name: Test Playbook
  hosts: localhost
  roles:
    - role: nvim
      tags: [editor]
"""
        playbook_path = playbook_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        service = PackagesService(playbook_path=playbook_path)
        roles = service.list_packages()

        assert len(roles) == 1
        assert roles[0].name == "nvim"
        assert roles[0].tags == ["editor"]

    def test_list_raises_when_playbook_missing(self, temp_dir: Path) -> None:
        """List raises PlaybookNotFoundError when playbook doesn't exist."""
        playbook_path = temp_dir / "nonexistent.yml"
        service = PackagesService(playbook_path=playbook_path)

        with pytest.raises(PlaybookNotFoundError):
            service.list_packages()

    def test_list_handles_empty_playbook(self, playbook_dir: Path) -> None:
        """List returns empty list for playbook with no roles."""
        playbook_content = """- name: Empty Playbook
  hosts: localhost
  gather_facts: true
"""
        playbook_path = playbook_dir / "bootstrap.yml"
        playbook_path.write_text(playbook_content)

        service = PackagesService(playbook_path=playbook_path)
        roles = service.list_packages()

        assert roles == []


class TestPackagesServiceInstall:
    """Tests for installing packages."""

    def test_install_runs_ansible_playbook(self, sample_playbook: Path) -> None:
        """Install runs ansible-playbook command."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = service.install()

            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args[0][0][0] == "ansible-playbook"
            assert str(sample_playbook) in call_args[0][0][1]
            assert call_args[1]["cwd"] == ansible_dir

    def test_install_with_tags(self, sample_playbook: Path) -> None:
        """Install includes tags in command."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            service.install(tags=["nvim", "zsh"])

            call_args = mock_run.call_args[0][0]
            assert "--tags" in call_args
            tags_index = call_args.index("--tags")
            assert call_args[tags_index + 1] == "nvim,zsh"

    def test_install_with_extra_args(self, sample_playbook: Path) -> None:
        """Install includes extra arguments."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            service.install(extra_args=["--ask-become-pass", "-v"])

            call_args = mock_run.call_args[0][0]
            assert "--ask-become-pass" in call_args
            assert "-v" in call_args

    def test_install_combines_tags_and_extra_args(self, sample_playbook: Path) -> None:
        """Install combines both tags and extra arguments."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            service.install(tags=["nvim"], extra_args=["--ask-become-pass"])

            call_args = mock_run.call_args[0][0]
            assert "--tags" in call_args
            assert "--ask-become-pass" in call_args

    def test_install_raises_on_ansible_failure(self, sample_playbook: Path) -> None:
        """Install raises AnsibleError on ansible failure."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(2, "ansible-playbook")

            with pytest.raises(AnsibleError):
                service.install()

    def test_install_raises_on_ansible_not_found(self, sample_playbook: Path) -> None:
        """Install raises AnsibleNotFoundError when ansible-playbook not found."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("ansible-playbook")

            with pytest.raises(AnsibleNotFoundError):
                service.install()

    def test_install_returns_completed_process(self, sample_playbook: Path) -> None:
        """Install returns CompletedProcess from subprocess."""
        ansible_dir = sample_playbook.parent.parent
        service = PackagesService(playbook_path=sample_playbook, ansible_dir=ansible_dir)

        mock_result = MagicMock(returncode=0)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = mock_result
            result = service.install()

            assert result == mock_result
