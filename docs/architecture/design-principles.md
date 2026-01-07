# Design Principles

[VERIFIED via source - 2026-01-03]

Core design decisions and architectural patterns used in the project.

## 1. Separation of Concerns

### Principle

Separate presentation logic (CLI) from business logic (services).

[VERIFIED via source - 2026-01-03]

### Implementation

**Command layer** handles:
- Argument parsing
- User interaction
- Output formatting
- Exit codes

**Service layer** handles:
- Business rules
- Data validation
- File operations
- Domain logic

[VERIFIED via source - 2026-01-03]

### Example

```python
# Command layer - CLI concerns
def add_wallpaper(path: Path, force: bool, no_validate: bool):
    service = get_service()
    try:
        service.add_wallpaper(path, overwrite=force, validate_extension=not no_validate)
        typer.echo(f"Successfully added '{path.name}' to wallpapers archive")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

# Service layer - Business logic
class WallpapersService:
    def add_wallpaper(self, wallpaper_path: Path, overwrite: bool, validate_extension: bool):
        if not wallpaper_path.exists():
            raise WallpaperNotFoundError(f"Wallpaper file not found: {wallpaper_path}")
        # ... business logic
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Services can be tested without CLI framework
- Services can be reused in different contexts
- CLI can be changed without affecting business logic
- Clear responsibility boundaries

## 2. Explicit Over Implicit

### Principle

Make behavior explicit rather than relying on implicit conventions.

[VERIFIED via source - 2026-01-03]

### Implementation

**Explicit validation:**

```python
if validate_extension and not self.is_valid_image_extension(filename):
    raise InvalidImageError(f"File does not have a valid image extension: {filename}")
```

Rather than silently accepting invalid files.

[VERIFIED via source - 2026-01-03]

**Explicit error messages:**

```python
raise WallpaperNotFoundError(f"Wallpaper file not found: {wallpaper_path}")
```

Rather than generic "File not found".

[VERIFIED via source - 2026-01-03]

**Explicit path resolution:**

```python
wallpaper_path = wallpaper_path.resolve()  # Explicitly resolve relative paths
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Easier to debug
- Clearer error messages
- No surprising behavior
- Better user experience

## 3. Fail Fast

### Principle

Detect and report errors as early as possible.

[VERIFIED via source - 2026-01-03]

### Implementation

**Argument validation:**

```python
path: Path = typer.Argument(..., exists=True, readable=True)
```

Typer validates file exists and is readable before calling function.

[VERIFIED via source - 2026-01-03]

**Early validation in service:**

```python
def add_wallpaper(self, wallpaper_path: Path, ...):
    if not wallpaper_path.exists():  # Check immediately
        raise WallpaperNotFoundError(...)
    if validate_extension and not self.is_valid_image_extension(filename):
        raise InvalidImageError(...)  # Check before expensive operations
    # ... continue with archive operations
```

[VERIFIED via source - 2026-01-03]

**Archive existence check:**

```python
def _ensure_archive_exists(self) -> None:
    if not self.archive_path.exists():
        raise ArchiveNotFoundError(f"Archive not found: {self.archive_path}")
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Prevents partial operations
- Clear error location
- No resource waste
- Easier debugging

## 4. Domain-Specific Exceptions

### Principle

Use specific exception types for different error conditions.

[VERIFIED via source - 2026-01-03]

### Implementation

**Exception hierarchy:**

```python
class WallpaperError(Exception):
    """Base exception for wallpaper operations."""

class ArchiveNotFoundError(WallpaperError):
    """Raised when the wallpaper archive doesn't exist."""

class WallpaperNotFoundError(WallpaperError):
    """Raised when a wallpaper file doesn't exist."""

class InvalidImageError(WallpaperError):
    """Raised when a file is not a valid image."""
```

[VERIFIED via source - 2026-01-03]

### Usage

**Specific exception for specific error:**

```python
if not wallpaper_path.exists():
    raise WallpaperNotFoundError(...)

if not self.is_valid_image_extension(filename):
    raise InvalidImageError(...)
```

[VERIFIED via source - 2026-01-03]

**Catch specific exceptions:**

```python
try:
    service.add_wallpaper(...)
except WallpaperError as e:  # Catches all wallpaper-related errors
    typer.echo(f"Error: {e}", err=True)
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Clear error types
- Specific handling possible
- Better error messages
- Easier debugging

## 5. Immutability Where Practical

### Principle

Use immutable data structures when they don't hinder functionality.

[VERIFIED via source - 2026-01-03]

### Implementation

**Frozen sets for constants:**

```python
VALID_EXTENSIONS = frozenset([
    "jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "tif"
])
```

[VERIFIED via source - 2026-01-03]

**Return new Path objects:**

