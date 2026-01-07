# Testing Guide

[VERIFIED via tests - 2026-01-03]

How to write and run tests for the dotfiles-config project.

## Test Framework

The project uses **pytest** for testing with **pytest-cov** for coverage reporting.

[VERIFIED via tests - 2026-01-03]

## Test Structure

```
tests/
├── conftest.py                                    # Shared fixtures
├── unit/                                          # Unit tests
│   ├── test_api.py                               # API structure tests
│   ├── test_api_characterization.py              # API behavior tests (48 tests)
│   ├── test_packages_service.py                  # PackagesService tests (16 tests)
│   ├── test_wallpapers_service.py                # WallpapersService tests (34 tests)
│   └── test_wallpapers_service_comprehensive.py  # Edge cases (14 tests)
└── integration/                                   # Integration tests
    ├── test_packages_cli.py                      # Packages CLI tests (17 tests)
    ├── test_wallpapers_cli.py                    # Wallpapers CLI tests (16 tests)
    └── test_wallpapers_cli_comprehensive.py      # CLI edge cases (17 tests)
```

[VERIFIED via CLI - 2026-01-04]

## Running Tests

### All Tests

```bash
make test
```

or

```bash
uv run pytest -v
```

[VERIFIED via tests - 2026-01-03]

### Unit Tests Only

```bash
make test-unit
```

or

```bash
uv run pytest -v tests/unit/
```

[VERIFIED via source - 2026-01-03]

### Integration Tests Only

```bash
make test-integration
```

or

```bash
uv run pytest -v tests/integration/
```

[VERIFIED via source - 2026-01-03]

### With Coverage

```bash
make test-cov
```

or

```bash
uv run pytest -v --cov=src --cov-report=term-missing
```

[VERIFIED via tests - 2026-01-03]

### Specific Test File

```bash
uv run pytest tests/unit/test_wallpapers_service.py -v
```

### Specific Test Class

```bash
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd -v
```

### Specific Test Function

```bash
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd::test_add_wallpaper_to_existing_archive -v
```

## Writing Unit Tests

Unit tests test individual components in isolation.

### Example Unit Test

```python
from pathlib import Path
from src.services.wallpapers_service import WallpapersService

class TestWallpapersService:
    """Tests for WallpapersService."""

    def test_list_wallpapers(self, sample_archive: Path):
        """List wallpapers in archive."""
        service = WallpapersService(sample_archive)
        wallpapers = service.list_wallpapers()
        assert len(wallpapers) > 0
        assert "test_wallpaper.png" in wallpapers
```

[VERIFIED via tests - 2026-01-04]

### Structure

```python
class Test<ComponentName>:
    """Tests for <component>."""

    def test_<scenario>(self, fixtures):
        """<Description of what is being tested>."""
        # Arrange
        service = WallpapersService(archive_path)

        # Act
        result = service.some_method()

        # Assert
        assert result == expected
```

## Writing Integration Tests

Integration tests test CLI commands end-to-end.

### Example Integration Test

```python
import subprocess

class TestWallpapersListCommand:
    """Tests for 'config assets wallpapers list' command."""

    def test_list_shows_wallpapers(self):
        """List displays wallpaper names."""
        result = subprocess.run(
            ["uv", "run", "config", "assets", "wallpapers", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Wallpapers in archive" in result.stdout
```

[VERIFIED via tests - 2026-01-03]

### Structure

```python
class Test<CommandName>:
    """Tests for '<command>' command."""

    def test_<scenario>(self):
        """<Description>."""
        result = subprocess.run(
            ["uv", "run", "config", "command", "subcommand"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "expected output" in result.stdout
```

## Using Fixtures

Fixtures provide reusable test data and setup.

### Shared Fixtures

Defined in `tests/conftest.py`:

[VERIFIED via source - 2026-01-03]

**temp_dir:**
```python
@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
```

**sample_image:**
```python
@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample image file."""
    image_path = temp_dir / "test_wallpaper.png"
    # Creates valid PNG
    return image_path
```

**sample_archive:**
```python
@pytest.fixture
def sample_archive(temp_dir: Path, sample_image: Path) -> Path:
    """Create a sample tar.gz archive."""
    archive_path = temp_dir / "wallpapers.tar.gz"
    # Creates archive with sample image
    return archive_path
```

### Using Fixtures

```python
def test_something(temp_dir: Path, sample_image: Path):
    """Test using fixtures."""
    # temp_dir and sample_image are provided by pytest
    assert sample_image.exists()
    assert sample_image.parent == temp_dir
```

### Creating Custom Fixtures

```python
@pytest.fixture
def custom_service(temp_dir: Path) -> WallpapersService:
    """Create a WallpapersService for testing."""
    archive_path = temp_dir / "wallpapers.tar.gz"
    return WallpapersService(archive_path)

def test_with_custom_fixture(custom_service: WallpapersService):
    """Test using custom fixture."""
    result = custom_service.list_wallpapers()
    assert isinstance(result, list)
```

