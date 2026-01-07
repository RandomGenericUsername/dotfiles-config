# Development Setup

[VERIFIED via source - 2026-01-03]

Complete guide for setting up a development environment.

## Prerequisites

- Python 3.12 or higher
- Git
- uv (recommended) or pip

[VERIFIED via source - 2026-01-03]

## Step-by-Step Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd dotfiles/config
```

### 2. Install Development Dependencies

Using Make (recommended):

```bash
make install-dev
```

[VERIFIED via source - 2026-01-03]

This creates a virtual environment (`.venv/`) and installs the package in editable mode with development dependencies.

Manual installation:

```bash
uv venv
uv pip install -e ".[dev]"
```

[VERIFIED via source - 2026-01-03]

### 3. Activate Virtual Environment

Using Make:

```bash
make shell
```

[VERIFIED via source - 2026-01-03]

Manual activation:

```bash
source .venv/bin/activate
```

### 4. Verify Installation

```bash
# Check CLI works
config --help

# Run tests
make test

# Check coverage
make test-cov
```

[VERIFIED via tests - 2026-01-03]

All 81 tests should pass with 83% coverage.

## Development Tools

### Make Targets

```bash
make help              # Show all available targets
make install           # Install package
make install-dev       # Install with dev dependencies
make shell             # Activate virtual environment
make clean             # Remove venv and build artifacts
make test              # Run all tests
make test-unit         # Run unit tests only
make test-integration  # Run integration tests only
make test-cov          # Run tests with coverage
```

[VERIFIED via source - 2026-01-03]

### Running Tests

**All tests:**
```bash
make test
```

**With coverage:**
```bash
make test-cov
```

**Specific test file:**
```bash
uv run pytest tests/unit/test_wallpapers_service.py -v
```

**Specific test:**
```bash
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd::test_add_wallpaper_to_existing_archive -v
```

**List tests without running:**
```bash
uv run pytest --collect-only
```

[VERIFIED via tests - 2026-01-03]

### Code Formatting

Currently no automated formatter configured.

<!-- TODO: Source not available -->

Future: Consider adding black or ruff for code formatting.

### Type Checking

Currently no automated type checking.

<!-- TODO: Source not available -->

Future: Consider adding mypy for static type checking.

## Development Environment

### Directory Structure

```
.
├── .venv/               # Virtual environment (generated)
├── __pycache__/         # Python cache (generated)
├── .pytest_cache/       # Pytest cache (generated)
├── .coverage            # Coverage data (generated)
├── src/                 # Source code
├── tests/               # Test suite
├── docs/                # Documentation
├── assets/              # Binary assets
├── config-files/        # Configuration files
└── packages/            # Package management (Ansible)
```

[VERIFIED via CLI - 2026-01-03]

### Python Path

The project uses absolute imports from `src/`:

```python
from src.main import main
from src.commands.assets.wallpapers.service import WallpapersService
```

[VERIFIED via source - 2026-01-03]

pytest configuration adds project root to Python path:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

[VERIFIED via source - 2026-01-03]

## IDE Setup

### VSCode

**Recommended extensions:**
- Python
- Pylance
- Pytest

**Settings (`.vscode/settings.json`):**

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ]
}
```

<!-- TODO: Source not available -->

### PyCharm

1. Open project directory
2. PyCharm should auto-detect `.venv/`
3. Mark `src/` as Sources Root
4. Configure pytest as test runner

## Common Development Tasks

### Adding a New Command

See [Adding Commands Guide](adding-commands.md)

### Writing Tests

See [Testing Guide](testing.md)

### Updating Dependencies

```bash
# Update dependencies in pyproject.toml
# Then regenerate lock file
uv pip install -e ".[dev]"
```

### Cleaning Build Artifacts

```bash
make clean
```

[VERIFIED via source - 2026-01-03]

This removes:
- Virtual environment
- Python cache
- Build directories
- `.coverage` file

### Rebuilding Environment

```bash
make clean
make install-dev
make test-cov
```

## Troubleshooting

### Tests Failing

**Check Python version:**
```bash
python --version  # Should be 3.12+
```

**Reinstall dependencies:**
```bash
make clean
make install-dev
```

**Run with verbose output:**
```bash
uv run pytest -vv
```

### Import Errors

**Ensure package installed in editable mode:**
```bash
uv pip install -e ".[dev]"
```

**Check Python path:**
```python
import sys
print(sys.path)
```

### Virtual Environment Issues

**Recreate virtual environment:**
```bash
make clean
make install-dev
```

**Ensure activation:**
```bash
which python  # Should point to .venv/bin/python
```

## Best Practices

### Before Committing

```bash
# 1. Run all tests
make test-cov

# 2. Verify coverage is high
# Check output for coverage percentage

# 3. Test CLI manually
config <your-command>

# 4. Update documentation if needed
```

### During Development

- Write tests first (TDD)
- Run tests frequently
- Keep commits focused and atomic
- Write clear commit messages

### Code Organization

- Keep command logic minimal (in `src/commands/`)
- Put business logic in service classes (in `service.py`)
- Separate concerns clearly
- Use type hints everywhere

[VERIFIED via source - 2026-01-03]

## See Also

- [Testing Guide](testing.md)
- [Adding Commands](adding-commands.md)
- [Architecture](../../architecture/index.md)
- [Design Principles](../../architecture/design-principles.md)