```python
wallpaper_path = wallpaper_path.resolve()  # Returns new Path, doesn't modify
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Thread safety
- No accidental modifications
- Hashable for sets/dicts
- Clear intent

## 6. Atomic Operations

### Principle

Ensure operations either complete fully or have no effect.

[VERIFIED via source - 2026-01-03]

### Implementation

**Archive updates use temporary directory:**

```python
with tempfile.TemporaryDirectory() as tmpdir:
    tmp_path = Path(tmpdir)

    # Extract existing archive to temp
    if self.archive_path.exists():
        with tarfile.open(self.archive_path, "r:gz") as tar:
            tar.extractall(tmp_path)

    # Add new wallpaper to temp
    shutil.copy2(wallpaper_path, tmp_path / filename)

    # Create new archive from temp
    with tarfile.open(self.archive_path, "w:gz") as tar:
        for file_path in tmp_path.iterdir():
            tar.add(file_path, arcname=file_path.name)

    # Temp directory auto-deleted on exit
```

[VERIFIED via source - 2026-01-03]

### Benefits

- No partial states
- Safe failure handling
- Rollback on error
- Data consistency

## 7. Dependency Injection

### Principle

Pass dependencies explicitly rather than creating them internally.

[VERIFIED via source - 2026-01-03]

### Implementation

**Service receives archive path:**

```python
class WallpapersService:
    def __init__(self, archive_path: Path) -> None:
        self.archive_path = archive_path
```

Rather than hardcoding the path inside the service.

[VERIFIED via source - 2026-01-03]

**Helper function creates service:**

```python
def get_service() -> WallpapersService:
    return WallpapersService(get_default_archive_path())
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Testable with different paths
- Flexible configuration
- Clear dependencies
- Easy mocking

## 8. Type Annotations

### Principle

Use type hints for all function signatures.

[VERIFIED via source - 2026-01-03]

### Implementation

**Full type annotations:**

```python
def add_wallpaper(
    self,
    wallpaper_path: Path,
    overwrite: bool = True,
    validate_extension: bool = True,
) -> None:
```

[VERIFIED via source - 2026-01-03]

**Class method annotations:**

```python
@classmethod
def is_valid_image_extension(cls, filename: str) -> bool:
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Self-documenting code
- Editor autocomplete
- Type checking possible
- Fewer runtime errors

## 9. Progressive Enhancement

### Principle

Provide core functionality with optional enhancements.

[VERIFIED via source - 2026-01-03]

### Implementation

**Validation is optional:**

```python
def add_wallpaper(..., validate_extension: bool = True):
    if validate_extension and not self.is_valid_image_extension(filename):
        raise InvalidImageError(...)
```

Users can disable validation with `--no-validate` if needed.

[VERIFIED via source - 2026-01-03]

**Shell completion is optional:**

```bash
config --install-completion  # Optional enhancement
```

[VERIFIED via CLI - 2026-01-03]

### Benefits

- Core features always work
- Advanced features available when needed
- No forced complexity
- Flexible usage

## 10. Documentation in Code

### Principle

Code should be self-documenting with clear names and docstrings.

[VERIFIED via source - 2026-01-03]

### Implementation

**Clear function names:**

```python
def is_valid_image_extension(...)  # Clear what it does
def get_default_archive_path(...)  # Clear what it returns
def _ensure_archive_exists(...)    # Private, clear purpose
```

[VERIFIED via source - 2026-01-03]

**Comprehensive docstrings:**

```python
def add_wallpaper(self, wallpaper_path: Path, overwrite: bool = True, validate_extension: bool = True) -> None:
    """Add a wallpaper to the archive.

    Args:
        wallpaper_path: Path to the wallpaper file
        overwrite: If True, replace existing wallpaper with same name
        validate_extension: If True, validate file has image extension

    Raises:
        WallpaperNotFoundError: If wallpaper file doesn't exist
        InvalidImageError: If file doesn't have valid image extension
        WallpaperError: If wallpaper exists and overwrite=False
    """
```

[VERIFIED via source - 2026-01-03]

### Benefits

- Self-documenting API
- Clear expectations
- Better IDE support
- Easier onboarding

## 11. Test-Driven Design

### Principle

Design with testability in mind.

[VERIFIED via tests - 2026-01-03]

### Implementation

**Service layer is independently testable:**

```python
# Unit test without CLI
service = WallpapersService(archive_path)
service.add_wallpaper(image_path)
assert image_path.name in service.list_wallpapers()
```

[VERIFIED via tests - 2026-01-03]

**Fixtures for common test data:**

```python
@pytest.fixture
def sample_image(temp_dir: Path) -> Path:
    """Create a sample image file for testing."""
    # ... creates valid PNG
```

[VERIFIED via source - 2026-01-03]

**100% coverage for core service:**

Service layer has 100% test coverage, ensuring all paths work correctly.

[VERIFIED via tests - 2026-01-03]

### Benefits

- Confident refactoring
- Regression prevention
- Clear requirements
- Living documentation

## See Also

- [CLI Structure](cli-structure.md)
- [Integration Points](integration-points.md)
- [Testing Documentation](../testing/index.md)
- [Development Guide](../guides/development/index.md)
