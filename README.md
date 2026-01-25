# dotfiles-config

Comprehensive configuration management system for dotfiles with modular architecture.

## Overview

`dotfiles-config` is a unified CLI and Python library for managing three complementary subsystems:

1. **Packages** - Ansible-based role and package installation
2. **Wallpapers** - Image archive management and extraction
3. **Icon Templates** - Icon template organization and copying

Each subsystem can be used independently or orchestrated together through a unified interface.

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd dotfiles-config

# Install all modules
uv sync
```

### Basic Usage

```bash
# Show all available commands
dotfiles-config --help

# Manage packages
dotfiles-config packages list
dotfiles-config packages install --tags core

# Manage wallpapers
dotfiles-config wallpapers list
dotfiles-config wallpapers add wallpapers.tar.gz image.jpg
dotfiles-config wallpapers extract wallpapers.tar.gz ~/Pictures

# Manage icon templates
dotfiles-config icon-templates list
dotfiles-config icon-templates list --category status-bar
dotfiles-config icon-templates copy ~/icons --category status-bar
```

## Architecture

### Modular Design

The project uses a **layered, modular architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Root CLI Layer                        │
│              (dotfiles_config.cli)                       │
│  ┌──────────────┬──────────────┬──────────────────────┐ │
│  │   Packages   │  Wallpapers  │  Icon Templates      │ │
│  │   Commands   │   Commands   │   Commands           │ │
│  └──────┬───────┴──────┬───────┴──────────┬───────────┘ │
└─────────┼──────────────┼──────────────────┼─────────────┘
          │              │                  │
      ┌───▼──────┐  ┌────▼───────┐  ┌──────▼──────┐
      │ Packages │  │ Wallpapers │  │ Icon        │
      │   API    │  │    API     │  │ Templates   │
      │          │  │            │  │ API         │
      └───┬──────┘  └────┬───────┘  └──────┬──────┘
          │              │                  │
      ┌───▼──────────────▼──────────────────▼──────┐
      │    Service Layer (Business Logic)          │
      │                                            │
      │ • PackagesService (Ansible integration)    │
      │ • WallpapersService (Archive operations)   │
      │ • IconTemplatesService (File operations)   │
      └────────────────────────────────────────────┘
```

### Key Design Principles

1. **Layered Architecture**: CLI → API → Service layers
2. **Modular Independence**: Each subsystem can be used separately
3. **Clear Separation**: Service, API, and CLI concerns clearly separated
4. **Exception Handling**: Specific exception types for error scenarios
5. **Testing**: Unit tests for services/APIs, integration tests for CLI
6. **Type Safety**: Python 3.12+ with type annotations

## Project Structure

```
dotfiles-config/
├── dotfiles-packages/              # Ansible playbook management
│   ├── src/dotfiles_packages/
│   ├── tests/
│   └── README.md
├── dotfiles-wallpapers/            # Wallpaper archive management
│   ├── src/dotfiles_wallpapers/
│   ├── tests/
│   └── README.md
├── dotfiles-icon-templates/        # Icon template management
│   ├── data/                       # Icon templates by category
│   ├── src/dotfiles_icon_templates/
│   ├── tests/
│   └── README.md
├── src/dotfiles_config/            # Root package
│   ├── __init__.py                 # Aggregates all APIs
│   ├── cli/
│   │   └── __init__.py             # Root CLI aggregation
│   └── exceptions.py               # Shared exceptions
├── tests/
│   ├── unit/                       # Service/API unit tests
│   └── integration/                # CLI integration tests
├── pyproject.toml                  # Workspace configuration
├── README.md                       # This file
└── docs/
    └── planning/                   # Project planning documents
```

## Modules

### dotfiles-packages

Ansible playbook and role management.

**Key Features:**
- List available roles from playbooks
- Install roles with tag filtering
- Ansible integration with subprocess

**Usage:**
```bash
dotfiles-config packages list
dotfiles-config packages install --tags core --tags optional
```

See [dotfiles-packages/README.md](dotfiles-packages/README.md) for details.

### dotfiles-wallpapers

Wallpaper archive management.

**Key Features:**
- List images in tar.gz archives
- Add wallpapers with validation
- Extract archives to directories
- Support for JPEG, PNG, WebP, GIF, BMP, TIFF

**Usage:**
```bash
dotfiles-config wallpapers list archive.tar.gz
dotfiles-config wallpapers add archive.tar.gz image.jpg
dotfiles-config wallpapers extract archive.tar.gz ~/Pictures
```

See [dotfiles-wallpapers/README.md](dotfiles-wallpapers/README.md) for details.

### dotfiles-icon-templates

Icon template organization and copying.

**Key Features:**
- Organize icons by category
- List and show icon information
- Copy icons with flexible filtering
- Category-based organization

