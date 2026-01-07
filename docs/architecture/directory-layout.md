# Directory Layout

[VERIFIED via CLI - 2026-01-03]

Complete project directory structure and organization.

## Full Directory Tree

```
.
├── assets/                            - Binary assets (icons, wallpapers, etc.)
│   ├── screenshot-tool-icons/
│   │   └── default/
│   ├── status-bar-icons/
│   │   ├── battery-icons/
│   │   ├── email-client-icon/
│   │   ├── network-icons/
│   │   ├── power-menu-icons/
│   │   └── wallpaper-selector-icons/
│   ├── wallpapers/
│   │   ├── manage_wallpapers.sh
│   │   ├── README.md
│   │   └── wallpapers.tar.gz          - Wallpaper archive
│   └── wlogout-icons/
│       └── templates/
├── config-files/                      - Application configuration files
│   ├── nvim/                          - Neovim configuration
│   │   ├── init.lua
│   │   └── lua/
│   │       ├── options.lua
│   │       └── plugins/               - Plugin configurations
│   └── zsh/                           - Zsh configuration
│       └── .zshrc.j2                  - Zsh config template
├── docs/                              - Documentation
│   ├── getting-started/
│   ├── architecture/
│   ├── reference/
│   │   ├── cli/
│   │   ├── python-api/
│   │   ├── config-files/
│   │   └── assets/
│   ├── guides/
│   │   ├── development/
│   │   ├── usage/
│   │   └── integration/
│   ├── examples/
│   └── testing/
├── packages/                          - Package management
│   └── ansible/                       - Ansible-based package installer
│       ├── ansible.cfg
│       ├── docs/
│       ├── inventory/
│       │   ├── group_vars/
│       │   │   └── all.yml            - Global Ansible variables
│       │   └── localhost.yml
│       ├── playbooks/
│       │   ├── bootstrap.yml          - Main playbook
│       │   └── roles/
│       │       └── features/
│       │           └── nvim/          - Neovim role
│       │               ├── defaults/main.yml
│       │               ├── tasks/main.yml
│       │               └── vars/main.yml
│       └── README.md
├── src/                               - Python source code
│   ├── __init__.py                    - Public API exports
│   ├── api/                           - Public API layer
│   │   ├── __init__.py                - API exports
│   │   ├── config.py                  - Config entry point
│   │   ├── assets.py                  - Assets facade
│   │   ├── packages.py                - Packages API
│   │   └── wallpapers.py              - Wallpapers API
│   ├── services/                      - Business logic layer
│   │   ├── __init__.py
│   │   ├── packages_service.py        - PackagesService
│   │   └── wallpapers_service.py      - WallpapersService
│   ├── commands/                      - CLI command implementations
│   │   ├── assets/                    - Asset management commands
│   │   │   ├── __init__.py            - Assets command group
│   │   │   └── wallpapers/            - Wallpaper commands
│   │   │       └── __init__.py        - CLI commands
│   │   ├── __init__.py
│   │   ├── dummy.py                   - Example command
│   │   └── install_packages.py        - Package installation
│   └── main.py                        - CLI application entry point
├── tests/                             - Test suite
│   ├── conftest.py                    - Shared test fixtures
│   ├── __init__.py
│   ├── integration/                   - Integration tests
│   │   ├── __init__.py
│   │   └── test_wallpapers_cli.py     - Wallpapers CLI tests
│   └── unit/                          - Unit tests
│       ├── __init__.py
│       └── test_wallpapers_service.py - WallpapersService tests
├── .coverage                          - Coverage data (generated)
├── .python-version                    - Python version specification
├── Makefile                           - Development commands
├── pyproject.toml                     - Python project configuration
├── README.md                          - Project README
├── REPOSITORY_DOCS_REQUIREMENTS.md    - Documentation requirements
└── uv.lock                            - Dependency lock file
```

[VERIFIED via CLI - 2026-01-03]

## Directory Descriptions

### `/assets`

Binary assets used in the dotfiles configuration.

**Subdirectories:**
- `screenshot-tool-icons/` - Icons for screenshot tools
- `status-bar-icons/` - Status bar icons (battery, network, email, power, wallpaper selector)
- `wallpapers/` - Wallpaper archive and management script
- `wlogout-icons/` - Logout menu icons