## Test Organization

### Test Class Naming

```python
class Test<Component><Operation>:
    """Tests for <description>."""
```

Examples:
- `TestWallpapersServiceInit`
- `TestWallpapersServiceAdd`
- `TestWallpapersListCommand`

[VERIFIED via tests - 2026-01-03]

### Test Function Naming

```python
def test_<scenario>_<expected_result>(self):
    """<Short description>."""
```

Examples:
- `test_add_wallpaper_success`
- `test_add_nonexistent_file_fails`
- `test_list_empty_archive`

[VERIFIED via tests - 2026-01-03]

### Test Docstrings

Every test function must have a docstring describing what it tests:

```python
def test_add_wallpaper_to_existing_archive(self):
    """Add new wallpaper to existing archive."""
```

[VERIFIED via tests - 2026-01-03]

## Assertions

### Good Assertions

**Specific:**
```python
assert result == "expected value"
```

**With message:**
```python
assert len(wallpapers) == 3, f"Expected 3 wallpapers, got {len(wallpapers)}"
```

**Multiple aspects:**
```python
assert result.returncode == 0
assert "Success" in result.stdout
assert result.stderr == ""
```

### Testing Exceptions

```python
import pytest

def test_invalid_input_raises_error(self):
    """Invalid input raises InvalidImageError."""
    service = WallpapersService(archive_path)

    with pytest.raises(InvalidImageError):
        service.add_wallpaper(Path("file.txt"))
```

[VERIFIED via tests - 2026-01-03]

### Testing Error Messages

```python
def test_error_message(self):
    """Error message is clear."""
    service = WallpapersService(archive_path)

    with pytest.raises(WallpaperNotFoundError) as exc_info:
        service.add_wallpaper(Path("/nonexistent/file.jpg"))

    assert "Wallpaper file not found" in str(exc_info.value)
```

[VERIFIED via tests - 2026-01-03]

## Test Coverage

### Current Coverage

**Overall:** 96%

**Total Tests:** 183

[VERIFIED via tests - 2026-01-04]

**By Module:**
- `api/config.py`: 100%
- `api/assets.py`: 100%
- `api/packages.py`: 100%
- `api/wallpapers.py`: 100%
- `services/wallpapers_service.py`: 100%
- `services/packages_service.py`: 100%
- `wallpapers/__init__.py`: 93%
- `assets/__init__.py`: 100%
- `main.py`: 83%

### Viewing Coverage

```bash
make test-cov
```

[VERIFIED via tests - 2026-01-03]

Output shows:
- Coverage percentage per file
- Missing line numbers
- Total coverage

### Coverage Goals

- **New code:** Aim for 100% coverage
- **Service layer:** Maintain 100% coverage
- **CLI layer:** Aim for >85% coverage
- **Overall:** Maintain >80% coverage

## Testing Best Practices

### 1. Test One Thing

Each test should verify one specific behavior:

**Good:**
```python
def test_add_wallpaper_success(self):
    """Add wallpaper successfully."""
    # Tests only successful addition
```

**Bad:**
```python
def test_wallpaper_operations(self):
    """Test add, list, and extract."""
    # Tests too many things
```

### 2. Use AAA Pattern

Arrange, Act, Assert:

```python
def test_something(self):
    """Test description."""
    # Arrange: Set up test data
    service = WallpapersService(archive_path)
    image_path = create_test_image()

    # Act: Execute the operation
    service.add_wallpaper(image_path)

    # Assert: Verify the result
    assert image_path.name in service.list_wallpapers()
```

### 3. Test Edge Cases

- Empty inputs
- Missing files
- Invalid data
- Boundary conditions

[VERIFIED via tests - 2026-01-03]

### 4. Test Error Conditions

```python
def test_add_nonexistent_file_raises(self):
    """Adding nonexistent file raises error."""
    with pytest.raises(WallpaperNotFoundError):
        service.add_wallpaper(Path("/nonexistent.jpg"))
```

[VERIFIED via tests - 2026-01-03]

### 5. Use Descriptive Names

Test names should describe what is being tested:

```python
def test_add_duplicate_without_force_fails(self):
    """Adding duplicate without --force shows error."""
```

[VERIFIED via tests - 2026-01-03]

## Debugging Tests

### Run with verbose output

```bash
uv run pytest -vv
```

### Show print statements

```bash
uv run pytest -s
```

### Stop on first failure

```bash
uv run pytest -x
```

### Run specific test

```bash
uv run pytest tests/unit/test_wallpapers_service.py::test_specific_test -vv
```

### Use pdb debugger

```python
def test_something(self):
    """Test description."""
    import pdb; pdb.set_trace()
    # Test code
```

## See Also

- [Development Setup](setup.md)
- [Adding Commands](adding-commands.md)
- [Testing Reference](../../testing/index.md)
- [Design Principles](../../architecture/design-principles.md)