**Usage:**
```bash
dotfiles-config icon-templates list --category status-bar
dotfiles-config icon-templates copy ~/icons --category status-bar
dotfiles-config icon-templates show battery.svg
```

See [dotfiles-icon-templates/README.md](dotfiles-icon-templates/README.md) for details.

## Python API

Use the unified API to orchestrate multiple subsystems:

```python
from dotfiles_config import Packages, Wallpapers, IconTemplates

# Initialize all subsystems
packages = Packages()
wallpapers = Wallpapers()
icons = IconTemplates()

# Package management
roles = packages.list_packages()
packages.install(tags=["core"])

# Wallpaper management
images = wallpapers.list_wallpapers("wallpapers.tar.gz")
wallpapers.extract_wallpapers("wallpapers.tar.gz", "~/Pictures")

# Icon template management
categories = icons.categories()
icons.copy("~/icons", category="status-bar")
```

## Testing

### Run All Tests

```bash
# Install dependencies
uv sync

# Run full test suite
uv run pytest

# Run with coverage
uv run pytest --cov=dotfiles_config --cov=dotfiles_packages --cov=dotfiles_wallpapers --cov=dotfiles_icon_templates
```

### Test Organization

```
tests/
├── unit/                          # Service/API unit tests
│   ├── test_packages_service.py
│   ├── test_packages_api.py
│   ├── test_wallpapers_service.py
│   ├── test_wallpapers_api.py
│   ├── test_icon_templates_service.py
│   └── test_icon_templates_api.py
└── integration/                   # CLI integration tests
    ├── test_packages_cli.py
    ├── test_wallpapers_cli.py
    ├── test_icon_templates_cli.py
    └── test_root_cli_hierarchy.py
```

### Test Coverage

- **Unit Tests**: Service layer business logic, API delegation, data models
- **Integration Tests**: CLI commands, error scenarios, command chaining
- **Mocking**: External commands (Ansible, archive operations) are mocked

## Development

### Adding a New Module

To add a new subsystem (e.g., `dotfiles-configs`):

1. Create module structure:
   ```
   dotfiles-configs/
   ├── src/dotfiles_configs/
   │   ├── __init__.py
   │   ├── api/
   │   ├── cli/
   │   ├── services/
   │   └── exceptions.py
   ├── tests/
   └── pyproject.toml
   ```

2. Implement layered architecture following existing patterns

3. Add to root `src/dotfiles_config/__init__.py`:
   ```python
   from dotfiles_configs import Configs
   __all__ = [..., "Configs"]
   ```

4. Add to root CLI in `src/dotfiles_config/cli/__init__.py`:
   ```python
   from dotfiles_configs.cli import app as configs_app
   app.add_typer(configs_app, name="configs")
   ```

### Running Locally

```bash
# Install in development mode
uv sync

# Run CLI
uv run dotfiles-config --help
uv run dotfiles-config packages list

# Run tests
uv run pytest tests/
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -v
```

## Configuration

Configuration locations (in order of precedence):

1. **CLI Arguments**: Direct command-line options
2. **Environment Variables**: `DOTFILES_*` prefix
3. **Config Files**: `~/.config/dotfiles/config.yaml`
4. **Defaults**: Built-in defaults

### Environment Variables

```bash
# Package configuration
export DOTFILES_PLAYBOOK=/path/to/playbook.yml

# Wallpaper configuration
export DOTFILES_ARCHIVE_DIR=/path/to/archives

# Icon template configuration
export DOTFILES_ICON_DATA=/path/to/icon/data
```

## Dependencies

### Core Dependencies

- **Python**: 3.12+
- **typer**: 0.9.0+ (CLI framework)
- **pyyaml**: (YAML parsing for packages)

### Optional Dependencies

- **ansible**: For package installation (runtime only)

### Development Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **uv**: Package/workspace management

## Error Handling

Each module exports specific exception types:

```python
from dotfiles_packages import PackagesError, AnsibleError
from dotfiles_wallpapers import WallpapersError, InvalidImageError
from dotfiles_icon_templates import IconTemplateError, CategoryNotFoundError

try:
    packages.install(tags=["core"])
except AnsibleError as e:
    print(f"Ansible failed: {e.return_code}")
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'dotfiles_*'`

**Solution**: Run `uv sync` to install all modules

**Issue**: Ansible not found when installing packages

**Solution**: Install Ansible separately or ensure it's in PATH

**Issue**: Permission denied when copying/extracting files

**Solution**: Ensure write permissions on target directories

## Contributing

When contributing:

1. Follow the layered architecture pattern
2. Add unit tests for service logic
3. Add integration tests for CLI
4. Update documentation (docstrings, README)
5. Run `uv run pytest` to ensure tests pass

## License

MIT