[VERIFIED via CLI - 2026-01-03]

### `/config-files`

Configuration files for various applications.

**Subdirectories:**
- `nvim/` - Neovim configuration (Lua-based)
- `zsh/` - Zsh configuration (Jinja2 template)

[VERIFIED via CLI - 2026-01-03]

### `/docs`

Project documentation (this documentation).

**Subdirectories:**
- `getting-started/` - Installation and first steps
- `architecture/` - System design and structure
- `reference/` - Complete API and CLI reference
- `guides/` - How-to guides for common tasks
- `examples/` - Practical examples
- `testing/` - Testing documentation

[VERIFIED via source - 2026-01-03]

### `/packages`

Package management systems.

**Subdirectories:**
- `ansible/` - Ansible-based package installation and configuration deployment

[VERIFIED via CLI - 2026-01-03]

### `/src`

Python source code for the CLI application and public API.

**Structure:**
- `__init__.py` - Public API exports
- `main.py` - Application entry point
- `api/` - Public API layer
  - `config.py` - Config entry point
  - `assets.py`, `packages.py`, `wallpapers.py` - API classes
- `services/` - Business logic layer
  - `packages_service.py` - PackagesService
  - `wallpapers_service.py` - WallpapersService
- `commands/` - CLI implementations
  - Individual command modules
  - Command groups (e.g., `assets/`)

[VERIFIED via CLI - 2026-01-04]

### `/tests`

Test suite using pytest.

**Structure:**
- `conftest.py` - Shared fixtures
- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for CLI commands

[VERIFIED via CLI - 2026-01-03]

## File Naming Conventions

### Python Files

- `snake_case.py` for modules
- `__init__.py` for package initialization
- `test_*.py` for test files

[VERIFIED via CLI - 2026-01-03]

### Configuration Files

- `.lua` for Neovim configuration
- `.j2` for Jinja2 templates
- `.yml` for Ansible files
- `.svg` for icon assets
- `.tar.gz` for compressed archives

[VERIFIED via CLI - 2026-01-03]

## Generated Files

These files are generated and excluded from version control:

- `.coverage` - Coverage data
- `.pytest_cache/` - pytest cache
- `__pycache__/` - Python bytecode cache
- `.venv/` - Virtual environment
- `*.egg-info/` - Package metadata

[VERIFIED via source - 2026-01-03]

## Configuration Files

### `pyproject.toml`

Python project configuration including:
- Package metadata
- Dependencies
- Build system
- Tool configuration (pytest)

[VERIFIED via source - 2026-01-03]

### `Makefile`

Development commands for:
- Virtual environment setup
- Dependency installation
- Test execution
- Cleanup

[VERIFIED via source - 2026-01-03]

### `uv.lock`

Dependency lock file managed by uv package manager.

[VERIFIED via CLI - 2026-01-03]

## Source Code Organization Principles

### 1. Command/Service Separation

Commands handle CLI concerns (argument parsing, output formatting).

Services handle business logic (archive operations, file management).

**Example:**
- Command: `src/commands/assets/wallpapers/__init__.py`
- Service: `src/commands/assets/wallpapers/service.py`

[VERIFIED via source - 2026-01-03]

### 2. Hierarchical Command Groups

Commands organized in a hierarchy matching CLI structure.

```
src/commands/
├── assets/              (command group)
│   └── wallpapers/      (command group)
│       └── add/list/extract (commands)
```

[VERIFIED via CLI - 2026-01-03]

### 3. Package Initialization

`__init__.py` files export public APIs and register commands.

**Example:** `src/commands/assets/__init__.py` exports `assets_app`

[VERIFIED via source - 2026-01-03]

## Asset Organization

Assets are organized by category and variant:

```
assets/
└── category-name/
    └── variant-name/
        └── asset-file.svg
```

[VERIFIED via CLI - 2026-01-03]

## See Also

- [CLI Structure](cli-structure.md)
- [Integration Points](integration-points.md)
- [Project Structure Guide](../getting-started/project-structure.md)
