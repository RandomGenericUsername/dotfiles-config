# Test Plan

> **Document ID**: TP-001  
> **Version**: 1.0  
> **Date**: 2026-01-24  
> **Status**: Draft  
> **Source**: [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

---

## 1. Introduction

### 1.1 Purpose

This document defines the test strategy, test cases, and acceptance criteria for the dotfiles-config refactoring project. Tests serve as the specification and foundational truth for the system behavior.

### 1.2 Scope

- Unit tests for all service and API layers
- Integration tests for all CLI commands
- End-to-end tests for the root wrapper

### 1.3 Test Principles

1. **Tests as Specification**: Tests define expected behavior
2. **Isolation**: Unit tests don't touch filesystem/network (use mocks)
3. **Integration Reality**: Integration tests use real files in temp directories
4. **Deterministic**: Tests produce same results on every run
5. **Fast**: Unit tests complete in milliseconds
6. **Independent**: Tests don't depend on each other

---

## 2. Test Environment

### 2.1 Tools

| Tool | Purpose |
|------|---------|
| pytest | Test framework |
| pytest-cov | Coverage reporting |
| unittest.mock | Mocking |
| tempfile | Temporary directories |
| typer.testing.CliRunner | CLI testing |

### 2.2 Directory Structure

```
<project>/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_<name>_service.py
│   └── test_<name>_api.py
└── integration/
    ├── __init__.py
    └── test_<name>_cli.py
```

### 2.3 Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=term-missing

# Specific project
uv run pytest dotfiles-packages/tests/

# Only unit tests
uv run pytest -k "unit"

# Only integration tests
uv run pytest -k "integration"
```

---

## 3. Shared Fixtures

### 3.1 Common Fixtures (conftest.py)

```python
# conftest.py
import pytest
from pathlib import Path
import tempfile
import tarfile
import shutil


@pytest.fixture
def temp_dir():
    """Provide a temporary directory that's cleaned up after test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_image(temp_dir):
    """Create a sample image file for testing."""
    image_path = temp_dir / "sample.jpg"
    image_path.write_bytes(b"fake image content")
    return image_path


@pytest.fixture
def sample_archive(temp_dir):
    """Create a sample tar.gz archive with wallpapers."""
    archive_path = temp_dir / "wallpapers.tar.gz"
    
    # Create some fake wallpapers
    wallpapers_dir = temp_dir / "wallpapers_content"
    wallpapers_dir.mkdir()
    (wallpapers_dir / "bg1.jpg").write_bytes(b"image1")
    (wallpapers_dir / "bg2.png").write_bytes(b"image2")
    
    # Create archive
    with tarfile.open(archive_path, "w:gz") as tar:
        for f in wallpapers_dir.iterdir():
            tar.add(f, arcname=f.name)
    
    return archive_path


@pytest.fixture
def empty_archive(temp_dir):
    """Create an empty tar.gz archive."""
    archive_path = temp_dir / "empty.tar.gz"
    with tarfile.open(archive_path, "w:gz"):
        pass
    return archive_path


@pytest.fixture
def sample_playbook(temp_dir):
    """Create a sample Ansible playbook."""
    playbook_path = temp_dir / "bootstrap.yml"
    playbook_content = """
- hosts: localhost
  roles:
    - role: nvim
      tags: [nvim]
    - role: zsh
      tags: [zsh, shell]
    - role: docker
      tags: [docker]
"""
    playbook_path.write_text(playbook_content)
    return playbook_path


@pytest.fixture
def sample_icons_dir(temp_dir):
    """Create sample icon template directory structure."""
    data_dir = temp_dir / "data"
    
    # Create categories
    (data_dir / "screenshot-tool").mkdir(parents=True)
    (data_dir / "status-bar").mkdir(parents=True)
    (data_dir / "wlogout").mkdir(parents=True)
    
    # Create sample icons
    (data_dir / "screenshot-tool" / "capture.svg").write_text("<svg/>")
    (data_dir / "status-bar" / "battery.svg").write_text("<svg/>")
    (data_dir / "status-bar" / "wifi.svg").write_text("<svg/>")
    (data_dir / "wlogout" / "lock.svg").write_text("<svg/>")
    
    return data_dir
```

---

## 4. Packages Module Tests

### 4.1 Unit Tests - Service Layer

**File**: `dotfiles-packages/tests/unit/test_packages_service.py`

#### TC-PKG-SVC-001: List packages returns roles from playbook

```python
def test_list_packages_returns_roles_from_playbook(sample_playbook):
    """Service should parse playbook and return roles with tags."""
    service = PackagesService(playbook_path=sample_playbook)
    
    roles = service.list_packages()
    
    assert len(roles) == 3
    assert roles[0].name == "nvim"
    assert roles[0].tags == ["nvim"]
    assert roles[1].name == "zsh"
    assert roles[1].tags == ["zsh", "shell"]
```

#### TC-PKG-SVC-002: List packages raises when playbook not found

```python
def test_list_packages_raises_when_playbook_not_found(temp_dir):
    """Service should raise PlaybookNotFoundError for missing playbook."""
    service = PackagesService(playbook_path=temp_dir / "missing.yml")
    
    with pytest.raises(PlaybookNotFoundError):
        service.list_packages()
```

#### TC-PKG-SVC-003: List packages handles empty playbook

```python
def test_list_packages_handles_empty_playbook(temp_dir):
    """Service should return empty list for playbook with no roles."""
    playbook = temp_dir / "empty.yml"
    playbook.write_text("- hosts: localhost\n")
    service = PackagesService(playbook_path=playbook)
    
    roles = service.list_packages()
    
    assert roles == []
```

#### TC-PKG-SVC-004: Install constructs correct command

```python
def test_install_constructs_correct_command(mocker, sample_playbook):
    """Service should construct correct ansible-playbook command."""
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = MagicMock(returncode=0)
    
    service = PackagesService(playbook_path=sample_playbook)
    service.install(tags=["nvim", "zsh"])
    
    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert "ansible-playbook" in call_args
    assert "--tags" in call_args
    assert "nvim,zsh" in call_args
```

#### TC-PKG-SVC-005: Install raises when ansible not found

```python
def test_install_raises_when_ansible_not_found(mocker, sample_playbook):
    """Service should raise AnsibleNotFoundError when ansible missing."""
    mocker.patch("subprocess.run", side_effect=FileNotFoundError())
    
    service = PackagesService(playbook_path=sample_playbook)
    
    with pytest.raises(AnsibleNotFoundError):
        service.install(tags=["nvim"])
```

#### TC-PKG-SVC-006: Install raises on ansible failure

```python
def test_install_raises_on_ansible_failure(mocker, sample_playbook):
    """Service should raise AnsibleError with return code on failure."""
    from subprocess import CalledProcessError
    mocker.patch("subprocess.run", side_effect=CalledProcessError(2, "cmd"))
    
    service = PackagesService(playbook_path=sample_playbook)
    
    with pytest.raises(AnsibleError) as exc_info:
        service.install(tags=["nvim"])
    
    assert exc_info.value.return_code == 2
```

### 4.2 Unit Tests - API Layer

**File**: `dotfiles-packages/tests/unit/test_packages_api.py`

#### TC-PKG-API-001: API wraps service correctly

```python
def test_packages_api_wraps_service(mocker, sample_playbook):
    """Packages API should delegate to service."""
    mock_service = mocker.patch.object(PackagesService, "list_packages")
    mock_service.return_value = [PackageRole("test", ["tag"])]
    
    packages = Packages(playbook_path=sample_playbook)
    result = packages.list()
    
    assert len(result) == 1
    mock_service.assert_called_once()
```

### 4.3 Integration Tests - CLI

**File**: `dotfiles-packages/tests/integration/test_packages_cli.py`

#### TC-PKG-CLI-001: List command outputs roles

```python
def test_list_command_outputs_roles(sample_playbook, monkeypatch):
    """List command should display roles from playbook."""
    monkeypatch.chdir(sample_playbook.parent)
    runner = CliRunner()
    
    result = runner.invoke(app, ["list"])
    
    assert result.exit_code == 0
    assert "nvim" in result.output
    assert "zsh" in result.output
```

#### TC-PKG-CLI-002: Install command passes tags

```python
def test_install_command_passes_tags(mocker, sample_playbook, monkeypatch):
    """Install command should pass tags to ansible-playbook."""
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value = MagicMock(returncode=0)
    monkeypatch.chdir(sample_playbook.parent)
    runner = CliRunner()
    
    result = runner.invoke(app, ["install", "--tags", "nvim"])
    
    assert result.exit_code == 0
    assert "--tags" in str(mock_run.call_args)
```

#### TC-PKG-CLI-003: List command exits 1 on error

```python
def test_list_command_exits_1_on_error(temp_dir, monkeypatch):
    """List command should exit with code 1 on error."""
    monkeypatch.chdir(temp_dir)
    runner = CliRunner()
    
    result = runner.invoke(app, ["list"])
    
    assert result.exit_code == 1
    assert "Error" in result.output
```

---

## 5. Wallpapers Module Tests

### 5.1 Unit Tests - Service Layer

**File**: `dotfiles-wallpapers/tests/unit/test_wallpapers_service.py`

#### TC-WP-SVC-001: List wallpapers returns files from archive

```python
def test_list_wallpapers_returns_files_from_archive(sample_archive):
    """Service should list all files in the archive."""
    service = WallpapersService(archive_path=sample_archive)
    
    wallpapers = service.list_wallpapers()
    
    assert len(wallpapers) == 2
    assert "bg1.jpg" in wallpapers
    assert "bg2.png" in wallpapers
```

#### TC-WP-SVC-002: List wallpapers raises when archive missing

```python
def test_list_wallpapers_raises_when_archive_missing(temp_dir):
    """Service should raise ArchiveNotFoundError for missing archive."""
    service = WallpapersService(archive_path=temp_dir / "missing.tar.gz")
    
    with pytest.raises(ArchiveNotFoundError):
        service.list_wallpapers()
```

#### TC-WP-SVC-003: Add wallpaper creates archive if missing

```python
def test_add_wallpaper_creates_archive_if_missing(temp_dir, sample_image):
    """Service should create archive when adding to non-existent archive."""
    archive_path = temp_dir / "new_archive.tar.gz"
    service = WallpapersService(archive_path=archive_path)
    
    service.add_wallpaper(sample_image)
    
    assert archive_path.exists()
    assert "sample.jpg" in service.list_wallpapers()
```

#### TC-WP-SVC-004: Add wallpaper validates extension

```python
def test_add_wallpaper_validates_extension(temp_dir):
    """Service should reject files with invalid extensions."""
    invalid_file = temp_dir / "document.txt"
    invalid_file.write_text("not an image")
    service = WallpapersService(archive_path=temp_dir / "archive.tar.gz")
    
    with pytest.raises(InvalidImageError):
        service.add_wallpaper(invalid_file)
```

#### TC-WP-SVC-005: Add wallpaper rejects duplicate without overwrite

```python
def test_add_wallpaper_rejects_duplicate_without_overwrite(sample_archive, temp_dir):
    """Service should reject duplicate without overwrite flag."""
    service = WallpapersService(archive_path=sample_archive)
    duplicate = temp_dir / "bg1.jpg"  # Same name as in archive
    duplicate.write_bytes(b"new content")
    
    with pytest.raises(WallpaperError):
        service.add_wallpaper(duplicate, overwrite=False)
```

#### TC-WP-SVC-006: Add wallpaper allows duplicate with overwrite

```python
def test_add_wallpaper_allows_duplicate_with_overwrite(sample_archive, temp_dir):
    """Service should allow duplicate when overwrite is True."""
    service = WallpapersService(archive_path=sample_archive)
    duplicate = temp_dir / "bg1.jpg"
    duplicate.write_bytes(b"new content")
    
    service.add_wallpaper(duplicate, overwrite=True)
    
    # Should not raise
    assert "bg1.jpg" in service.list_wallpapers()
```

#### TC-WP-SVC-007: Extract wallpapers creates directory

```python
def test_extract_wallpapers_creates_directory(sample_archive, temp_dir):
    """Service should create wallpapers subdirectory."""
    service = WallpapersService(archive_path=sample_archive)
    output = temp_dir / "output"
    
    result = service.extract_wallpapers(output)
    
    assert result == output / "wallpapers"
    assert result.exists()
    assert (result / "bg1.jpg").exists()
    assert (result / "bg2.png").exists()
```

#### TC-WP-SVC-008: Is valid image extension accepts common formats

```python
@pytest.mark.parametrize("filename,expected", [
    ("image.jpg", True),
    ("image.jpeg", True),
    ("image.png", True),
    ("image.gif", True),
    ("image.webp", True),
    ("image.bmp", True),
    ("image.tiff", True),
    ("image.tif", True),
    ("image.JPG", True),  # Case insensitive
    ("image.txt", False),
    ("image.pdf", False),
    ("noextension", False),
])
def test_is_valid_image_extension(filename, expected):
    """Service should validate image extensions correctly."""
    assert WallpapersService.is_valid_image_extension(filename) == expected
```

### 5.2 Unit Tests - API Layer

**File**: `dotfiles-wallpapers/tests/unit/test_wallpapers_api.py`

#### TC-WP-API-001: API wraps service correctly

```python
def test_wallpapers_api_wraps_service(sample_archive):
    """Wallpapers API should delegate to service."""
    wallpapers = Wallpapers(archive_path=sample_archive)
    
    result = wallpapers.list()
    
    assert len(result) == 2
```

### 5.3 Integration Tests - CLI

**File**: `dotfiles-wallpapers/tests/integration/test_wallpapers_cli.py`

#### TC-WP-CLI-001: List command shows wallpapers

```python
def test_list_command_shows_wallpapers(sample_archive, monkeypatch):
    """List command should display wallpapers in archive."""
    # Configure to use sample archive
    runner = CliRunner()
    
    result = runner.invoke(app, ["list"])
    
    assert result.exit_code == 0
    assert "bg1.jpg" in result.output
```

#### TC-WP-CLI-002: Add command adds wallpaper

```python
def test_add_command_adds_wallpaper(temp_dir, sample_image):
    """Add command should add wallpaper to archive."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["add", str(sample_image)])
    
    assert result.exit_code == 0
    assert "Successfully added" in result.output
```

#### TC-WP-CLI-003: Add command force overwrites

```python
def test_add_command_force_overwrites(sample_archive, temp_dir):
    """Add command with --force should overwrite existing."""
    duplicate = temp_dir / "bg1.jpg"
    duplicate.write_bytes(b"new")
    runner = CliRunner()
    
    result = runner.invoke(app, ["add", str(duplicate), "--force"])
    
    assert result.exit_code == 0
```

#### TC-WP-CLI-004: Extract command extracts to directory

```python
def test_extract_command_extracts_to_directory(sample_archive, temp_dir):
    """Extract command should extract wallpapers."""
    output = temp_dir / "output"
    runner = CliRunner()
    
    result = runner.invoke(app, ["extract", str(output)])
    
    assert result.exit_code == 0
    assert "Extracted" in result.output
```

---

## 6. Icon Templates Module Tests

### 6.1 Unit Tests - Service Layer

**File**: `dotfiles-icon-templates/tests/unit/test_icon_templates_service.py`

#### TC-ICON-SVC-001: List categories returns directory names

```python
def test_list_categories_returns_directory_names(sample_icons_dir):
    """Service should list category directories."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    
    categories = service.list_categories()
    
    assert len(categories) == 3
    assert "screenshot-tool" in categories
    assert "status-bar" in categories
    assert "wlogout" in categories
```

#### TC-ICON-SVC-002: List icons returns files in category

```python
def test_list_icons_returns_files_in_category(sample_icons_dir):
    """Service should list icons in specified category."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    
    icons = service.list_icons(category="status-bar")
    
    assert len(icons) == 2
    names = [i.name for i in icons]
    assert "battery.svg" in names
    assert "wifi.svg" in names
```

#### TC-ICON-SVC-003: List icons raises for unknown category

```python
def test_list_icons_raises_for_unknown_category(sample_icons_dir):
    """Service should raise CategoryNotFoundError for unknown category."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    
    with pytest.raises(CategoryNotFoundError):
        service.list_icons(category="nonexistent")
```

#### TC-ICON-SVC-004: Get icon returns icon info

```python
def test_get_icon_returns_icon_info(sample_icons_dir):
    """Service should return IconInfo for valid icon."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    
    info = service.get_icon("battery.svg")
    
    assert info.name == "battery.svg"
    assert info.category == "status-bar"
    assert info.path.exists()
```

#### TC-ICON-SVC-005: Get icon raises for unknown icon

```python
def test_get_icon_raises_for_unknown_icon(sample_icons_dir):
    """Service should raise IconNotFoundError for unknown icon."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    
    with pytest.raises(IconNotFoundError):
        service.get_icon("nonexistent.svg")
```

#### TC-ICON-SVC-006: Copy icons copies to target

```python
def test_copy_icons_copies_to_target(sample_icons_dir, temp_dir):
    """Service should copy icons to target directory."""
    service = IconTemplatesService(data_path=sample_icons_dir)
    target = temp_dir / "target"
    
    copied = service.copy_icons(target, category="status-bar")
    
    assert len(copied) == 2
    assert (target / "battery.svg").exists()
    assert (target / "wifi.svg").exists()
```

### 6.2 Integration Tests - CLI

**File**: `dotfiles-icon-templates/tests/integration/test_icon_templates_cli.py`

#### TC-ICON-CLI-001: List command shows categories

```python
def test_list_command_shows_categories(sample_icons_dir):
    """List command should display categories."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["list"])
    
    assert result.exit_code == 0
    assert "screenshot-tool" in result.output
    assert "status-bar" in result.output
```

#### TC-ICON-CLI-002: Copy command copies icons

```python
def test_copy_command_copies_icons(sample_icons_dir, temp_dir):
    """Copy command should copy icons to target."""
    target = temp_dir / "target"
    runner = CliRunner()
    
    result = runner.invoke(app, ["copy", str(target), "--category", "status-bar"])
    
    assert result.exit_code == 0
    assert "Copied" in result.output
```

#### TC-ICON-CLI-003: Show command displays details

```python
def test_show_command_displays_details(sample_icons_dir):
    """Show command should display icon details."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["show", "battery.svg"])
    
    assert result.exit_code == 0
    assert "battery" in result.output
    assert "status-bar" in result.output
```

---

## 7. Root Wrapper Tests

### 7.1 Integration Tests

**File**: `tests/integration/test_cli_hierarchy.py`

#### TC-ROOT-001: Root CLI routes to packages

```python
def test_root_cli_routes_to_packages():
    """Root CLI should route packages command correctly."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["packages", "--help"])
    
    assert result.exit_code == 0
    assert "install" in result.output
    assert "list" in result.output
```

#### TC-ROOT-002: Root CLI routes to wallpapers

```python
def test_root_cli_routes_to_wallpapers():
    """Root CLI should route wallpapers command correctly."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["wallpapers", "--help"])
    
    assert result.exit_code == 0
    assert "add" in result.output
    assert "list" in result.output
    assert "extract" in result.output
```

#### TC-ROOT-003: Root CLI routes to icon-templates

```python
def test_root_cli_routes_to_icon_templates():
    """Root CLI should route icon-templates command correctly."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["icon-templates", "--help"])
    
    assert result.exit_code == 0
    assert "list" in result.output
    assert "copy" in result.output
    assert "show" in result.output
```

#### TC-ROOT-004: Root help shows all subcommands

```python
def test_root_help_shows_all_subcommands():
    """Root CLI help should list all subcommands."""
    runner = CliRunner()
    
    result = runner.invoke(app, ["--help"])
    
    assert result.exit_code == 0
    assert "packages" in result.output
    assert "wallpapers" in result.output
    assert "icon-templates" in result.output
```

---

## 8. Coverage Requirements

### 8.1 Minimum Coverage

| Component | Minimum Coverage |
|-----------|------------------|
| Service Layer | 90% |
| API Layer | 85% |
| CLI Layer | 80% |
| Overall | 85% |

### 8.2 Coverage Commands

```bash
# Generate coverage report
uv run pytest --cov=src --cov-report=html --cov-report=term-missing

# Check coverage threshold
uv run pytest --cov=src --cov-fail-under=85
```

---

## 9. Test Case Matrix

### 9.1 Requirements Traceability

| Test Case | Requirement | Feature Spec |
|-----------|-------------|--------------|
| TC-PKG-SVC-001 | REQ-PKG-001 | FS-PKG-001 |
| TC-PKG-SVC-002 | REQ-PKG-ERR-001 | FS-PKG-001 |
| TC-PKG-SVC-004 | REQ-PKG-002 | FS-PKG-002 |
| TC-PKG-SVC-005 | REQ-PKG-ERR-002 | FS-PKG-002 |
| TC-WP-SVC-001 | REQ-WP-001 | FS-WP-001 |
| TC-WP-SVC-002 | REQ-WP-ERR-001 | FS-WP-001 |
| TC-WP-SVC-003 | REQ-WP-002 | FS-WP-002 |
| TC-WP-SVC-004 | REQ-WP-004 | FS-WP-002 |
| TC-WP-SVC-007 | REQ-WP-003 | FS-WP-003 |
| TC-ICON-SVC-001 | REQ-ICON-001 | FS-ICON-001 |
| TC-ICON-SVC-002 | REQ-ICON-002 | FS-ICON-001 |
| TC-ICON-SVC-006 | REQ-ICON-004 | FS-ICON-002 |

---

## 10. Test Execution Schedule

### 10.1 During Development

- Run unit tests on every change
- Run integration tests before committing
- Maintain green build at all times

### 10.2 CI Pipeline (Future)

```yaml
# Example CI configuration
test:
  script:
    - uv sync
    - uv run pytest --cov=src --cov-fail-under=85
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | AI Assistant | Initial creation |
