# tests/integration/test_packages_cli.py
"""Integration tests for packages CLI commands."""
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from src.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_playbook(temp_dir: Path) -> Path:
    """Create a sample Ansible playbook for testing."""
    playbook_content = """- name: Test Playbook
  hosts: localhost
  gather_facts: true

  pre_tasks:
    - name: Debug paths
      ansible.builtin.debug:
        msg: "Testing"
      tags: [debug]

  roles:
    - role: nvim
      tags: [nvim]
    - role: zsh
      tags: [zsh, shell]
    - role: tmux
"""
    playbook_path = temp_dir / "bootstrap.yml"
    playbook_path.write_text(playbook_content)
    return playbook_path


class TestPackagesInstallCommand:
    """Tests for 'config packages install' command."""

    def test_install_shows_in_help(self, cli_runner: CliRunner) -> None:
        """Install command appears in packages help."""
        result = cli_runner.invoke(app, ["packages", "--help"])
        assert result.exit_code == 0
        assert "install" in result.output

    def test_install_command_builds_correct_ansible_command(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Install command builds correct ansible-playbook command."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            # Change to temp_dir so the Path.cwd() logic works
            with patch("pathlib.Path.cwd", return_value=temp_dir):
                # Create minimal ansible directory structure
                ansible_dir = temp_dir / "packages" / "ansible"
                playbook_dir = ansible_dir / "playbooks"
                playbook_dir.mkdir(parents=True)
                playbook_path = playbook_dir / "bootstrap.yml"
                playbook_path.write_text("---\n- hosts: localhost\n")

                result = cli_runner.invoke(app, ["packages", "install"])

            assert result.exit_code == 0
            assert mock_run.called
            call_args = mock_run.call_args
            assert call_args[0][0][0] == "ansible-playbook"
            assert "bootstrap.yml" in call_args[0][0][1]
            assert call_args[1]["cwd"] == ansible_dir

    def test_install_with_tags_option(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Install command accepts --tags option."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            with patch("pathlib.Path.cwd", return_value=temp_dir):
                ansible_dir = temp_dir / "packages" / "ansible"
                playbook_dir = ansible_dir / "playbooks"
                playbook_dir.mkdir(parents=True)
                playbook_path = playbook_dir / "bootstrap.yml"
                playbook_path.write_text("---\n- hosts: localhost\n")

                result = cli_runner.invoke(
                    app, ["packages", "install", "--tags", "nvim", "--tags", "zsh"]
                )

            assert result.exit_code == 0
            assert mock_run.called
            call_args = mock_run.call_args[0][0]
            assert "--tags" in call_args
            # Tags should be joined with comma
            tags_index = call_args.index("--tags")
            assert call_args[tags_index + 1] == "nvim,zsh"

    def test_install_forwards_extra_args(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Install command forwards extra arguments to ansible-playbook."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            with patch("pathlib.Path.cwd", return_value=temp_dir):
                ansible_dir = temp_dir / "packages" / "ansible"
                playbook_dir = ansible_dir / "playbooks"
                playbook_dir.mkdir(parents=True)
                playbook_path = playbook_dir / "bootstrap.yml"
                playbook_path.write_text("---\n- hosts: localhost\n")

                result = cli_runner.invoke(
                    app,
                    ["packages", "install", "--", "--ask-become-pass", "-v"],
                )

            assert result.exit_code == 0
            assert mock_run.called
            call_args = mock_run.call_args[0][0]
            assert "--ask-become-pass" in call_args
            assert "-v" in call_args

    def test_install_handles_ansible_failure(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Install command handles ansible-playbook failures."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(2, "ansible-playbook")

            with patch("pathlib.Path.cwd", return_value=temp_dir):
                ansible_dir = temp_dir / "packages" / "ansible"
                playbook_dir = ansible_dir / "playbooks"
                playbook_dir.mkdir(parents=True)
                playbook_path = playbook_dir / "bootstrap.yml"
                playbook_path.write_text("---\n- hosts: localhost\n")

                result = cli_runner.invoke(app, ["packages", "install"])

            assert result.exit_code == 2
            assert "Error running ansible-playbook" in result.output

    def test_install_handles_missing_ansible(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """Install command handles missing ansible-playbook command."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("ansible-playbook")

            with patch("pathlib.Path.cwd", return_value=temp_dir):
                ansible_dir = temp_dir / "packages" / "ansible"
                playbook_dir = ansible_dir / "playbooks"
                playbook_dir.mkdir(parents=True)
                playbook_path = playbook_dir / "bootstrap.yml"
                playbook_path.write_text("---\n- hosts: localhost\n")

                result = cli_runner.invoke(app, ["packages", "install"])

            assert result.exit_code == 1
            assert "ansible-playbook command not found" in result.output


class TestPackagesListCommand:
    """Tests for 'config packages list' command."""

    def test_list_shows_in_help(self, cli_runner: CliRunner) -> None:
        """List command appears in packages help."""
        result = cli_runner.invoke(app, ["packages", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_list_displays_roles_and_tags(
        self, cli_runner: CliRunner, temp_dir: Path, sample_playbook: Path
    ) -> None:
        """List command displays roles with their tags."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            ansible_dir = temp_dir / "packages" / "ansible"
            playbook_dir = ansible_dir / "playbooks"
            playbook_dir.mkdir(parents=True)
            # Move sample playbook to expected location
            target_playbook = playbook_dir / "bootstrap.yml"
            target_playbook.write_text(sample_playbook.read_text())

            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 0
        assert "nvim" in result.output
        assert "zsh" in result.output
        assert "tmux" in result.output
        assert "[nvim]" in result.output
        assert "[zsh, shell]" in result.output

    def test_list_handles_missing_playbook(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """List command handles missing playbook gracefully."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            # Don't create the playbook file
            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_list_handles_empty_playbook(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """List command handles playbook with no roles."""
        playbook_content = """- name: Empty Playbook
  hosts: localhost
  gather_facts: true
"""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            ansible_dir = temp_dir / "packages" / "ansible"
            playbook_dir = ansible_dir / "playbooks"
            playbook_dir.mkdir(parents=True)
            playbook_path = playbook_dir / "bootstrap.yml"
            playbook_path.write_text(playbook_content)

            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 0
        assert "No roles found" in result.output

    def test_list_shows_usage_hint(
        self, cli_runner: CliRunner, temp_dir: Path, sample_playbook: Path
    ) -> None:
        """List command shows usage hint at the end."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            ansible_dir = temp_dir / "packages" / "ansible"
            playbook_dir = ansible_dir / "playbooks"
            playbook_dir.mkdir(parents=True)
            target_playbook = playbook_dir / "bootstrap.yml"
            target_playbook.write_text(sample_playbook.read_text())

            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 0
        assert "Usage:" in result.output
        assert "config packages install" in result.output


class TestCommandHierarchy:
    """Tests for the command hierarchy structure."""

    def test_packages_command_exists(self, cli_runner: CliRunner) -> None:
        """Packages command is registered."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "packages" in result.output

    def test_packages_has_description(self, cli_runner: CliRunner) -> None:
        """Packages command has help description."""
        result = cli_runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Manage system packages" in result.output

    def test_packages_subcommands_exist(self, cli_runner: CliRunner) -> None:
        """Packages has install and list subcommands."""
        result = cli_runner.invoke(app, ["packages", "--help"])
        assert result.exit_code == 0
        assert "install" in result.output
        assert "list" in result.output

    def test_old_install_packages_command_removed(
        self, cli_runner: CliRunner
    ) -> None:
        """Old 'install-packages' command is no longer available."""
        result = cli_runner.invoke(app, ["install-packages"])
        assert result.exit_code != 0
        assert "No such command" in result.output


class TestPackagesListRoleFormats:
    """Tests for different role format handling in list command."""

    def test_list_handles_string_roles(
        self, cli_runner: CliRunner, temp_dir: Path
    ) -> None:
        """List command handles simple string role format."""
        playbook_content = """- name: Test Playbook
  hosts: localhost
  roles:
    - simple_role
"""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            ansible_dir = temp_dir / "packages" / "ansible"
            playbook_dir = ansible_dir / "playbooks"
            playbook_dir.mkdir(parents=True)
            playbook_path = playbook_dir / "bootstrap.yml"
            playbook_path.write_text(playbook_content)

            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 0
        assert "simple_role" in result.output
        assert "[no tags]" in result.output

    def test_list_shows_total_count(
        self, cli_runner: CliRunner, temp_dir: Path, sample_playbook: Path
    ) -> None:
        """List command shows total count of roles."""
        with patch("pathlib.Path.cwd", return_value=temp_dir):
            ansible_dir = temp_dir / "packages" / "ansible"
            playbook_dir = ansible_dir / "playbooks"
            playbook_dir.mkdir(parents=True)
            target_playbook = playbook_dir / "bootstrap.yml"
            target_playbook.write_text(sample_playbook.read_text())

            result = cli_runner.invoke(app, ["packages", "list"])

        assert result.exit_code == 0
        assert "Total: 3 role(s)" in result.output
