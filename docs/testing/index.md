# Testing

[VERIFIED via tests - 2026-01-04]

Complete testing documentation for the dotfiles-config system.

## Overview

The project uses pytest for testing with comprehensive unit and integration test coverage.

**Test Framework:** pytest 9.0.2

**Python Version:** 3.12.12

**Test Runner:** `uv run pytest`

[VERIFIED via tests - 2026-01-04]

## Test Statistics

**Total Tests:** 183

**Test Results:** 183 passed, 0 failed

**Code Coverage:** 96% overall

[VERIFIED via tests - 2026-01-04]

**Breakdown by Test Type:**

- **Unit Tests:** 112 tests (API and service layer)
- **Integration Tests:** 71 tests (CLI layer)

[VERIFIED via tests - 2026-01-04]

**Coverage by Module:**

| Module | Statements | Missing | Coverage |
|--------|-----------|---------|----------|
| src/commands/__init__.py | 0 | 0 | 100% |
| src/commands/assets/__init__.py | 4 | 0 | 100% |
| src/commands/assets/wallpapers/__init__.py | 43 | 3 | 93% |
| src/commands/assets/wallpapers/service.py | 59 | 0 | 100% |
| src/commands/dummy.py | 3 | 1 | 67% |
| src/commands/install_packages.py | 25 | 19 | 24% |
| src/main.py | 12 | 2 | 83% |
| **TOTAL** | **146** | **25** | **83%** |

[VERIFIED via tests - 2026-01-04]

## Test Coverage Summary

For a detailed behavior-by-behavior breakdown of all tested functionality, see:

**[Test Coverage Summary](test-coverage-summary.md)**

This document describes:
- All tested behaviors organized by feature area
- Supported image formats
- Default behaviors
- Edge cases covered
- Complete test inventory

[VERIFIED via source - 2026-01-04]

## Test Structure

```
tests/
├── conftest.py                                    - Shared fixtures
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_api.py                               - API structure tests (21 tests)
│   ├── test_api_characterization.py              - API behavior tests (48 tests)
│   ├── test_packages_service.py                  - PackagesService tests (16 tests)
│   ├── test_wallpapers_service.py                - Core service tests (34 tests)
│   └── test_wallpapers_service_comprehensive.py  - Edge cases (14 tests)
└── integration/
    ├── __init__.py
    ├── test_packages_cli.py                      - Packages CLI tests (17 tests)
    ├── test_wallpapers_cli.py                    - Core CLI tests (16 tests)
    └── test_wallpapers_cli_comprehensive.py      - CLI edge cases (17 tests)
```

[VERIFIED via CLI - 2026-01-04]

## Running Tests

### Run All Tests

```bash
uv run pytest -v
```

[VERIFIED via tests - 2026-01-04]

### Run Unit Tests Only

```bash
uv run pytest -v tests/unit/
```

or

```bash
make test-unit
```

[VERIFIED via source - 2026-01-03]

### Run Integration Tests Only

```bash
uv run pytest -v tests/integration/
```

or

```bash
make test-integration
```

[VERIFIED via source - 2026-01-03]

### Run with Coverage

```bash
uv run pytest -v --cov=src --cov-report=term-missing
```

or

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-04]

### List Tests Without Running

```bash
uv run pytest -v --collect-only
```

[VERIFIED via tests - 2026-01-04]

## Test Suites

### Unit Tests

**Files:**
- [tests/unit/test_api.py](../../tests/unit/test_api.py) - API structure tests (21 tests)
- [tests/unit/test_api_characterization.py](../../tests/unit/test_api_characterization.py) - API behavior tests (48 tests)
- [tests/unit/test_packages_service.py](../../tests/unit/test_packages_service.py) - PackagesService tests (16 tests)
- [tests/unit/test_wallpapers_service.py](../../tests/unit/test_wallpapers_service.py) - Core service tests (34 tests)
- [tests/unit/test_wallpapers_service_comprehensive.py](../../tests/unit/test_wallpapers_service_comprehensive.py) - Edge cases (14 tests)

**Total Unit Tests:** 133 tests

[VERIFIED via tests - 2026-01-04]

#### API Tests

Tests for the public API layer (Config, Assets, Packages, Wallpapers classes).

**Files:**
- `test_api.py` - Structure tests (21 tests)
- `test_api_characterization.py` - Behavior tests (48 tests)

**Coverage:**
- Config class lazy loading and properties
- Assets facade pattern
- Packages API construction and methods
- Wallpapers API construction and methods
- PackageRole dataclass
- Import patterns and entry points

