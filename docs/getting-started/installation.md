# Installation

[VERIFIED via source - 2026-01-03]

Complete installation guide for the dotfiles-config system.

## Prerequisites

### Required

**Python 3.12 or higher**

[VERIFIED via source - 2026-01-03]

Check your Python version:

```bash
python3 --version
```

Install Python 3.12+ if needed:

```bash
# Arch Linux
sudo pacman -S python

# Debian/Ubuntu
sudo apt install python3.12

# Fedora
sudo dnf install python3.12
```

**Git**

```bash
# Arch Linux
sudo pacman -S git

# Debian/Ubuntu
sudo apt install git

# Fedora
sudo dnf install git
```

### Optional

**uv (Recommended Package Manager)**

uv is a fast Python package manager that's faster than pip.

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Ansible (For Package Installation)**

[VERIFIED via source - 2026-01-03]

Required if you want to use `config install-packages`.

```bash
# Using pipx (recommended)
pipx install ansible-core

# Using pip
pip install ansible-core

# Using system package manager
sudo pacman -S ansible        # Arch Linux
sudo apt install ansible      # Debian/Ubuntu
sudo dnf install ansible      # Fedora
```

Verify Ansible version:

```bash
ansible --version
```

Required: Ansible 2.20+

[VERIFIED via source - 2026-01-03]

## Installation Methods

### Method 1: Development Installation (Recommended)

For development and testing.

**Step 1: Clone Repository**

```bash
git clone <repository-url>
cd dotfiles/config
```

**Step 2: Install with Development Dependencies**

Using Make:

```bash
make install-dev
```

[VERIFIED via source - 2026-01-03]

Or manually:

```bash
uv venv
uv pip install -e ".[dev]"
```

[VERIFIED via source - 2026-01-03]

**Step 3: Activate Virtual Environment**

Using Make:

```bash
make shell
```

[VERIFIED via source - 2026-01-03]

Or manually:

```bash
source .venv/bin/activate
```

**Step 4: Verify Installation**

```bash
config --version
config --help
```

[VERIFIED via CLI - 2026-01-03]

### Method 2: Production Installation

For regular usage without development tools.

**Step 1: Clone Repository**

```bash
git clone <repository-url>
cd dotfiles/config
```

**Step 2: Install Package**

Using Make:

```bash
make install
```

[VERIFIED via source - 2026-01-03]

Or manually:

```bash
uv venv
uv pip install -e .
```

[VERIFIED via source - 2026-01-03]

**Step 3: Activate Virtual Environment**

```bash
source .venv/bin/activate
```

**Step 4: Verify Installation**

```bash
config --help
```

[VERIFIED via CLI - 2026-01-03]

## Post-Installation

### Enable Shell Completion

Install shell completion for your shell:

```bash
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

Restart your shell or source your shell configuration.

### Verify All Components

**Check CLI is working:**

```bash
config dummy
```

[VERIFIED via CLI - 2026-01-03]

Output: `This is a dummy command! It doesn't do much, but it works!`

**Check Ansible integration (if installed):**

```bash
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

**Check wallpaper management:**

```bash
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

**Run tests (development installation only):**

```bash
make test
```

[VERIFIED via tests - 2026-01-03]

All 81 tests should pass.

## Troubleshooting

### Issue: `config: command not found`

**Cause:** Virtual environment not activated or package not installed.

**Solution:**

```bash
source .venv/bin/activate
```

Or reinstall:

```bash
make install-dev
```

### Issue: `ModuleNotFoundError: No module named 'typer'`

**Cause:** Dependencies not installed.

**Solution:**

```bash
uv pip install -e ".[dev]"
```

### Issue: `ansible-playbook: command not found`

**Cause:** Ansible not installed.

**Solution:**

Install Ansible (see Prerequisites section above).

Note: Ansible is only required for `config install-packages` command.

### Issue: Python version too old

**Cause:** Python version below 3.12.

**Solution:**

Install Python 3.12 or higher. Check system-specific instructions in Prerequisites.

### Issue: Tests failing

**Cause:** Various reasons.

**Solution:**

1. Ensure all dependencies are installed:
   ```bash
   uv pip install -e ".[dev]"
   ```

2. Check test output for specific errors:
   ```bash
   uv run pytest -v
   ```

3. Verify Python version:
   ```bash
   python3 --version
   ```

## Uninstallation

### Remove Virtual Environment

```bash
make clean
```

[VERIFIED via source - 2026-01-03]

Or manually:

```bash
rm -rf .venv
```

### Remove Build Artifacts

```bash
make clean
```

This removes:
- Virtual environment (`.venv/`)
- Build directories (`build/`, `dist/`, `*.egg-info/`)
- Python cache (`__pycache__/`, `*.pyc`)

[VERIFIED via source - 2026-01-03]

## Upgrading

To upgrade to the latest version:

```bash
git pull
make clean
make install-dev
```

## Development Setup

For contributing to the project:

**Step 1: Install Development Dependencies**

```bash
make install-dev
```

[VERIFIED via source - 2026-01-03]

**Step 2: Run Tests**

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-03]

**Step 3: Check Available Make Targets**

```bash
make help
```

[VERIFIED via source - 2026-01-03]

Output shows all available commands:
- `install` - Create venv and install dependencies
- `install-dev` - Install with dev dependencies
- `shell` - Start a new shell with venv activated
- `clean` - Remove venv and build artifacts
- `test` - Run pytest tests
- `test-unit` - Run unit tests only
- `test-integration` - Run integration tests only
- `test-cov` - Run tests with coverage report

## See Also

- [First Steps](first-steps.md) - Getting started with basic usage
- [Development Guide](../guides/development/index.md) - Contributing to the project
- [CLI Reference](../reference/cli/index.md) - Complete command reference
