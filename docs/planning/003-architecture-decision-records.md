# Architecture Decision Records (ADRs)

> **Document ID**: ADR-INDEX  
> **Date**: 2026-01-24  
> **Source**: [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

This directory contains Architecture Decision Records for the dotfiles-config project.

---

## ADR Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-001](#adr-001-build-backend-selection) | Build Backend Selection | Accepted | 2026-01-24 |
| [ADR-002](#adr-002-flat-project-hierarchy) | Flat Project Hierarchy | Accepted | 2026-01-24 |
| [ADR-003](#adr-003-dual-interface-pattern) | Dual Interface Pattern | Accepted | 2026-01-24 |
| [ADR-004](#adr-004-naming-convention) | Naming Convention | Accepted | 2026-01-24 |
| [ADR-005](#adr-005-fresh-test-suites) | Fresh Test Suites | Accepted | 2026-01-24 |
| [ADR-006](#adr-006-layered-architecture) | Layered Architecture | Accepted | 2026-01-24 |

---

## ADR-001: Build Backend Selection

### Status
Accepted

### Context
Python projects require a build backend to create distributable packages. The old project used `hatchling`, a mature and widely-adopted backend. UV provides its own build backend `uv_build` designed for UV-native workflows.

We needed to decide which build backend to use for the refactored projects.

### Decision
We will use `uv_build` as the build backend for all projects.

```toml
[build-system]
requires = ["uv_build>=0.9.22,<0.10.0"]
build-backend = "uv_build"
```

### Rationale

**Chosen: `uv_build`**

Advantages:
- Native UV workspace support with automatic member resolution
- Auto-detects `src/` layout without extra configuration
- Faster builds (Rust-powered)
- Zero-config for common project layouts
- Designed for UV-first development workflow

**Rejected: `hatchling`**

Would have been better if:
- Publishing to PyPI immediately
- Need maximum compatibility with pip and other tools
- Working outside UV ecosystem

### Consequences

**Positive:**
- Simpler `pyproject.toml` configuration
- Faster development iteration
- Seamless workspace integration

**Negative:**
- Less ecosystem adoption outside UV
- Would need migration if publishing to PyPI
- Tighter coupling to UV toolchain

### Notes
If individual packages need to be published to PyPI in the future, we can switch those specific packages to `hatchling` while keeping internal packages on `uv_build`.

---

## ADR-002: Flat Project Hierarchy

### Status
Accepted

### Context
The old project structure had a nested hierarchy:

```
root/
├── packages/
└── assets/
    ├── wallpapers/
    └── icon-templates/
```

The `assets/` directory acted as an aggregator for wallpapers and icon-templates. We needed to decide whether to maintain this nesting or flatten the structure.

### Decision
We will use a flat hierarchy where all subprojects are top-level peers:

```
root/
├── dotfiles-packages/
├── dotfiles-wallpapers/
└── dotfiles-icon-templates/
```

### Rationale

**Chosen: Flat Hierarchy**

Advantages:
- Simpler mental model
- Each project equally accessible
- No unnecessary aggregation layer
- Cleaner workspace configuration
- Independent versioning easier
- Simpler import paths

**Rejected: Nested Hierarchy with Assets Aggregator**

Would have been better if:
- Logical grouping was essential for large number of asset types
- Needed to version/release assets as a single unit
- Strong domain boundary between "assets" and other concerns

### Consequences

**Positive:**
- Removed `assets` aggregator complexity
- Direct access to wallpapers and icon-templates
- Simpler CLI command structure (`dotfiles-config wallpapers` vs `dotfiles-config assets wallpapers`)

**Negative:**
- No logical grouping if more asset types are added
- Root namespace may become crowded with many projects

### Notes
If future asset types are added (e.g., fonts, themes), we may reconsider adding an assets aggregator or grouping mechanism.

---

## ADR-003: Dual Interface Pattern

### Status
Accepted

### Context
Users may want to interact with the system in different ways:
- Interactive terminal usage
- Shell scripts
- Python programs
- Other Python tools that compose functionality

We needed to decide how to expose functionality.

### Decision
Every project will expose both a CLI interface and a Python API interface.

```python
# CLI usage
$ dotfiles-wallpapers list

# Python API usage
from dotfiles_wallpapers import Wallpapers
wallpapers = Wallpapers()
wallpapers.list()
```

### Rationale

**Chosen: Dual Interface**

Advantages:
- Maximum flexibility for users
- CLI for interactive and scripted usage
- Python API for programmatic integration
- Same business logic serves both interfaces
- Enables composition in larger systems
- Testable at multiple levels

**Rejected: CLI Only**

Would have been sufficient if:
- Only terminal usage was expected
- No programmatic integration needed

**Rejected: API Only**

Would have been sufficient if:
- Only programmatic usage was expected
- CLI could be built separately

### Consequences

**Positive:**
- Users choose interface that fits their workflow
- API can be used by other Python tools
- CLI commands stay thin (delegate to API/Service)

**Negative:**
- More code to maintain (CLI + API layers)
- Must keep both interfaces in sync
- Documentation needed for both interfaces

---

## ADR-004: Naming Convention

### Status
Accepted

### Context
Project names, package names, and CLI commands need consistent naming. Python has conventions for package naming (lowercase, underscores for imports) and project naming varies.

We needed to establish a consistent naming convention.

### Decision
Use `dotfiles-` prefix for all projects with the following patterns:

| Type | Convention | Example |
|------|------------|---------|
| Project directory | kebab-case | `dotfiles-packages/` |
| Package name (pyproject.toml) | kebab-case | `dotfiles-packages` |
| Import path | snake_case | `dotfiles_packages` |
| CLI command | kebab-case | `dotfiles-packages` |

### Rationale

**Chosen: `dotfiles-` Prefix**

Advantages:
- Clear namespace identification
- Avoids conflicts with common package names (`packages`, `wallpapers`)
- Consistent branding across all projects
- Easy to identify related projects

**Rejected: No Prefix**

Would have caused:
- Potential naming conflicts
- Unclear relationship between projects
- Generic names (`packages`) are ambiguous

**Rejected: Different Prefix (e.g., `dc-`)**

Would have been:
- Less readable
- Unclear what `dc` stands for

### Consequences

**Positive:**
- Clear, unambiguous naming
- Easy to discover related packages
- Consistent user experience

**Negative:**
- Longer names to type
- Verbose import statements

---

## ADR-005: Fresh Test Suites

### Status
Accepted

### Context
The old project has existing tests. During refactoring, we could either:
1. Migrate existing tests to new structure
2. Create new tests from scratch

We needed to decide the test migration strategy.

### Decision
We will create fresh test suites rather than migrating existing tests.

### Rationale

**Chosen: Fresh Test Suites**

Advantages:
- Tests serve as specification for new architecture
- No assumptions from old structure carried over
- Opportunity to establish proper patterns
- Tests become "foundational truth" for documentation
- Ensures tests match new project structure
- Can improve test quality and coverage

**Rejected: Migrate Existing Tests**

Would have been better if:
- Existing tests were comprehensive and well-structured
- Time was critical
- Old and new architectures were similar

### Consequences

**Positive:**
- Clean slate for test design
- Tests accurately reflect new architecture
- Consistent test patterns across all projects

**Negative:**
- More initial effort
- May miss edge cases covered by old tests
- Temporary reduction in test coverage during transition

### Notes
Old tests should be consulted for edge cases and scenarios but not directly copied. Test cases from old tests can inform new test design.

---

## ADR-006: Layered Architecture

### Status
Accepted

### Context
Each subproject needs internal organization. We needed to decide how to structure the code within each project.

### Decision
Each subproject will follow a three-layer architecture:

```
project/
├── cli/          # CLI Layer - Typer commands
│   └── commands/
├── api/          # API Layer - Public Python interface
└── services/     # Service Layer - Business logic
```

**Layer Responsibilities:**

| Layer | Responsibility | Dependencies |
|-------|---------------|--------------|
| CLI | Argument parsing, output formatting, exit codes | API, Services |
| API | Public interface, convenience methods | Services |
| Services | Business logic, validation, I/O | None (external only) |

### Rationale

**Chosen: Three-Layer Architecture**

Advantages:
- Clear separation of concerns
- Services testable without CLI framework
- Services reusable across interfaces
- CLI stays thin (presentation only)
- API provides clean programmatic interface

**Rejected: Two-Layer (CLI + Services)**

Would have:
- Mixed CLI concerns with public API
- No clean programmatic interface

**Rejected: No Layers (Flat)**

Would have:
- Mixed responsibilities
- Hard to test
- Hard to maintain

### Consequences

**Positive:**
- Clear responsibility boundaries
- Each layer independently testable
- Easy to understand code organization
- Consistent across all projects

**Negative:**
- More files and directories
- Potential for over-abstraction in simple cases
- Need to decide which layer owns each piece of logic

### Implementation Notes

```python
# CLI Layer - handles presentation
@app.command()
def add(path: Path, force: bool = False):
    service = get_service()
    try:
        service.add_wallpaper(path, overwrite=force)
        typer.echo(f"Added {path.name}")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

# API Layer - clean interface
class Wallpapers:
    def add(self, path: Path, *, force: bool = False):
        self._service.add_wallpaper(path, overwrite=force)

# Service Layer - business logic
class WallpapersService:
    def add_wallpaper(self, path: Path, overwrite: bool):
        if not path.exists():
            raise WallpaperNotFoundError(...)
        # actual implementation
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | AI Assistant | Initial creation |