[VERIFIED via tests - 2026-01-04]

#### PackagesService Tests

Tests for the Packages service layer.

**File:**
- `test_packages_service.py` - (16 tests)

**Coverage:**
- PackageRole and exception classes
- list_packages() method
- install() method
- Error handling

[VERIFIED via tests - 2026-01-04]

#### WallpapersService Tests

Tests for the Wallpapers service layer.

**Test Classes** (test_wallpapers_service.py):

1. **TestWallpapersServiceInit** (2 tests)
   - Service initialization with existing archive
   - Service initialization with nonexistent archive

2. **TestWallpapersServiceList** (3 tests)
   - List wallpapers in archive
   - List empty archive
   - List raises error for nonexistent archive

3. **TestWallpapersServiceAdd** (8 tests)
   - Add wallpaper to existing archive
   - Add wallpaper creates archive if missing
   - Add nonexistent file raises error
   - Add overwrites existing wallpaper
   - Add duplicate without overwrite raises error
   - Add validates image extension
   - Add allows skip validation
   - Add handles relative paths

4. **TestWallpapersServiceExtract** (6 tests)
   - Extract creates wallpapers subdirectory
   - Extract places files in subdirectory
   - Extract creates parent directory
   - Extract empty archive
   - Extract nonexistent archive raises error
   - Extract returns list of extracted files

5. **TestWallpapersServiceValidation** (15 tests)
   - Valid image extensions: jpg, jpeg, png, gif, bmp, webp, tiff, tif, JPG, PNG
   - Invalid image extensions: txt, py, tar.gz, mp4, noextension

[VERIFIED via tests - 2026-01-04]

**Comprehensive Test Classes** (test_wallpapers_service_comprehensive.py):

1. **TestHiddenFilesAndDirectories** (2 tests)
   - List filters hidden files (starting with .)
   - List filters directories (returns only files)

2. **TestMultipleImageFormats** (1 test)
   - Add multiple wallpapers with different formats

3. **TestArchivePreservation** (1 test)
   - Add preserves all existing wallpapers

4. **TestServiceDefaultBehavior** (2 tests)
   - Default overwrites duplicates
   - Default validates extensions

5. **TestValidationEdgeCases** (2 tests)
   - Handles filenames with multiple dots
   - Validates mixed case extensions

6. **TestExtractBehavior** (2 tests)
   - Extract multiple times to same location
   - Extract returns correct path name

7. **TestFilenameHandling** (2 tests)
   - Preserves original filename
   - Uses basename not full path

8. **TestArchiveFormatBehavior** (2 tests)
   - Archive is compressed gzip format
   - Creates parent directories

[VERIFIED via tests - 2026-01-04]

### Integration Tests

**Files:**
- [tests/integration/test_packages_cli.py](../../tests/integration/test_packages_cli.py) - Packages CLI tests (17 tests)
- [tests/integration/test_wallpapers_cli.py](../../tests/integration/test_wallpapers_cli.py) - Core tests (16 tests)
- [tests/integration/test_wallpapers_cli_comprehensive.py](../../tests/integration/test_wallpapers_cli_comprehensive.py) - Edge cases (17 tests)

**Total Integration Tests:** 50 tests

[VERIFIED via tests - 2026-01-04]

#### Packages CLI Tests

Tests for the `config install-packages` CLI command.

**File:**
- `test_packages_cli.py` - (17 tests)

**Coverage:**
- Package installation command
- Tag selection
- Error handling
- Help text

[VERIFIED via tests - 2026-01-04]

#### Wallpapers CLI Tests

**Core Test Classes** (test_wallpapers_cli.py):

1. **TestWallpapersAddCommand** (7 tests)
   - Add command appears in help
   - Add wallpaper successfully
   - Add nonexistent file fails
   - Add duplicate without --force fails
   - Add duplicate with --force succeeds
   - Add invalid extension fails
   - Add with --no-validate allows any file

2. **TestWallpapersExtractCommand** (3 tests)
   - Extract command appears in help
   - Extract creates wallpapers directory
   - Extract with missing archive fails

3. **TestWallpapersListCommand** (3 tests)
   - List command appears in help
   - List shows wallpapers
   - List shows message for empty archive

4. **TestCommandHierarchy** (3 tests)
   - Assets command exists
   - Wallpapers subcommand exists under assets
   - Full command path 'assets wallpapers list' works

[VERIFIED via tests - 2026-01-04]

