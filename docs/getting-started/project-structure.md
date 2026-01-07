# Project Structure

[VERIFIED via CLI - 2026-01-03]

Understanding the repository layout and organization.

## Repository Overview

```
dotfiles/config/
├── assets/           - Binary assets (wallpapers, icons)
├── config-files/     - Application configuration files
├── docs/             - Documentation (this documentation)
├── packages/         - Package management (Ansible)
├── src/              - Python source code
├── tests/            - Test suite
├── Makefile          - Development commands
├── pyproject.toml    - Python project configuration
└── README.md         - Project README
```

[VERIFIED via CLI - 2026-01-03]

## Key Directories

### `/assets` - Binary Assets

Contains non-code assets like wallpapers and icons.

**Structure:**
```
assets/
├── screenshot-tool-icons/     - Icons for screenshot tools
├── status-bar-icons/          - Status bar icons (battery, network, etc.)
├── wallpapers/                - Wallpaper archive and management
└── wlogout-icons/             - Logout menu icons
```

[VERIFIED via CLI - 2026-01-03]

**Purpose:**
- Store binary files outside source control (or in compressed archives)
- Organize assets by category
- Provide management tools (CLI and scripts)

**Key Files:**
- `wallpapers/wallpapers.tar.gz` - Compressed wallpaper archive
- `wallpapers/manage_wallpapers.sh` - Bash management script
- Various `.svg` icon files

[VERIFIED via CLI - 2026-01-03]

### `/config-files` - Application Configurations

Contains configuration files for various applications.

**Structure:**
```
config-files/
├── nvim/              - Neovim configuration
│   ├── init.lua       - Main Neovim entry point
│   └── lua/           - Lua configuration modules
└── zsh/               - Zsh shell configuration
    └── .zshrc.j2      - Zsh config template
```

[VERIFIED via CLI - 2026-01-03]

**Purpose:**
- Store application configuration files
- Version control configurations
- Deploy via Ansible to system locations

**Deployment:**
- Ansible copies files from here to `~/.config/` (or `$XDG_CONFIG_HOME`)
- Jinja2 templates (`.j2`) are processed during deployment

[VERIFIED via source - 2026-01-03]

### `/docs` - Documentation

