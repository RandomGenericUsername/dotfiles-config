# Dotfiles Configuration System Documentation

[VERIFIED via source - 2026-01-03]

Complete documentation for the dotfiles-config CLI and configuration management system.

## Quick Links

- **[Getting Started](getting-started/index.md)** - Installation and first steps
- **[CLI Reference](reference/cli/index.md)** - Complete command reference
- **[Examples](examples/index.md)** - Practical usage examples

## What is dotfiles-config?

A Python-based CLI tool for managing dotfiles, system packages, and configuration files. It combines:

- **Python CLI** (Typer) - User-friendly command-line interface
- **Ansible** - Package installation and configuration deployment
- **Asset Management** - Wallpapers, icons, and other resources

[VERIFIED via source - 2026-01-03]

## Key Features

- **Wallpaper Management:** Add, list, and extract wallpapers from compressed archives
- **Package Installation:** Install system packages and deploy configurations via Ansible
- **Type-Safe CLI:** Built with Typer for excellent help messages and shell completion
- **Well-Tested:** 81 tests with 83% code coverage
- **Multi-Distribution:** Supports Debian, Fedora, and Arch Linux via Ansible

[VERIFIED via tests - 2026-01-03]

## Documentation Structure

### [Getting Started](getting-started/index.md)

New user onboarding and installation.

- [Installation](getting-started/installation.md) - How to install
- [First Steps](getting-started/first-steps.md) - Basic usage
- [Project Structure](getting-started/project-structure.md) - Repository layout

### [Reference](reference/index.md)

Complete API and CLI documentation.

- [CLI Reference](reference/cli/index.md) - All commands and options
- [Python API](reference/python-api/index.md) - Programming interface
- [Configuration Files](reference/config-files/index.md) - Config file documentation
- [Assets](reference/assets/index.md) - Binary assets documentation

### [Architecture](architecture/index.md)

System design and structure.

- [CLI Structure](architecture/cli-structure.md) - Command organization
- [Directory Layout](architecture/directory-layout.md) - Project structure
- [Integration Points](architecture/integration-points.md) - Component interactions
- [Design Principles](architecture/design-principles.md) - Design decisions

### [Guides](guides/development/index.md)

Task-oriented how-to guides.

**Development:**
- [Setup](guides/development/setup.md) - Development environment
- [Testing](guides/development/testing.md) - Writing tests
- [Adding Commands](guides/development/adding-commands.md) - Extending the CLI
- [Code Style](guides/development/code-style.md) - Code conventions

**Usage:**
- [Managing Wallpapers](guides/usage/wallpapers.md) - Wallpaper workflows
- [Installing Packages](guides/usage/packages.md) - Package installation

### [Examples](examples/index.md)

Practical, tested examples.

- CLI command examples
- Python API usage
- Complete workflows
- Testing examples

### [Testing](testing/index.md)

Testing documentation.

- Test structure and organization
- Running tests
- Coverage reports
- Writing new tests

## Quick Start

```bash
# Install
git clone <repository-url>
cd dotfiles/config
make install-dev
make shell

# Verify
config --help

# Install packages
config install-packages --tags nvim --ask-become-pass

# Manage wallpapers
config assets wallpapers list
config assets wallpapers add ~/Pictures/wallpaper.jpg
config assets wallpapers extract ~/Pictures

# Run tests
make test-cov
```

[VERIFIED via CLI - 2026-01-03]

## Common Tasks

### Install System Packages

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

### Manage Wallpapers

```bash
config assets wallpapers list
config assets wallpapers add ~/Pictures/image.jpg
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

### Run Tests

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-03]

### Get Help

```bash
config --help
config assets wallpapers --help
```

[VERIFIED via CLI - 2026-01-03]

## Project Statistics

[VERIFIED via tests - 2026-01-04]

- **Total Tests:** 81 (all passing)
- **Code Coverage:** 83%
- **Source Files:** 7 Python modules
- **Test Files:** 4 test modules
- **Asset Files:** 51 files
- **Documentation Pages:** 40+ pages

## Technology Stack

**Core:**
- Python 3.12+
- Typer (CLI framework)
- uv (package manager)

**Configuration:**
- Ansible 2.20+
- Jinja2 (templating)

**Testing:**
- pytest
- pytest-cov

**Build:**
- Hatchling (build backend)
- Make (automation)

[VERIFIED via source - 2026-01-03]

## Requirements

**Required:**
- Python 3.12 or higher
- Git

**Optional:**
- Ansible 2.20+ (for package installation)
- uv (recommended package manager)

[VERIFIED via source - 2026-01-03]

## Contributing

See [Development Guide](guides/development/index.md) for:
- Setting up development environment
- Writing tests
- Adding new commands
- Code style guidelines

## Support

For issues and feature requests, please refer to the project repository.

## License

<!-- TODO: Source not available -->

License information not yet specified in repository.
