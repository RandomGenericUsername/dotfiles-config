# Architecture

[VERIFIED via source - 2026-01-03]

System architecture and design documentation for the dotfiles-config project.

## Contents

### [CLI Structure](cli-structure.md)

How the command-line interface is organized and how commands are registered.

- Typer application hierarchy
- Command registration patterns
- Context passing and argument forwarding

### [Directory Layout](directory-layout.md)

Complete project directory structure and organization.

- Source code organization
- Asset management
- Configuration files
- Test structure

### [Integration Points](integration-points.md)

How different components interact with each other and with external systems.

- Python CLI ↔ Ansible integration
- Asset management workflows
- Configuration deployment

### [Design Principles](design-principles.md)

Core design decisions and architectural patterns.

- Separation of concerns
- Service layer pattern
- Error handling strategy
- Testing philosophy

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    config CLI                           │
│                   (Typer Application)                    │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼──────────────┐
            │               │              │
            ▼               ▼              ▼
    ┌─────────────┐  ┌──────────┐  ┌──────────────┐
    │   dummy     │  │install-  │  │   assets     │
    │  (example)  │  │packages  │  │   (group)    │
    └─────────────┘  └──────────┘  └──────────────┘
                            │              │
                            │              ▼
                            │       ┌──────────────┐
                            │       │  wallpapers  │
                            │       │   (group)    │
                            │       └──────────────┘
                            │              │
                            │    ┌─────────┼────────┐
                            │    │         │        │
                            │    ▼         ▼        ▼
                            │  ┌────┐  ┌─────┐  ┌───────┐
                            │  │add │  │list │  │extract│
                            │  └────┘  └─────┘  └───────┘
                            │                       │
                            │                       ▼
                            │             ┌──────────────────┐
                            │             │WallpapersService │
                            │             │  (service layer) │
                            │             └──────────────────┘
                            ▼
                    ┌──────────────┐
                    │   Ansible    │
                    │   Playbook   │
                    └──────────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                    ▼               ▼
            ┌─────────────┐  ┌─────────────┐
            │Config Files │  │  Packages   │
            │ Deployment  │  │Installation │
            └─────────────┘  └─────────────┘
```

[VERIFIED via source - 2026-01-03]

## Technology Stack

**Core:**
- Python 3.12+
- Typer (CLI framework)
- uv (package manager)

**Configuration Management:**
- Ansible 2.20+
- Jinja2 (templating)

**Testing:**
- pytest
- pytest-cov

**Build:**
- Hatchling (build backend)

[VERIFIED via source - 2026-01-03]

## Key Architectural Decisions

### 1. CLI Framework: Typer

Typer provides automatic help generation, type checking, and shell completion.

[VERIFIED via source - 2026-01-03]

### 2. Service Layer Pattern

Business logic separated from CLI commands for testability and reusability.

Example: `WallpapersService` handles archive operations independently of CLI.

[VERIFIED via source - 2026-01-03]

### 3. Ansible Integration

Package installation and configuration deployment delegated to Ansible for:
- Multi-distribution support
- Idempotent operations
- Mature ecosystem

[VERIFIED via source - 2026-01-03]

### 4. Asset Archives

Wallpapers stored in tar.gz format for:
- Version control efficiency (single compressed file)
- Easy extraction and management
- Standard format with wide tooling support

[VERIFIED via source - 2026-01-03]

## See Also

- [CLI Reference](../reference/cli/index.md)
- [Python API Reference](../reference/python-api/index.md)
- [Development Guide](../guides/development/index.md)
