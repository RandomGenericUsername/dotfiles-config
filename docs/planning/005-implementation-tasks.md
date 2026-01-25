# Implementation Tasks

> **Document ID**: TASKS-001  
> **Version**: 1.0  
> **Date**: 2026-01-24  
> **Status**: Draft  
> **Source**: [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

---

## Overview

This document breaks down the implementation into actionable tasks organized by phase. Each task is designed to be independently completable and testable.

### Task Status Legend
- 🔲 Not Started
- 🔄 In Progress
- ✅ Completed
- ⏸️ Blocked

### Priority Legend
- P0: Critical - Must complete first
- P1: High - Core functionality
- P2: Medium - Important but not blocking
- P3: Low - Nice to have

---

## Phase 1: Project Scaffolding

**Goal**: Create all project directories and configuration files  
**Estimated Effort**: 2-3 hours  
**Dependencies**: None

### Task 1.1: Create dotfiles-packages Project Structure

**ID**: TASK-1.1  
**Priority**: P0  
**Status**: 🔲

Create the directory structure for the packages project.

**Acceptance Criteria**:
- [ ] Directory `dotfiles-packages/` exists
- [ ] All subdirectories created per architecture
- [ ] All `__init__.py` files created (empty)

**Deliverables**:
```
dotfiles-packages/
├── README.md
├── pyproject.toml
├── src/
│   └── dotfiles_packages/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands/
│       │       └── __init__.py
│       ├── api/
│       │   └── __init__.py
│       └── services/
│           └── __init__.py
├── ansible/
│   ├── ansible.cfg
│   ├── inventory/
│   └── playbooks/
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   └── __init__.py
    └── integration/
        └── __init__.py
```

---

### Task 1.2: Create dotfiles-wallpapers Project Structure

**ID**: TASK-1.2  
**Priority**: P0  
**Status**: 🔲

Create the directory structure for the wallpapers project.

**Acceptance Criteria**:
- [ ] Directory `dotfiles-wallpapers/` exists
- [ ] All subdirectories created per architecture
- [ ] All `__init__.py` files created (empty)

**Deliverables**:
```
dotfiles-wallpapers/
├── README.md
├── pyproject.toml
├── src/
│   └── dotfiles_wallpapers/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands/
│       │       └── __init__.py
│       ├── api/
│       │   └── __init__.py
│       └── services/
│           └── __init__.py
├── data/
│   └── .gitkeep
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   └── __init__.py
    └── integration/
        └── __init__.py
```

---

### Task 1.3: Create dotfiles-icon-templates Project Structure

**ID**: TASK-1.3  
**Priority**: P0  
**Status**: 🔲

Create the directory structure for the icon-templates project.

**Acceptance Criteria**:
- [ ] Directory `dotfiles-icon-templates/` exists
- [ ] All subdirectories created per architecture
- [ ] All `__init__.py` files created (empty)

**Deliverables**:
```
dotfiles-icon-templates/
├── README.md
├── pyproject.toml
├── src/
│   └── dotfiles_icon_templates/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── commands/
│       │       └── __init__.py
│       ├── api/
│       │   └── __init__.py
│       └── services/
│           └── __init__.py
├── data/
│   ├── screenshot-tool/
│   ├── status-bar/
│   └── wlogout/
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    │   └── __init__.py
    └── integration/
        └── __init__.py
```

---

### Task 1.4: Create pyproject.toml Files

**ID**: TASK-1.4  
**Priority**: P0  
**Status**: 🔲  
**Depends On**: TASK-1.1, TASK-1.2, TASK-1.3

Create `pyproject.toml` for each subproject with `uv_build` backend.

**Acceptance Criteria**:
- [ ] `dotfiles-packages/pyproject.toml` valid
- [ ] `dotfiles-wallpapers/pyproject.toml` valid
- [ ] `dotfiles-icon-templates/pyproject.toml` valid
- [ ] All use `uv_build` backend
- [ ] All have correct dependencies
- [ ] All have CLI entry points defined

**Template** (adapt per project):
```toml
[project]
name = "dotfiles-packages"
version = "0.1.0"
description = "Package management for dotfiles via Ansible"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "typer>=0.9.0",
]

[project.scripts]
dotfiles-packages = "dotfiles_packages.cli:app"

[build-system]
requires = ["uv_build>=0.9.22,<0.10.0"]
build-backend = "uv_build"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

---

### Task 1.5: Update Root pyproject.toml

**ID**: TASK-1.5  
**Priority**: P0  
**Status**: 🔲  
**Depends On**: TASK-1.4

Update root `pyproject.toml` to define UV workspace members.

**Acceptance Criteria**:
- [ ] Workspace members defined
- [ ] Dependencies include subprojects
- [ ] `uv sync` succeeds

**Changes**:
```toml
[tool.uv.workspace]
members = [
    "dotfiles-packages",
    "dotfiles-wallpapers",
    "dotfiles-icon-templates",
]

[project]
dependencies = [
    "typer>=0.9.0",
    "dotfiles-packages",
    "dotfiles-wallpapers",
    "dotfiles-icon-templates",
]
```

---

### Task 1.6: Verify Workspace Setup

**ID**: TASK-1.6  
**Priority**: P0  
**Status**: 🔲  
**Depends On**: TASK-1.5

Verify the workspace is correctly configured.

**Acceptance Criteria**:
- [ ] `uv sync` completes without errors
- [ ] All packages importable
- [ ] No circular dependency issues

**Verification Commands**:
```bash
cd dotfiles-config
uv sync
uv run python -c "import dotfiles_packages"
uv run python -c "import dotfiles_wallpapers"
uv run python -c "import dotfiles_icon_templates"
```

---

## Phase 2: Packages Module

**Goal**: Fully functional `dotfiles-packages` project  
**Estimated Effort**: 4-6 hours  
**Dependencies**: Phase 1

### Task 2.1: Implement PackagesService

**ID**: TASK-2.1  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-1.6

Port the service layer with all exceptions and business logic.

**Acceptance Criteria**:
- [ ] `PackagesError` base exception
- [ ] `PlaybookNotFoundError` exception
- [ ] `AnsibleNotFoundError` exception
- [ ] `AnsibleError` exception with return_code
- [ ] `PackageRole` dataclass
- [ ] `PackagesService` class with `list_packages()` method
- [ ] `PackagesService` class with `install()` method

**Files**:
- `src/dotfiles_packages/services/__init__.py`
- `src/dotfiles_packages/services/packages_service.py`

**Reference**: `dotfiles-config-old/packages/src/packages/services/packages_service.py`

---

### Task 2.2: Implement Packages API

**ID**: TASK-2.2  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.1

Create the public Python API class.

**Acceptance Criteria**:
- [ ] `Packages` class implemented
- [ ] `list()` method delegates to service
- [ ] `install()` method delegates to service
- [ ] Default paths configured correctly

**Files**:
- `src/dotfiles_packages/api/__init__.py`
- `src/dotfiles_packages/api/packages.py`

**Reference**: `dotfiles-config-old/packages/src/packages/api/packages.py`

---

### Task 2.3: Implement Packages CLI

**ID**: TASK-2.3  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.1

Create CLI commands using Typer.

**Acceptance Criteria**:
- [ ] `list` command implemented
- [ ] `install` command implemented with `--tags` option
- [ ] `install` command forwards extra arguments
- [ ] Proper error handling and exit codes
- [ ] Help text for all commands

**Files**:
- `src/dotfiles_packages/cli/__init__.py`
- `src/dotfiles_packages/cli/commands/__init__.py`
- `src/dotfiles_packages/cli/commands/list.py`
- `src/dotfiles_packages/cli/commands/install.py`

**Reference**: `dotfiles-config-old/packages/src/packages/main.py`

---

### Task 2.4: Setup Package Exports

**ID**: TASK-2.4  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.2, TASK-2.3

Configure `__init__.py` to export public API.

**Acceptance Criteria**:
- [ ] `Packages` importable from `dotfiles_packages`
- [ ] `PackageRole` importable from `dotfiles_packages`
- [ ] All exceptions importable from `dotfiles_packages`
- [ ] `app` (CLI) importable from `dotfiles_packages`

**File**: `src/dotfiles_packages/__init__.py`

**Expected Content**:
```python
from dotfiles_packages.api.packages import Packages
from dotfiles_packages.services.packages_service import (
    PackageRole,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
)
from dotfiles_packages.cli import app

__all__ = [
    "Packages",
    "PackageRole",
    "PackagesError",
    "PlaybookNotFoundError",
    "AnsibleError",
    "AnsibleNotFoundError",
    "app",
]
```

---

### Task 2.5: Copy Ansible Directory

**ID**: TASK-2.5  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-1.1

Copy ansible configuration from old project.

**Acceptance Criteria**:
- [ ] `ansible.cfg` copied
- [ ] `inventory/` directory copied
- [ ] `playbooks/` directory copied
- [ ] Paths updated if necessary

**Source**: `dotfiles-config-old/packages/ansible/`  
**Destination**: `dotfiles-packages/ansible/`

---

### Task 2.6: Write Packages Unit Tests

**ID**: TASK-2.6  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.1, TASK-2.2

Write unit tests for service and API layers.

**Acceptance Criteria**:
- [ ] Service tests cover `list_packages()`
- [ ] Service tests cover `install()`
- [ ] Service tests cover all error scenarios
- [ ] API tests verify delegation to service
- [ ] All tests pass

**Files**:
- `tests/unit/test_packages_service.py`
- `tests/unit/test_packages_api.py`

---

### Task 2.7: Write Packages Integration Tests

**ID**: TASK-2.7  
**Priority**: P2  
**Status**: 🔲  
**Depends On**: TASK-2.3

Write integration tests for CLI.

**Acceptance Criteria**:
- [ ] `list` command tested
- [ ] `install` command tested (with mocked ansible)
- [ ] Error scenarios tested
- [ ] Exit codes verified

**Files**:
- `tests/integration/test_packages_cli.py`

---

## Phase 3: Wallpapers Module

**Goal**: Fully functional `dotfiles-wallpapers` project  
**Estimated Effort**: 4-6 hours  
**Dependencies**: Phase 1

### Task 3.1: Implement WallpapersService

**ID**: TASK-3.1  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-1.6

Port the service layer with all exceptions and business logic.

**Acceptance Criteria**:
- [ ] `WallpaperError` base exception
- [ ] `ArchiveNotFoundError` exception
- [ ] `WallpaperNotFoundError` exception
- [ ] `InvalidImageError` exception
- [ ] `WallpapersService` class with `list_wallpapers()` method
- [ ] `WallpapersService` class with `add_wallpaper()` method
- [ ] `WallpapersService` class with `extract_wallpapers()` method
- [ ] `is_valid_image_extension()` class method

**Files**:
- `src/dotfiles_wallpapers/services/__init__.py`
- `src/dotfiles_wallpapers/services/wallpapers_service.py`

**Reference**: `dotfiles-config-old/assets/wallpapers/src/wallpapers/services/wallpapers_service.py`

---

### Task 3.2: Implement Wallpapers API

**ID**: TASK-3.2  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-3.1

Create the public Python API class.

**Acceptance Criteria**:
- [ ] `Wallpapers` class implemented
- [ ] `list()` method delegates to service
- [ ] `add()` method delegates to service
- [ ] `extract()` method delegates to service
- [ ] Default archive path configured correctly

**Files**:
- `src/dotfiles_wallpapers/api/__init__.py`
- `src/dotfiles_wallpapers/api/wallpapers.py`

**Reference**: `dotfiles-config-old/assets/wallpapers/src/wallpapers/api/wallpapers.py`

---

### Task 3.3: Implement Wallpapers CLI

**ID**: TASK-3.3  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-3.1

Create CLI commands using Typer.

**Acceptance Criteria**:
- [ ] `list` command implemented
- [ ] `add` command implemented with `--force` and `--no-validate` options
- [ ] `extract` command implemented
- [ ] Proper error handling and exit codes
- [ ] Help text for all commands

**Files**:
- `src/dotfiles_wallpapers/cli/__init__.py`
- `src/dotfiles_wallpapers/cli/commands/__init__.py`
- `src/dotfiles_wallpapers/cli/commands/list.py`
- `src/dotfiles_wallpapers/cli/commands/add.py`
- `src/dotfiles_wallpapers/cli/commands/extract.py`

**Reference**: `dotfiles-config-old/assets/wallpapers/src/wallpapers/main.py`

---

### Task 3.4: Setup Wallpapers Exports

**ID**: TASK-3.4  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-3.2, TASK-3.3

Configure `__init__.py` to export public API.

**Acceptance Criteria**:
- [ ] `Wallpapers` importable from `dotfiles_wallpapers`
- [ ] All exceptions importable from `dotfiles_wallpapers`
- [ ] `app` (CLI) importable from `dotfiles_wallpapers`

**File**: `src/dotfiles_wallpapers/__init__.py`

---

### Task 3.5: Write Wallpapers Unit Tests

**ID**: TASK-3.5  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-3.1, TASK-3.2

Write unit tests for service and API layers.

**Acceptance Criteria**:
- [ ] Service tests cover `list_wallpapers()`
- [ ] Service tests cover `add_wallpaper()`
- [ ] Service tests cover `extract_wallpapers()`
- [ ] Service tests cover `is_valid_image_extension()`
- [ ] Service tests cover all error scenarios
- [ ] API tests verify delegation to service
- [ ] All tests pass

**Files**:
- `tests/unit/test_wallpapers_service.py`
- `tests/unit/test_wallpapers_api.py`

---

### Task 3.6: Write Wallpapers Integration Tests

**ID**: TASK-3.6  
**Priority**: P2  
**Status**: 🔲  
**Depends On**: TASK-3.3

Write integration tests for CLI.

**Acceptance Criteria**:
- [ ] `list` command tested
- [ ] `add` command tested
- [ ] `extract` command tested
- [ ] Error scenarios tested
- [ ] Exit codes verified

**Files**:
- `tests/integration/test_wallpapers_cli.py`

---

## Phase 4: Icon Templates Module

**Goal**: Fully functional `dotfiles-icon-templates` project  
**Estimated Effort**: 6-8 hours  
**Dependencies**: Phase 1

### Task 4.1: Design IconTemplatesService

**ID**: TASK-4.1  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-1.6

Design and implement the service layer (new implementation, not port).

**Acceptance Criteria**:
- [ ] `IconTemplateError` base exception
- [ ] `CategoryNotFoundError` exception
- [ ] `IconNotFoundError` exception
- [ ] `IconInfo` dataclass
- [ ] `IconTemplatesService` class with `list_categories()` method
- [ ] `IconTemplatesService` class with `list_icons()` method
- [ ] `IconTemplatesService` class with `get_icon()` method
- [ ] `IconTemplatesService` class with `copy_icons()` method

**Files**:
- `src/dotfiles_icon_templates/services/__init__.py`
- `src/dotfiles_icon_templates/services/icon_templates_service.py`

---

### Task 4.2: Implement IconTemplates API

**ID**: TASK-4.2  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-4.1

Create the public Python API class.

**Acceptance Criteria**:
- [ ] `IconTemplates` class implemented
- [ ] `categories()` method delegates to service
- [ ] `list()` method delegates to service
- [ ] `show()` method delegates to service
- [ ] `copy()` method delegates to service
- [ ] Default data path configured correctly

**Files**:
- `src/dotfiles_icon_templates/api/__init__.py`
- `src/dotfiles_icon_templates/api/icon_templates.py`

---

### Task 4.3: Implement IconTemplates CLI

**ID**: TASK-4.3  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-4.1

Create CLI commands using Typer.

**Acceptance Criteria**:
- [ ] `list` command implemented with `--category` option
- [ ] `copy` command implemented with `--category` and `--icons` options
- [ ] `show` command implemented
- [ ] Proper error handling and exit codes
- [ ] Help text for all commands

**Files**:
- `src/dotfiles_icon_templates/cli/__init__.py`
- `src/dotfiles_icon_templates/cli/commands/__init__.py`
- `src/dotfiles_icon_templates/cli/commands/list.py`
- `src/dotfiles_icon_templates/cli/commands/copy.py`
- `src/dotfiles_icon_templates/cli/commands/show.py`

---

### Task 4.4: Setup IconTemplates Exports

**ID**: TASK-4.4  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-4.2, TASK-4.3

Configure `__init__.py` to export public API.

**Acceptance Criteria**:
- [ ] `IconTemplates` importable from `dotfiles_icon_templates`
- [ ] `IconInfo` importable from `dotfiles_icon_templates`
- [ ] All exceptions importable from `dotfiles_icon_templates`
- [ ] `app` (CLI) importable from `dotfiles_icon_templates`

**File**: `src/dotfiles_icon_templates/__init__.py`

---

### Task 4.5: Setup Data Directory

**ID**: TASK-4.5  
**Priority**: P2  
**Status**: 🔲  
**Depends On**: TASK-1.3

Create/migrate icon template data.

**Acceptance Criteria**:
- [ ] `data/screenshot-tool/` exists with icons
- [ ] `data/status-bar/` exists with icons
- [ ] `data/wlogout/` exists with icons

**Source**: `dotfiles-config-old/assets/icon-templates/data/`  
**Destination**: `dotfiles-icon-templates/data/`

---

### Task 4.6: Write IconTemplates Unit Tests

**ID**: TASK-4.6  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-4.1, TASK-4.2

Write unit tests for service and API layers.

**Acceptance Criteria**:
- [ ] Service tests cover `list_categories()`
- [ ] Service tests cover `list_icons()`
- [ ] Service tests cover `get_icon()`
- [ ] Service tests cover `copy_icons()`
- [ ] Service tests cover all error scenarios
- [ ] API tests verify delegation to service
- [ ] All tests pass

**Files**:
- `tests/unit/test_icon_templates_service.py`
- `tests/unit/test_icon_templates_api.py`

---

### Task 4.7: Write IconTemplates Integration Tests

**ID**: TASK-4.7  
**Priority**: P2  
**Status**: 🔲  
**Depends On**: TASK-4.3

Write integration tests for CLI.

**Acceptance Criteria**:
- [ ] `list` command tested
- [ ] `copy` command tested
- [ ] `show` command tested
- [ ] Error scenarios tested
- [ ] Exit codes verified

**Files**:
- `tests/integration/test_icon_templates_cli.py`

---

## Phase 5: Root Wrapper Integration

**Goal**: `dotfiles-config` aggregates all subprojects  
**Estimated Effort**: 2-3 hours  
**Dependencies**: Phase 2, 3, 4

### Task 5.1: Update Root CLI

**ID**: TASK-5.1  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.3, TASK-3.3, TASK-4.3

Create main CLI that imports subproject CLIs.

**Acceptance Criteria**:
- [ ] `packages` subcommand routes to dotfiles-packages
- [ ] `wallpapers` subcommand routes to dotfiles-wallpapers
- [ ] `icon-templates` subcommand routes to dotfiles-icon-templates
- [ ] Help text shows all subcommands

**Files**:
- `src/dotfiles_config/cli/__init__.py`
- `src/dotfiles_config/cli/commands/__init__.py`

---

### Task 5.2: Setup Root Exports

**ID**: TASK-5.2  
**Priority**: P1  
**Status**: 🔲  
**Depends On**: TASK-2.4, TASK-3.4, TASK-4.4

Configure root `__init__.py` to re-export APIs.

**Acceptance Criteria**:
- [ ] `Packages` importable from `dotfiles_config`
- [ ] `Wallpapers` importable from `dotfiles_config`
- [ ] `IconTemplates` importable from `dotfiles_config`

**File**: `src/dotfiles_config/__init__.py`

---

### Task 5.3: Write Root Integration Tests

**ID**: TASK-5.3  
**Priority**: P2  
**Status**: 🔲  
**Depends On**: TASK-5.1

Write integration tests for CLI hierarchy.

**Acceptance Criteria**:
- [ ] Root CLI routes correctly to subcommands
- [ ] All subcommands accessible
- [ ] Help text correct

**Files**:
- `tests/integration/test_cli_hierarchy.py`

---

### Task 5.4: Create README Files

**ID**: TASK-5.4  
**Priority**: P3  
**Status**: 🔲  
**Depends On**: All previous tasks

Create README documentation for each project.

**Acceptance Criteria**:
- [ ] `dotfiles-packages/README.md` documents usage
- [ ] `dotfiles-wallpapers/README.md` documents usage
- [ ] `dotfiles-icon-templates/README.md` documents usage
- [ ] Root `README.md` updated with new structure

---

## Task Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| Phase 1: Scaffolding | 6 tasks | 2-3 hours |
| Phase 2: Packages | 7 tasks | 4-6 hours |
| Phase 3: Wallpapers | 6 tasks | 4-6 hours |
| Phase 4: Icon Templates | 7 tasks | 6-8 hours |
| Phase 5: Root Wrapper | 4 tasks | 2-3 hours |
| **Total** | **30 tasks** | **18-26 hours** |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | AI Assistant | Initial creation |