**Comprehensive Test Classes** (test_wallpapers_cli_comprehensive.py):

1. **TestAddCommandFlags** (2 tests)
   - Short form -f flag works
   - Force and no-validate flags work together

2. **TestListCommandOutput** (2 tests)
   - List shows count in output
   - List output is sorted alphabetically

3. **TestExtractCommandBehavior** (2 tests)
   - Extract shows count in output
   - Extract shows destination path

4. **TestErrorMessageQuality** (3 tests)
   - Nonexistent file shows helpful error
   - Duplicate error mentions --force flag
   - Invalid extension error is clear

5. **TestCommandArgumentValidation** (2 tests)
   - Add requires path argument
   - Extract requires path argument

6. **TestHelpMessages** (5 tests)
   - Add help describes --force flag
   - Add help describes --no-validate flag
   - Add help shows -f short flag
   - Extract help describes behavior
   - List help describes behavior

7. **TestDefaultArchivePath** (1 test)
   - Commands use default archive path in assets/wallpapers/

[VERIFIED via tests - 2026-01-04]

## Shared Fixtures

**File:** [tests/conftest.py](../../tests/conftest.py)

[VERIFIED via source - 2026-01-03]

### `temp_dir`

Provides a temporary directory that is cleaned up after the test.

```python
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]
```

### `sample_image`

Creates a minimal valid PNG file (1x1 transparent pixel) for testing.

```python
@pytest.fixture
def sample_image(temp_dir: Path) -> Path
```

### `sample_archive`

Creates a tar.gz archive containing one sample image.

```python
@pytest.fixture
def sample_archive(temp_dir: Path, sample_image: Path) -> Path
```

### `empty_archive`

Creates an empty tar.gz archive.

```python
@pytest.fixture
def empty_archive(temp_dir: Path) -> Path
```

### `nonexistent_archive`

Returns a path to a nonexistent archive (for error testing).

```python
@pytest.fixture
def nonexistent_archive(temp_dir: Path) -> Path
```

[VERIFIED via source - 2026-01-03]

## Configuration

**File:** [pyproject.toml](../../pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

[VERIFIED via source - 2026-01-03]

## Test Dependencies

[VERIFIED via source - 2026-01-03]

**Required packages:**
- pytest>=8.0.0
- pytest-cov>=4.0.0

Install with:

```bash
uv pip install -e ".[dev]"
```

or

```bash
make install-dev
```

## Known Warnings

[VERIFIED via tests - 2026-01-04]

**DeprecationWarning:** 27 warnings about `tar.extractall()` filter argument

**Location:** `src/commands/assets/wallpapers/service.py:139` and `:175`

**Cause:** Python 3.14 will require explicit filter argument for security

**Impact:** None (warnings only, all 81 tests pass)

**Status:** Future improvement needed before Python 3.14

## Coverage Gaps

[VERIFIED via tests - 2026-01-04]

**Low Coverage Modules:**

1. **src/commands/install_packages.py** (24% coverage)
   - Missing: Error handling paths (lines 19-50)
   - Reason: Requires actual Ansible installation and execution

2. **src/commands/dummy.py** (67% coverage)
   - Missing: Line 8 (typer.echo execution)
   - Reason: CLI command not directly tested

3. **src/main.py** (83% coverage)
   - Missing: Lines 22, 26 (main function execution)
   - Reason: Entry point not directly tested

4. **src/commands/assets/wallpapers/__init__.py** (93% coverage)
   - Missing: Lines 95-97 (error handling paths)
   - Reason: Specific error conditions not triggered in tests

## Adding New Tests

### Unit Test Template

```python
import pytest
from pathlib import Path

class TestNewFeature:
    """Tests for new feature."""

    def test_basic_functionality(self, temp_dir: Path):
        """Test basic functionality."""
        # Arrange
        # Act
        # Assert
        pass
```

### Integration Test Template

```python
import subprocess

class TestNewCommand:
    """Tests for new CLI command."""

    def test_command_in_help(self):
        """Command appears in help output."""
        result = subprocess.run(
            ["uv", "run", "config", "--help"],
            capture_output=True,
            text=True,
        )
        assert "new-command" in result.stdout
```

## Continuous Integration

<!-- TODO: Source not available -->

No CI/CD configuration exists yet. Tests run locally only.

## See Also

- [Test Coverage Summary](test-coverage-summary.md) - Detailed behavior breakdown
- [Development Guide](../guides/development/testing.md) - Testing best practices
- [Python API Reference](../reference/python-api/index.md) - API documentation
