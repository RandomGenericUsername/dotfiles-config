# Technical Requirements Document (TRD)

> **Document ID**: TRD-001  
> **Version**: 1.0  
> **Date**: 2026-01-24  
> **Status**: Draft  
> **Source**: [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the technical requirements for refactoring the `dotfiles-config-old` monolithic project into separate, independent UV workspace projects.

### 1.2 Scope

This TRD covers:
- `dotfiles-packages` - Package management via Ansible
- `dotfiles-wallpapers` - Wallpaper archive management
- `dotfiles-icon-templates` - Icon template management
- `dotfiles-config` - Root wrapper/aggregator

### 1.3 Definitions

| Term | Definition |
|------|------------|
| UV Workspace | A collection of related Python projects managed by UV |
| CLI | Command Line Interface |
| API | Application Programming Interface (Python) |
| Service Layer | Business logic implementation |

---

## 2. System Requirements

### 2.1 General Requirements

#### REQ-GEN-001: UV Workspace Structure
The system SHALL be organized as a UV workspace with independent member projects.

#### REQ-GEN-002: Dual Interface
Each subproject SHALL provide both a CLI interface and a Python API interface.

#### REQ-GEN-003: Build Backend
All projects SHALL use `uv_build` as the build backend.

#### REQ-GEN-004: Python Version
All projects SHALL require Python >= 3.12.

#### REQ-GEN-005: Independent Installability
Each subproject SHALL be independently installable via `uv pip install` or `pip install`.

#### REQ-GEN-006: Layered Architecture
Each subproject SHALL follow a three-layer architecture:
- CLI Layer (commands)
- API Layer (public interface)
- Service Layer (business logic)

---

## 3. Project Structure Requirements

### 3.1 Root Project (`dotfiles-config`)

#### REQ-ROOT-001: Workspace Definition
The root `pyproject.toml` SHALL define all subprojects as workspace members.

#### REQ-ROOT-002: CLI Aggregation
The root project SHALL provide a CLI that delegates to subproject CLIs.

#### REQ-ROOT-003: API Re-exports
The root project SHALL re-export public APIs from all subprojects.

#### REQ-ROOT-004: CLI Entry Point
The root project SHALL provide CLI entry point `dotfiles-config`.

### 3.2 Subproject Structure

#### REQ-STRUCT-001: Directory Layout
Each subproject SHALL follow this directory structure:
```
project-name/
├── pyproject.toml
├── README.md
├── src/<package_name>/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── commands/
│   ├── api/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

#### REQ-STRUCT-002: Naming Convention
Project directories SHALL use kebab-case with `dotfiles-` prefix.
Package names SHALL use snake_case with `dotfiles_` prefix.

---

## 4. Packages Module Requirements

### 4.1 Functional Requirements

#### REQ-PKG-001: List Packages
The system SHALL list available Ansible roles and their tags from the playbook.

**Input**: None (uses configured playbook path)  
**Output**: List of `PackageRole` objects with `name` and `tags`

#### REQ-PKG-002: Install Packages
The system SHALL install packages by executing `ansible-playbook` with specified tags.

**Input**: 
- `tags: Optional[List[str]]` - Ansible tags to run
- `extra_args: Optional[List[str]]` - Additional ansible-playbook arguments

**Output**: `subprocess.CompletedProcess` with execution result

#### REQ-PKG-003: Tag Forwarding
The install command SHALL forward `--tags` option to ansible-playbook.

#### REQ-PKG-004: Extra Arguments
The install command SHALL forward all unrecognized arguments to ansible-playbook.

### 4.2 Error Handling Requirements

#### REQ-PKG-ERR-001: Playbook Not Found
The system SHALL raise `PlaybookNotFoundError` when the playbook file does not exist.

#### REQ-PKG-ERR-002: Ansible Not Found
The system SHALL raise `AnsibleNotFoundError` when ansible-playbook command is not available.

#### REQ-PKG-ERR-003: Ansible Execution Error
The system SHALL raise `AnsibleError` with return code when ansible-playbook fails.

### 4.3 CLI Requirements

#### REQ-PKG-CLI-001: Install Command
```
dotfiles-packages install [--tags TAG1,TAG2] [EXTRA_ARGS...]
```

#### REQ-PKG-CLI-002: List Command
```
dotfiles-packages list
```

#### REQ-PKG-CLI-003: Exit Codes
- Exit 0: Success
- Exit 1: Error (playbook not found, ansible not found)
- Exit N: Ansible exit code on execution failure

### 4.4 API Requirements

#### REQ-PKG-API-001: Packages Class
The `Packages` class SHALL provide:
- `__init__(playbook_path: Optional[Path], ansible_dir: Optional[Path])`
- `list() -> List[PackageRole]`
- `install(tags: Optional[List[str]], extra_args: Optional[List[str]]) -> CompletedProcess`

#### REQ-PKG-API-002: Public Exports
The package SHALL export:
- `Packages` (API class)
- `PackageRole` (data class)
- `PackagesError`, `PlaybookNotFoundError`, `AnsibleError`, `AnsibleNotFoundError` (exceptions)
- `app` (Typer CLI app)

### 4.5 Configuration Requirements

#### REQ-PKG-CFG-001: Default Playbook Path
Default playbook path SHALL be `<project>/ansible/playbooks/bootstrap.yml`.

#### REQ-PKG-CFG-002: Ansible Directory
The ansible working directory SHALL be `<project>/ansible/`.

---

## 5. Wallpapers Module Requirements

### 5.1 Functional Requirements

#### REQ-WP-001: List Wallpapers
The system SHALL list all wallpaper filenames in the archive.

**Input**: None (uses configured archive path)  
**Output**: `List[str]` of wallpaper filenames

#### REQ-WP-002: Add Wallpaper
The system SHALL add a wallpaper image to the archive.

**Input**:
- `path: Path` - Path to wallpaper file
- `overwrite: bool` - Whether to overwrite existing
- `validate_extension: bool` - Whether to validate image extension

**Output**: None (modifies archive)

#### REQ-WP-003: Extract Wallpapers
The system SHALL extract all wallpapers to a specified directory.

**Input**: `output_path: Path` - Target directory  
**Output**: `Path` to created `wallpapers/` subdirectory

#### REQ-WP-004: Extension Validation
The system SHALL validate image extensions against allowed formats:
`jpg, jpeg, png, gif, bmp, webp, tiff, tif`

#### REQ-WP-005: Archive Format
Wallpapers SHALL be stored in a `tar.gz` archive.

#### REQ-WP-006: Duplicate Handling
When adding a wallpaper with existing name:
- If `overwrite=True`: Replace existing
- If `overwrite=False`: Raise error

### 5.2 Error Handling Requirements

#### REQ-WP-ERR-001: Archive Not Found
The system SHALL raise `ArchiveNotFoundError` when archive does not exist (for list/extract).

#### REQ-WP-ERR-002: Wallpaper Not Found
The system SHALL raise `WallpaperNotFoundError` when source wallpaper file does not exist.

#### REQ-WP-ERR-003: Invalid Image
The system SHALL raise `InvalidImageError` when file has invalid extension (if validation enabled).

#### REQ-WP-ERR-004: Duplicate Without Force
The system SHALL raise `WallpaperError` when adding duplicate without overwrite flag.

### 5.3 CLI Requirements

#### REQ-WP-CLI-001: Add Command
```
dotfiles-wallpapers add PATH [--force/-f] [--no-validate]
```

#### REQ-WP-CLI-002: List Command
```
dotfiles-wallpapers list
```

#### REQ-WP-CLI-003: Extract Command
```
dotfiles-wallpapers extract PATH
```

#### REQ-WP-CLI-004: Exit Codes
- Exit 0: Success
- Exit 1: Any error

### 5.4 API Requirements

#### REQ-WP-API-001: Wallpapers Class
The `Wallpapers` class SHALL provide:
- `__init__(archive_path: Optional[Path])`
- `list() -> List[str]`
- `add(path: Path, *, force: bool = False, validate: bool = True) -> None`
- `extract(output_path: Path) -> Path`

#### REQ-WP-API-002: Public Exports
The package SHALL export:
- `Wallpapers` (API class)
- `WallpaperError`, `ArchiveNotFoundError`, `WallpaperNotFoundError`, `InvalidImageError` (exceptions)
- `app` (Typer CLI app)

### 5.5 Configuration Requirements

#### REQ-WP-CFG-001: Default Archive Path
Default archive path SHALL be `<project>/data/wallpapers.tar.gz`.

---

## 6. Icon Templates Module Requirements

### 6.1 Functional Requirements

#### REQ-ICON-001: List Categories
The system SHALL list available icon categories.

**Input**: None  
**Output**: `List[str]` of category names

#### REQ-ICON-002: List Icons
The system SHALL list icons, optionally filtered by category.

**Input**: `category: Optional[str]`  
**Output**: `List[IconInfo]` with icon details

#### REQ-ICON-003: Show Icon Details
The system SHALL display details about a specific icon.

**Input**: `name: str`  
**Output**: `IconInfo` with icon details

#### REQ-ICON-004: Copy Icons
The system SHALL copy icons to a target directory.

**Input**:
- `target: Path` - Target directory
- `category: Optional[str]` - Filter by category
- `icons: Optional[List[str]]` - Specific icons to copy

**Output**: `List[Path]` of copied files

### 6.2 Data Model Requirements

#### REQ-ICON-DATA-001: IconInfo Structure
`IconInfo` SHALL contain:
- `name: str` - Icon name
- `category: str` - Category name
- `path: Path` - File path
- `variants: List[str]` - Available variants (if applicable)

#### REQ-ICON-DATA-002: Categories
The system SHALL support categories:
- `screenshot-tool`
- `status-bar`
- `wlogout`

### 6.3 Error Handling Requirements

#### REQ-ICON-ERR-001: Category Not Found
The system SHALL raise `CategoryNotFoundError` when category does not exist.

#### REQ-ICON-ERR-002: Icon Not Found
The system SHALL raise `IconNotFoundError` when icon does not exist.

### 6.4 CLI Requirements

#### REQ-ICON-CLI-001: List Command
```
dotfiles-icon-templates list [--category CATEGORY]
```

#### REQ-ICON-CLI-002: Copy Command
```
dotfiles-icon-templates copy TARGET [--category CATEGORY] [--icons ICON1,ICON2]
```

#### REQ-ICON-CLI-003: Show Command
```
dotfiles-icon-templates show NAME
```

### 6.5 API Requirements

#### REQ-ICON-API-001: IconTemplates Class
The `IconTemplates` class SHALL provide:
- `__init__(data_path: Optional[Path])`
- `categories() -> List[str]`
- `list(category: Optional[str] = None) -> List[IconInfo]`
- `show(name: str) -> IconInfo`
- `copy(target: Path, category: Optional[str] = None, icons: Optional[List[str]] = None) -> List[Path]`

#### REQ-ICON-API-002: Public Exports
The package SHALL export:
- `IconTemplates` (API class)
- `IconInfo` (data class)
- `IconTemplateError`, `CategoryNotFoundError`, `IconNotFoundError` (exceptions)
- `app` (Typer CLI app)

### 6.5 Configuration Requirements

#### REQ-ICON-CFG-001: Default Data Path
Default data path SHALL be `<project>/data/`.

---

## 7. Non-Functional Requirements

### 7.1 Performance

#### REQ-NFR-001: CLI Response Time
CLI commands SHALL respond within 1 second for non-network operations.

### 7.2 Maintainability

#### REQ-NFR-002: Test Coverage
Each module SHALL have >= 80% code coverage.

#### REQ-NFR-003: Type Hints
All public APIs SHALL have complete type annotations.

### 7.3 Compatibility

#### REQ-NFR-004: Platform Support
The system SHALL support Linux operating systems.

#### REQ-NFR-005: UV Compatibility
The system SHALL be compatible with UV package manager.

---

## 8. Traceability Matrix

| Requirement | Feature Spec | Test Case | Implementation |
|-------------|--------------|-----------|----------------|
| REQ-PKG-001 | FS-PKG-001 | TC-PKG-001 | Phase 2 |
| REQ-PKG-002 | FS-PKG-002 | TC-PKG-002 | Phase 2 |
| REQ-WP-001 | FS-WP-001 | TC-WP-001 | Phase 3 |
| REQ-WP-002 | FS-WP-002 | TC-WP-002 | Phase 3 |
| REQ-WP-003 | FS-WP-003 | TC-WP-003 | Phase 3 |
| REQ-ICON-001 | FS-ICON-001 | TC-ICON-001 | Phase 4 |
| REQ-ICON-002 | FS-ICON-002 | TC-ICON-002 | Phase 4 |
| REQ-ICON-003 | FS-ICON-003 | TC-ICON-003 | Phase 4 |
| REQ-ICON-004 | FS-ICON-004 | TC-ICON-004 | Phase 4 |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | AI Assistant | Initial creation |
