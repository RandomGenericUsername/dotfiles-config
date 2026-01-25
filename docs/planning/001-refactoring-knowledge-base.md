# Refactoring Knowledge Base

> **Document Type**: Discovery & Analysis Output  
> **Date**: 2026-01-24  
> **Status**: Draft  
> **Purpose**: Foundational knowledge for deriving TRDs, ADRs, Feature Specs, and Implementation Tasks

---

## Table of Contents

1. [Project Context](#1-project-context)
2. [Source Analysis (dotfiles-config-old)](#2-source-analysis-dotfiles-config-old)
3. [Target Architecture (dotfiles-config)](#3-target-architecture-dotfiles-config)
4. [Module Inventory](#4-module-inventory)
5. [Architectural Decisions](#5-architectural-decisions)
6. [Command Mapping](#6-command-mapping)
7. [API Surface](#7-api-surface)
8. [Test Strategy](#8-test-strategy)
9. [Implementation Phases](#9-implementation-phases)
10. [Open Questions](#10-open-questions)
11. [References](#11-references)

---

## 1. Project Context

### 1.1 Problem Statement

The `dotfiles-config-old` project combines multiple concerns (packages, wallpapers, icon-templates) in a nested workspace structure. This creates:

- Tight coupling between modules
- Difficulty in independent versioning
- Complex dependency management
- Harder to maintain and test in isolation

### 1.2 Goal

Refactor into **separate UV projects** that:

- Can be used as **standalone CLI tools**
- Can be **imported as Python libraries**
- Are **independently testable and versionable**
- Can be **aggregated** by a wrapper project

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| Packages module migration | New feature development |
| Wallpapers module migration | Config-files management |
| Icon-templates module migration | Documentation site |
| Root wrapper project | CI/CD pipeline |
| Fresh test suites | Migration of existing data |

---

## 2. Source Analysis (dotfiles-config-old)

### 2.1 Project Structure

```
dotfiles-config-old/
├── pyproject.toml              # Root project config
├── src/
│   ├── __init__.py
│   └── main.py                 # Root CLI aggregator
├── packages/                   # Package management module
│   ├── pyproject.toml
│   ├── ansible/                # Ansible files
│   │   ├── ansible.cfg
│   │   ├── inventory/
│   │   └── playbooks/
│   ├── src/packages/
│   │   ├── __init__.py
│   │   ├── main.py             # CLI entry
│   │   ├── api/
│   │   │   └── packages.py     # Python API
│   │   └── services/
│   │       └── packages_service.py
│   └── tests/
├── assets/                     # Assets aggregator module
│   ├── pyproject.toml
│   ├── src/assets/
│   │   ├── __init__.py
│   │   └── main.py             # Aggregates wallpapers + icon-templates
│   ├── wallpapers/             # Wallpapers submodule
│   │   ├── pyproject.toml
│   │   ├── src/wallpapers/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── api/
│   │   │   │   └── wallpapers.py
│   │   │   └── services/
│   │   │       └── wallpapers_service.py
│   │   └── tests/
│   └── icon-templates/         # Icon templates submodule
│       ├── pyproject.toml
│       ├── src/icon_templates/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── api/
│       │   └── services/
│       ├── data/               # Icon template files
│       └── tests/
└── tests/
```

### 2.2 Dependency Graph

```
dotfiles-config-old (root)
├── imports → assets.main.app
├── imports → packages.main.app
│
assets (aggregator)
├── imports → wallpapers.main.app
├── imports → icon_templates.main.app
│
packages
├── depends → typer
├── depends → pyyaml
│
wallpapers
├── depends → typer
│
icon_templates
├── depends → typer
```

### 2.3 Build Configuration

**Root `pyproject.toml`:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.workspace]
members = [
    "packages",
    "assets/wallpapers",
    "assets/icon-templates-cli",
    "assets",
]
```

### 2.4 CLI Entry Points

| Package | Entry Point | Target |
|---------|-------------|--------|
| Root | `config` | `src.main:main` |
| Packages | `packages` | `packages.main:app` |
| Assets | `assets` | `assets.main:app` |
| Wallpapers | `wallpapers` | `wallpapers.main:app` |
| Icon Templates | `icon-templates` | `icon_templates.main:app` |

---

## 3. Target Architecture (dotfiles-config)

### 3.1 Design Principles

1. **Separation of Concerns**: Each domain (packages, wallpapers, icon-templates) is its own project
2. **Dual Interface**: Every project supports both CLI and Python API usage
3. **Layered Architecture**: CLI → API → Service pattern per project
4. **UV Workspace**: Root project acts as workspace coordinator
5. **Independent Testability**: Each project has its own test suite

### 3.2 Target Structure

```
dotfiles-config/
├── pyproject.toml                      # UV workspace root
├── README.md
├── docs/
│   └── planning/
│       └── 001-refactoring-knowledge-base.md  # This document
├── src/dotfiles_config/
│   ├── __init__.py                     # Re-exports from subprojects
│   └── cli/
│       ├── __init__.py                 # Main Typer app
│       └── commands/                   # Delegating commands
│
├── dotfiles-packages/                  # Standalone project
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/dotfiles_packages/
│   │   ├── __init__.py                 # Public exports
│   │   ├── cli/
│   │   │   ├── __init__.py             # Typer app
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── install.py
│   │   │       └── list.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── packages.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── packages_service.py
│   ├── ansible/
│   │   ├── ansible.cfg
│   │   ├── inventory/
│   │   └── playbooks/
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       │   ├── __init__.py
│       │   ├── test_packages_service.py
│       │   └── test_packages_api.py
│       └── integration/
│           ├── __init__.py
│           └── test_packages_cli.py
│
├── dotfiles-wallpapers/                # Standalone project
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/dotfiles_wallpapers/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── add.py
│   │   │       ├── extract.py
│   │   │       └── list.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── wallpapers.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── wallpapers_service.py
│   ├── data/
│   │   └── wallpapers.tar.gz           # Archive location
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       │   ├── __init__.py
│       │   ├── test_wallpapers_service.py
│       │   └── test_wallpapers_api.py
│       └── integration/
│           ├── __init__.py
│           └── test_wallpapers_cli.py
│
├── dotfiles-icon-templates/            # Standalone project
│   ├── pyproject.toml
│   ├── README.md
│   ├── src/dotfiles_icon_templates/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── list.py
│   │   │       ├── copy.py
│   │   │       └── show.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── icon_templates.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── icon_templates_service.py
│   ├── data/
│   │   ├── screenshot-tool/
│   │   ├── status-bar/
│   │   └── wlogout/
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       └── integration/
│
└── tests/                              # Root integration tests
    └── integration/
        └── test_cli_hierarchy.py
```

### 3.3 Package Naming Convention

| Project Directory | Package Name | Import Path | CLI Command |
|-------------------|--------------|-------------|-------------|
| `dotfiles-packages/` | `dotfiles-packages` | `dotfiles_packages` | `dotfiles-packages` |
| `dotfiles-wallpapers/` | `dotfiles-wallpapers` | `dotfiles_wallpapers` | `dotfiles-wallpapers` |
| `dotfiles-icon-templates/` | `dotfiles-icon-templates` | `dotfiles_icon_templates` | `dotfiles-icon-templates` |
| Root | `dotfiles-config` | `dotfiles_config` | `dotfiles-config` |

---

## 4. Module Inventory

### 4.1 Packages Module

#### 4.1.1 Purpose
Manage system packages via Ansible playbooks.

#### 4.1.2 Current Implementation Status
✅ Fully implemented in `dotfiles-config-old`

#### 4.1.3 Service Layer

**File**: `packages_service.py`

**Classes:**
- `PackagesService` - Main service class

**Exceptions:**
- `PackagesError` - Base exception
- `PlaybookNotFoundError` - Playbook file doesn't exist
- `AnsibleError` - Ansible command fails (includes `return_code`)
- `AnsibleNotFoundError` - Ansible not installed

**Data Classes:**
- `PackageRole` - Represents a role with `name: str` and `tags: List[str]`

**Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(playbook_path: Optional[Path], ansible_dir: Optional[Path])` | Initialize with paths |
| `list_packages` | `() -> List[PackageRole]` | Parse playbook and list roles with tags |
| `install` | `(tags: Optional[List[str]], extra_args: Optional[List[str]]) -> CompletedProcess` | Run ansible-playbook |

#### 4.1.4 API Layer

**File**: `packages.py`

**Class**: `Packages`

**Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(playbook_path: Optional[Path], ansible_dir: Optional[Path])` | Initialize |
| `list` | `() -> List[PackageRole]` | List packages |
| `install` | `(tags: Optional[List[str]], extra_args: Optional[List[str]]) -> CompletedProcess` | Install packages |

#### 4.1.5 CLI Commands

| Command | Options | Description |
|---------|---------|-------------|
| `install` | `--tags`, `[extra_args...]` | Install packages via Ansible |
| `list` | (none) | List available roles and tags |

#### 4.1.6 Dependencies
- `typer>=0.9.0`
- `pyyaml>=6.0`

---

### 4.2 Wallpapers Module

#### 4.2.1 Purpose
Manage wallpapers stored in a tar.gz archive.

#### 4.2.2 Current Implementation Status
✅ Fully implemented in `dotfiles-config-old`

#### 4.2.3 Service Layer

**File**: `wallpapers_service.py`

**Classes:**
- `WallpapersService` - Main service class

**Exceptions:**
- `WallpaperError` - Base exception
- `ArchiveNotFoundError` - Archive doesn't exist
- `WallpaperNotFoundError` - Wallpaper file doesn't exist
- `InvalidImageError` - File has invalid image extension

**Class Attributes:**
- `VALID_EXTENSIONS: frozenset` - Allowed image extensions

**Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(archive_path: Path)` | Initialize with archive path |
| `is_valid_image_extension` | `@classmethod (filename: str) -> bool` | Check extension validity |
| `list_wallpapers` | `() -> List[str]` | List wallpapers in archive |
| `add_wallpaper` | `(wallpaper_path: Path, overwrite: bool, validate_extension: bool) -> None` | Add to archive |
| `extract_wallpapers` | `(output_path: Path) -> Path` | Extract all wallpapers |

#### 4.2.4 API Layer

**File**: `wallpapers.py`

**Class**: `Wallpapers`

**Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(archive_path: Optional[Path])` | Initialize |
| `list` | `() -> List[str]` | List wallpapers |
| `add` | `(path: Path, *, force: bool, validate: bool) -> None` | Add wallpaper |
| `extract` | `(output_path: Path) -> Path` | Extract wallpapers |

#### 4.2.5 CLI Commands

| Command | Options | Description |
|---------|---------|-------------|
| `add` | `PATH`, `--force/-f`, `--no-validate` | Add wallpaper to archive |
| `extract` | `PATH` | Extract all wallpapers |
| `list` | (none) | List wallpapers in archive |

#### 4.2.6 Dependencies
- `typer>=0.9.0`

---

### 4.3 Icon Templates Module

#### 4.3.1 Purpose
Manage icon templates for various UI components (status bar, screenshot tool, wlogout).

#### 4.3.2 Current Implementation Status
🚧 Scaffold only in `dotfiles-config-old`

#### 4.3.3 Service Layer (To Be Implemented)

**File**: `icon_templates_service.py`

**Planned Classes:**
- `IconTemplatesService` - Main service class

**Planned Exceptions:**
- `IconTemplateError` - Base exception
- `CategoryNotFoundError` - Category doesn't exist
- `IconNotFoundError` - Icon doesn't exist

**Planned Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(data_path: Optional[Path])` | Initialize with data path |
| `list_categories` | `() -> List[str]` | List available categories |
| `list_icons` | `(category: Optional[str]) -> List[IconInfo]` | List icons |
| `get_icon` | `(name: str, category: Optional[str]) -> IconInfo` | Get icon details |
| `copy_icons` | `(target: Path, category: Optional[str], icons: Optional[List[str]]) -> List[Path]` | Copy icons |

#### 4.3.4 API Layer (To Be Implemented)

**File**: `icon_templates.py`

**Class**: `IconTemplates`

**Planned Methods:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(data_path: Optional[Path])` | Initialize |
| `categories` | `() -> List[str]` | List categories |
| `list` | `(category: Optional[str]) -> List[IconInfo]` | List icons |
| `show` | `(name: str) -> IconInfo` | Show icon details |
| `copy` | `(target: Path, **filters) -> List[Path]` | Copy icons |

#### 4.3.5 CLI Commands

| Command | Options | Description |
|---------|---------|-------------|
| `list` | `--category` | List available icon templates |
| `copy` | `TARGET`, `--category`, `--icons` | Copy icons to target directory |
| `show` | `NAME` | Show details about an icon template |

#### 4.3.6 Data Structure

```
data/
├── screenshot-tool/
│   └── *.svg (or other formats)
├── status-bar/
│   ├── battery-icons/
│   ├── email-client-icon/
│   ├── network-icons/
│   ├── power-menu-icons/
│   └── wallpaper-selector-icons/
└── wlogout/
    └── templates/
```

#### 4.3.7 Dependencies
- `typer>=0.9.0`

---

## 5. Architectural Decisions

### 5.1 Build Backend: `uv_build`

**Decision**: Use `uv_build` instead of `hatchling`

**Rationale**:
- Native UV workspace support
- Auto-detects `src/` layout without extra config
- Faster builds (Rust-powered)
- Projects are internal to workspace, not published to PyPI

**Trade-offs**:
- Less ecosystem adoption outside UV
- Would need to switch to `hatchling` if publishing to PyPI

### 5.2 Flat Project Hierarchy

**Decision**: All subprojects are top-level peers, no `assets/` aggregator

**Old Structure**:
```
root/
├── packages/
└── assets/
    ├── wallpapers/
    └── icon-templates/
```

**New Structure**:
```
root/
├── dotfiles-packages/
├── dotfiles-wallpapers/
└── dotfiles-icon-templates/
```

**Rationale**:
- Simpler mental model
- Each project is equally accessible
- No unnecessary aggregation layer
- Cleaner workspace configuration

### 5.3 Dual Interface Pattern

**Decision**: Every project exposes both CLI and Python API

**Rationale**:
- CLI for interactive and scripted usage
- Python API for programmatic integration
- Same business logic serves both interfaces
- Enables composition in larger systems

**Implementation**:
```
project/
├── cli/          # Typer-based CLI
├── api/          # Python API classes
└── services/     # Shared business logic
```

### 5.4 Naming Convention

**Decision**: Use `dotfiles-` prefix for all projects

**Examples**:
- Package: `dotfiles-packages`
- Import: `from dotfiles_packages import Packages`
- CLI: `dotfiles-packages install`

**Rationale**:
- Clear namespace identification
- Avoids conflicts with common package names
- Consistent branding

### 5.5 Fresh Test Suites

**Decision**: Create new tests rather than migrate existing

**Rationale**:
- Tests serve as specification for new architecture
- Old tests may have assumptions about old structure
- Opportunity to establish proper patterns
- Tests become "foundational truth" for documentation

---

## 6. Command Mapping

### 6.1 CLI Command Transformation

| Old Command | New Standalone | New via Wrapper |
|-------------|----------------|-----------------|
| `config packages install [--tags TAG] [ARGS]` | `dotfiles-packages install [--tags TAG] [ARGS]` | `dotfiles-config packages install [--tags TAG] [ARGS]` |
| `config packages list` | `dotfiles-packages list` | `dotfiles-config packages list` |
| `config assets wallpapers add PATH [--force] [--no-validate]` | `dotfiles-wallpapers add PATH [--force] [--no-validate]` | `dotfiles-config wallpapers add PATH [--force] [--no-validate]` |
| `config assets wallpapers list` | `dotfiles-wallpapers list` | `dotfiles-config wallpapers list` |
| `config assets wallpapers extract PATH` | `dotfiles-wallpapers extract PATH` | `dotfiles-config wallpapers extract PATH` |
| `config assets icon-templates list` | `dotfiles-icon-templates list` | `dotfiles-config icon-templates list` |
| `config assets icon-templates copy TARGET` | `dotfiles-icon-templates copy TARGET` | `dotfiles-config icon-templates copy TARGET` |
| `config assets icon-templates show NAME` | `dotfiles-icon-templates show NAME` | `dotfiles-config icon-templates show NAME` |

### 6.2 Removed Commands/Namespaces

| Old | Reason |
|-----|--------|
| `config assets` | Aggregator removed; wallpapers/icon-templates are now peers |

---

## 7. API Surface

### 7.1 Public Exports per Package

#### `dotfiles_packages`

```python
from dotfiles_packages import (
    # API
    Packages,
    
    # Exceptions
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
    
    # Data classes
    PackageRole,
    
    # CLI app (for composition)
    app,
)
```

#### `dotfiles_wallpapers`

```python
from dotfiles_wallpapers import (
    # API
    Wallpapers,
    
    # Exceptions
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
    
    # CLI app (for composition)
    app,
)
```

#### `dotfiles_icon_templates`

```python
from dotfiles_icon_templates import (
    # API
    IconTemplates,
    
    # Exceptions
    IconTemplateError,
    CategoryNotFoundError,
    IconNotFoundError,
    
    # Data classes
    IconInfo,
    
    # CLI app (for composition)
    app,
)
```

#### `dotfiles_config` (Root Wrapper)

```python
from dotfiles_config import (
    # Re-exported APIs
    Packages,
    Wallpapers,
    IconTemplates,
    
    # CLI app
    app,
)
```

### 7.2 Usage Examples

#### Standalone Usage

```python
from dotfiles_packages import Packages

packages = Packages()
roles = packages.list()
for role in roles:
    print(f"{role.name}: {role.tags}")

packages.install(tags=["nvim", "zsh"])
```

```python
from dotfiles_wallpapers import Wallpapers
from pathlib import Path

wallpapers = Wallpapers()
print(wallpapers.list())

wallpapers.add(Path("~/Pictures/bg.png"), force=True)
wallpapers.extract(Path("/tmp/my-wallpapers"))
```

#### Via Wrapper

```python
from dotfiles_config import Packages, Wallpapers

packages = Packages()
wallpapers = Wallpapers()
```

---

## 8. Test Strategy

### 8.1 Test Principles

1. **Tests as Specification**: Tests define expected behavior
2. **Isolation**: Unit tests don't touch filesystem/network
3. **Integration**: CLI tests use real files in temp directories
4. **Coverage**: Aim for high coverage on service layer

### 8.2 Test Structure per Project

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_<name>_service.py    # Service layer tests
│   └── test_<name>_api.py        # API layer tests
└── integration/
    ├── __init__.py
    └── test_<name>_cli.py        # CLI end-to-end tests
```

### 8.3 Common Fixtures

```python
# conftest.py

import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def sample_archive(temp_dir):
    """Create a sample tar.gz archive for testing."""
    # Implementation...
```

### 8.4 Test Cases per Module

#### Packages Module Tests

**Unit Tests (Service)**:
- `test_list_packages_returns_roles_from_playbook`
- `test_list_packages_raises_when_playbook_not_found`
- `test_list_packages_handles_empty_playbook`
- `test_install_constructs_correct_command`
- `test_install_raises_when_ansible_not_found`

**Unit Tests (API)**:
- `test_packages_api_wraps_service`
- `test_packages_api_default_paths`

**Integration Tests (CLI)**:
- `test_list_command_outputs_roles`
- `test_install_command_passes_tags`
- `test_install_command_forwards_extra_args`

#### Wallpapers Module Tests

**Unit Tests (Service)**:
- `test_list_wallpapers_returns_files_from_archive`
- `test_list_wallpapers_raises_when_archive_missing`
- `test_add_wallpaper_creates_archive_if_missing`
- `test_add_wallpaper_validates_extension`
- `test_add_wallpaper_rejects_duplicate_without_force`
- `test_extract_wallpapers_creates_directory`
- `test_is_valid_image_extension_accepts_common_formats`

**Unit Tests (API)**:
- `test_wallpapers_api_wraps_service`
- `test_wallpapers_api_default_archive_path`

**Integration Tests (CLI)**:
- `test_list_command_shows_wallpapers`
- `test_add_command_adds_wallpaper`
- `test_add_command_force_overwrites`
- `test_extract_command_extracts_to_directory`

#### Icon Templates Module Tests

**Unit Tests (Service)**:
- `test_list_categories_returns_directory_names`
- `test_list_icons_returns_files_in_category`
- `test_get_icon_returns_icon_info`
- `test_copy_icons_copies_to_target`

**Integration Tests (CLI)**:
- `test_list_command_shows_categories`
- `test_copy_command_copies_icons`
- `test_show_command_displays_details`

---

## 9. Implementation Phases

### Phase 1: Project Scaffolding

**Goal**: Create all project directories and configuration files

**Tasks**:
1. Create `dotfiles-packages/` directory structure
2. Create `dotfiles-wallpapers/` directory structure
3. Create `dotfiles-icon-templates/` directory structure
4. Create all `pyproject.toml` files with `uv_build`
5. Update root `pyproject.toml` with workspace members
6. Create placeholder `__init__.py` files
7. Verify `uv sync` works

**Deliverables**:
- All directories exist
- All `pyproject.toml` files valid
- `uv sync` succeeds

### Phase 2: Packages Module

**Goal**: Fully functional `dotfiles-packages` project

**Tasks**:
1. Port `PackagesService` class and exceptions
2. Port `Packages` API class
3. Port `PackageRole` data class
4. Create CLI with `install` and `list` commands
5. Set up `__init__.py` exports
6. Copy ansible directory
7. Write unit tests for service
8. Write unit tests for API
9. Write integration tests for CLI

**Deliverables**:
- `dotfiles-packages install` works
- `dotfiles-packages list` works
- `from dotfiles_packages import Packages` works
- All tests pass

### Phase 3: Wallpapers Module

**Goal**: Fully functional `dotfiles-wallpapers` project

**Tasks**:
1. Port `WallpapersService` class and exceptions
2. Port `Wallpapers` API class
3. Create CLI with `add`, `extract`, `list` commands
4. Set up `__init__.py` exports
5. Create `data/` directory for archive
6. Write unit tests for service
7. Write unit tests for API
8. Write integration tests for CLI

**Deliverables**:
- `dotfiles-wallpapers add/extract/list` work
- `from dotfiles_wallpapers import Wallpapers` works
- All tests pass

### Phase 4: Icon Templates Module

**Goal**: Fully functional `dotfiles-icon-templates` project

**Tasks**:
1. Design and implement `IconTemplatesService`
2. Design and implement `IconTemplates` API
3. Create CLI with `list`, `copy`, `show` commands
4. Set up `__init__.py` exports
5. Create/migrate `data/` directory structure
6. Write unit tests
7. Write integration tests

**Deliverables**:
- `dotfiles-icon-templates list/copy/show` work
- `from dotfiles_icon_templates import IconTemplates` works
- All tests pass

### Phase 5: Root Wrapper Integration

**Goal**: `dotfiles-config` aggregates all subprojects

**Tasks**:
1. Configure `pyproject.toml` workspace members
2. Add subprojects as dependencies
3. Create main CLI that imports subproject CLIs
4. Create `__init__.py` re-exports
5. Write integration tests for CLI hierarchy

**Deliverables**:
- `dotfiles-config packages/wallpapers/icon-templates` all work
- `from dotfiles_config import Packages, Wallpapers, IconTemplates` works
- All tests pass

---

## 10. Open Questions

### 10.1 Resolved

| Question | Decision |
|----------|----------|
| Naming prefix? | `dotfiles-` for all |
| Project hierarchy? | Flat peers |
| Build backend? | `uv_build` |
| Test approach? | Fresh start |
| Assets aggregator? | Removed |

### 10.2 To Be Decided

| Question | Options | Notes |
|----------|---------|-------|
| Where to store ansible files? | `dotfiles-packages/ansible/` vs separate location | Currently planning inside package |
| Where to store wallpaper archive? | `dotfiles-wallpapers/data/` vs user config | Currently planning inside package |
| Icon template variants support? | Per the scaffold: default, rounded, sharp, modern | Needs design |
| Version strategy? | Unified vs independent versions | Not yet decided |

---

## 11. References

### 11.1 Source Files (dotfiles-config-old)

| File | Purpose |
|------|---------|
| `src/main.py` | Root CLI aggregator |
| `packages/src/packages/main.py` | Packages CLI |
| `packages/src/packages/services/packages_service.py` | Packages business logic |
| `packages/src/packages/api/packages.py` | Packages Python API |
| `assets/src/assets/main.py` | Assets aggregator CLI |
| `assets/wallpapers/src/wallpapers/main.py` | Wallpapers CLI |
| `assets/wallpapers/src/wallpapers/services/wallpapers_service.py` | Wallpapers business logic |
| `assets/wallpapers/src/wallpapers/api/wallpapers.py` | Wallpapers Python API |
| `assets/icon-templates/src/icon_templates/main.py` | Icon templates CLI (scaffold) |

### 11.2 Documentation (dotfiles-config-old)

| File | Content |
|------|---------|
| `docs/architecture/cli-structure.md` | CLI hierarchy documentation |
| `docs/architecture/design-principles.md` | Design patterns and principles |
| `docs/architecture/directory-layout.md` | Directory structure |
| `docs/reference/tags.md` | Ansible tags reference |

---

## Document History

| Date | Author | Changes |
|------|--------|---------|
| 2026-01-24 | AI Assistant | Initial creation |

---

## Next Steps

From this knowledge base, the following documents can be derived:

1. **Technical Requirements Document (TRD)** - Formal requirements extracted from Module Inventory
2. **Architecture Decision Records (ADRs)** - One ADR per decision in Section 5
3. **Feature Specifications** - Detailed specs for each module
4. **Implementation Tasks** - Actionable tickets from Phase breakdown
5. **Test Plan** - Formal test specification from Section 8
