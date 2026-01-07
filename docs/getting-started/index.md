# Getting Started

[VERIFIED via source - 2026-01-03]

Quick start guide for the dotfiles-config system.

## Contents

- [Installation](installation.md) - Install the dotfiles-config CLI
- [First Steps](first-steps.md) - Basic usage and commands
- [Project Structure](project-structure.md) - Understanding the repository layout

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd dotfiles/config
```

### 2. Install Dependencies

```bash
make install-dev
```

[VERIFIED via source - 2026-01-03]

This creates a virtual environment and installs the package with development dependencies.

### 3. Activate Virtual Environment

```bash
make shell
```

[VERIFIED via source - 2026-01-03]

Or manually:

```bash
source .venv/bin/activate
```

### 4. Verify Installation

```bash
config --help
```

[VERIFIED via CLI - 2026-01-03]

You should see the CLI help output with available commands.

### 5. Run Tests

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-03]

All 81 tests should pass with 83% coverage.

## What's Next?

- **Install System Packages:** Use `config install-packages` to install and configure system packages
- **Manage Wallpapers:** Use `config assets wallpapers` to manage wallpaper collection
- **Explore Documentation:** Browse the complete [reference documentation](../reference/index.md)

## System Requirements

**Required:**
- Python 3.12 or higher
- Git

**Optional:**
- Ansible 2.20+ (for package installation)
- uv package manager (recommended)

[VERIFIED via source - 2026-01-03]

## See Also

- [Installation Guide](installation.md) - Detailed installation instructions
- [CLI Reference](../reference/cli/index.md) - Complete command reference
- [Architecture](../architecture/index.md) - System design overview