Complete project documentation (what you're reading now).

**Structure:**
```
docs/
├── getting-started/    - Installation and first steps
├── architecture/       - System design
├── reference/          - API and CLI reference
├── guides/             - How-to guides
├── examples/           - Practical examples
└── testing/            - Testing documentation
```

[VERIFIED via CLI - 2026-01-03]

**Purpose:**
- Comprehensive project documentation
- User guides and references
- Developer documentation

### `/packages` - Package Management

Ansible-based package installation and configuration.

**Structure:**
```
packages/
└── ansible/
    ├── ansible.cfg         - Ansible configuration
    ├── inventory/          - Inventory and variables
    │   ├── localhost.yml   - Local host definition
    │   └── group_vars/     - Group variables
    ├── playbooks/          - Playbooks and roles
    │   ├── bootstrap.yml   - Main playbook
    │   └── roles/          - Ansible roles
    └── README.md           - Ansible documentation
```

[VERIFIED via CLI - 2026-01-03]

**Purpose:**
- Install system packages
- Deploy configuration files
- Multi-distribution support

**Key Concepts:**
- **Playbook:** `bootstrap.yml` - Main entry point
- **Roles:** Modular configuration units (e.g., `nvim`)
- **Tags:** Selective execution (e.g., `--tags nvim`)
- **Variables:** Customizable paths and settings

[VERIFIED via source - 2026-01-03]

### `/src` - Python Source Code

CLI application and public API source code.

**Structure:**
```
src/
├── __init__.py              - Public API exports (Config, Assets, Packages, Wallpapers)
├── main.py                  - CLI entry point
├── api/                     - Public API layer
│   ├── __init__.py          - API exports
│   ├── config.py            - Config entry point class
│   ├── assets.py            - Assets facade class
│   ├── packages.py          - Packages API class
│   └── wallpapers.py        - Wallpapers API class
├── services/                - Business logic layer
│   ├── __init__.py
│   ├── packages_service.py  - Package management service
│   └── wallpapers_service.py - Wallpaper management service
└── commands/                - CLI command implementations
    ├── dummy.py             - Example command
    ├── install_packages.py  - Package installation
    └── assets/              - Asset management
        └── wallpapers/      - Wallpaper commands
            └── __init__.py  - add, extract, list commands
```

[VERIFIED via CLI - 2026-01-04]

**Organization Principles:**
- **main.py:** Application entry point, command registration
- **api/:** Public API layer providing high-level interfaces
- **services/:** Business logic layer (wallpapers, packages)
- **commands/:** CLI command implementations organized hierarchically
- **Separation:** API → Commands → Services (three-layer architecture)

[VERIFIED via source - 2026-01-04]

**Example Flow:**
1. User imports from `src` (or `src.api`)
2. `Config` class provides entry point via lazy-loaded properties
3. API classes wrap service layer
4. Services handle business logic
5. Commands use services for CLI operations

### `/tests` - Test Suite

Comprehensive test suite using pytest.

**Structure:**
```
tests/
├── conftest.py                 - Shared fixtures
├── unit/                       - Unit tests
│   └── test_wallpapers_service.py
└── integration/                - Integration tests
    └── test_wallpapers_cli.py
```

[VERIFIED via CLI - 2026-01-03]

**Test Organization:**
- **Unit tests:** Test individual components in isolation
- **Integration tests:** Test CLI commands end-to-end
- **Fixtures:** Shared test data and setup

**Running Tests:**
```bash
make test           # All tests
make test-unit      # Unit tests only
make test-integration  # Integration tests only
make test-cov       # Tests with coverage
```

[VERIFIED via source - 2026-01-03]

## Configuration Files

### `pyproject.toml`

Python project configuration.

**Contains:**
- Package metadata (name, version, description)
- Dependencies (typer)
- Development dependencies (pytest, pytest-cov)
- Console scripts entry point (`config = "src.main:main"`)
- Build system (hatchling)
- Tool configuration (pytest)

[VERIFIED via source - 2026-01-03]

### `Makefile`

Development task automation.

**Available Targets:**
```
make help              # Show available targets
make install           # Install package
make install-dev       # Install with dev dependencies
make shell             # Activate virtual environment
make clean             # Remove build artifacts
make test              # Run tests
make test-unit         # Run unit tests
make test-integration  # Run integration tests
make test-cov          # Run tests with coverage
```

[VERIFIED via source - 2026-01-03]

### `uv.lock`

Dependency lock file for reproducible installations.

[VERIFIED via CLI - 2026-01-03]

### `.python-version`

Specifies Python version for the project.

[VERIFIED via CLI - 2026-01-03]

## File Naming Conventions

### Python Files
- `snake_case.py` - Module files
- `__init__.py` - Package initialization
- `test_*.py` - Test files

### Configuration Files
- `.lua` - Lua files (Neovim)
- `.j2` - Jinja2 templates
- `.yml`, `.yaml` - YAML files (Ansible)
- `.md` - Markdown documentation

### Assets
- `.svg` - SVG icons
- `.tar.gz` - Compressed archives
- `.sh` - Shell scripts

[VERIFIED via CLI - 2026-01-03]

## Import Paths

The project uses absolute imports from the `src/` package:

**Top-level API (recommended):**
```python
from src import Config, Assets, Packages, Wallpapers
```

**Direct API imports:**
```python
from src.api import Config, Assets, Packages, Wallpapers
```

**Service layer imports (for advanced use):**
```python
from src.services.packages_service import PackagesService
from src.services.wallpapers_service import WallpapersService
```

**CLI imports (internal use):**
```python
from src.commands.packages import packages_app
from src.commands.assets.wallpapers import wallpapers_app
from src.main import main, app
```

[VERIFIED via source - 2026-01-04]

**pytest configuration** adds project root to Python path:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

[VERIFIED via source - 2026-01-04]

## Generated Files (Excluded from Git)

These files are generated during development:

- `.venv/` - Virtual environment
- `__pycache__/` - Python bytecode cache
- `.pytest_cache/` - pytest cache
- `.coverage` - Coverage data
- `build/`, `dist/`, `*.egg-info/` - Build artifacts

Clean with: `make clean`

[VERIFIED via source - 2026-01-03]

## Understanding the Flow

### User API Call → Result

```
Python code: cfg = Config(); cfg.assets.wallpapers.list()
                    ↓
          src/__init__.py (exports Config)
                    ↓
          src/api/config.py (Config class)
                    ↓
          src/api/assets.py (Assets facade)
                    ↓
          src/api/wallpapers.py (Wallpapers API)
                    ↓
          src/services/wallpapers_service.py (WallpapersService.list_wallpapers)
                    ↓
          File system (wallpapers.tar.gz)
                    ↓
          Return results to user
```

### User CLI Command → Output

```
User types: config assets wallpapers list
                    ↓
          src/main.py (app entry point)
                    ↓
          src/commands/assets/__init__.py (assets_app)
                    ↓
          src/commands/assets/wallpapers/__init__.py (list_wallpapers)
                    ↓
          src/services/wallpapers_service.py (WallpapersService.list_wallpapers)
                    ↓
          File system (wallpapers.tar.gz)
                    ↓
          Output to user
```

[VERIFIED via source - 2026-01-04]

## Where to Find Things

**Need to...** → **Look in...**

- Use the public API → `src/` (import Config) or `src/api/`
- Add a CLI command → `src/commands/`
- Add business logic → `src/services/`
- Add API class → `src/api/`
- Add tests → `tests/unit/` or `tests/integration/`
- Add configuration file → `config-files/<app>/`
- Add asset → `assets/<category>/`
- Add Ansible role → `packages/ansible/playbooks/roles/`
- Read documentation → `docs/`

## See Also

- [Directory Layout](../architecture/directory-layout.md) - Detailed directory structure
- [CLI Structure](../architecture/cli-structure.md) - How commands are organized
- [Installation](installation.md) - How to install the project
