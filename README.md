# Dotfiles Configuration System

[VERIFIED via source - 2026-01-03]

A Python-based CLI tool for managing dotfiles, system packages, and configuration files.

## Features

- **Wallpaper Management:** Manage wallpapers in compressed archives
- **Package Installation:** Install and configure system packages with Ansible
- **Type-Safe CLI:** Built with Typer for excellent UX
- **Well-Tested:** 81 tests with 83% coverage
- **Multi-Distribution:** Debian, Fedora, and Arch Linux support

[VERIFIED via tests - 2026-01-03]

## Quick Start

```bash
# Install
git clone <repository-url>
cd dotfiles/config
make install-dev
make shell

# Use
config --help
config assets wallpapers list
config install-packages --tags nvim --ask-become-pass

# Test
make test-cov
```

[VERIFIED via CLI - 2026-01-03]

## Documentation

Complete documentation is available in the [docs/](docs/index.md) directory:

- **[Getting Started](docs/getting-started/index.md)** - Installation and first steps
- **[CLI Reference](docs/reference/cli/index.md)** - Complete command reference
- **[Examples](docs/examples/index.md)** - Practical usage examples
- **[Development Guide](docs/guides/development/index.md)** - Contributing to the project
- **[Architecture](docs/architecture/index.md)** - System design
- **[Testing](docs/testing/index.md)** - Test documentation

## Installation

### Prerequisites

- Python 3.12 or higher
- Git
- Ansible 2.20+ (optional, for package installation)

[VERIFIED via source - 2026-01-03]

### Install

```bash
# Clone repository
git clone <repository-url>
cd dotfiles/config

# Install with development dependencies
make install-dev

# Activate virtual environment
make shell

# Verify installation
config --help
```

[VERIFIED via CLI - 2026-01-03]

See [Installation Guide](docs/getting-started/installation.md) for detailed instructions.

## Usage

### Manage Wallpapers

```bash
# List wallpapers
config assets wallpapers list

# Add wallpaper
config assets wallpapers add ~/Pictures/wallpaper.jpg

# Extract wallpapers
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

### Install Packages

```bash
# Install Neovim and configuration
config install-packages --tags nvim --ask-become-pass

# Show debug information
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

See [Usage Guides](docs/guides/usage/index.md) for more examples.

## Project Structure

```
.
├── assets/           - Binary assets (wallpapers, icons)
├── config-files/     - Application configuration files
├── docs/             - Complete documentation
├── packages/         - Package management (Ansible)
├── src/              - Python source code
├── tests/            - Test suite (81 tests, 83% coverage)
├── Makefile          - Development commands
└── pyproject.toml    - Python project configuration
```

[VERIFIED via CLI - 2026-01-03]

See [Project Structure](docs/getting-started/project-structure.md) for details.

## Development

```bash
# Setup
make install-dev
make shell

# Run tests
make test-cov

# Clean
make clean
```

[VERIFIED via source - 2026-01-03]

See [Development Guide](docs/guides/development/index.md) for:
- Setting up development environment
- Writing tests
- Adding new commands
- Code style guidelines

## Available Commands

### Core Commands

- `config install-packages` - Install packages using Ansible
- `config dummy` - Example dummy command

### Asset Management

- `config assets wallpapers list` - List wallpapers
- `config assets wallpapers add` - Add wallpaper
- `config assets wallpapers extract` - Extract wallpapers

[VERIFIED via CLI - 2026-01-03]

See [CLI Reference](docs/reference/cli/index.md) for complete documentation.

## Testing

```bash
# All tests
make test

# With coverage
make test-cov

# Unit tests only
make test-unit

# Integration tests only
make test-integration
```

[VERIFIED via tests - 2026-01-03]

**Test Statistics:**
- Total: 81 tests (all passing)
- Coverage: 83%
- Unit tests: 48
- Integration tests: 33

See [Testing Documentation](docs/testing/index.md) for details.

## Technology Stack

- **Python 3.12+** - Core language
- **Typer** - CLI framework
- **Ansible 2.20+** - Configuration management
- **pytest** - Testing framework
- **uv** - Package manager

[VERIFIED via source - 2026-01-03]

## Make Targets

```bash
make help              # Show available targets
make install           # Install package
make install-dev       # Install with dev dependencies
make shell             # Activate virtual environment
make clean             # Remove venv and build artifacts
make test              # Run all tests
make test-unit         # Run unit tests
make test-integration  # Run integration tests
make test-cov          # Run tests with coverage
```

[VERIFIED via source - 2026-01-03]

## License

<!-- TODO: Source not available -->

License information not yet specified.

## Support

For documentation, see the [docs/](docs/index.md) directory.

For development guidelines, see the [Development Guide](docs/guides/development/index.md).
