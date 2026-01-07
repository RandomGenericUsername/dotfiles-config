# Code Style

[VERIFIED via source - 2026-01-04]

Code style guidelines and conventions for the dotfiles-config project.

## Python Style

### General Guidelines

Follow PEP 8 Python style guide with project-specific conventions.

### Line Length

Maximum 100 characters (flexible for readability).

[VERIFIED via source - 2026-01-03]

### Imports

**Order:**
1. Standard library imports
2. Third-party imports
3. Local imports

**Format:**
```python
import os
import sys
from pathlib import Path
from typing import List, Optional

import typer

from src import Config
from src.services.wallpapers_service import WallpapersService
```

[VERIFIED via source - 2026-01-04]

### Naming Conventions

**Modules:** `lowercase_with_underscores.py`

```python
# Good
wallpapers_service.py
install_packages.py

# Bad
WallpapersService.py
installPackages.py
```

**Classes:** `PascalCase`

```python
# Good
class WallpapersService:
class ArchiveNotFoundError:

# Bad
class wallpapers_service:
class archiveNotFoundError:
```

[VERIFIED via source - 2026-01-03]

**Functions:** `lowercase_with_underscores`

```python
# Good
def add_wallpaper():
def get_default_archive_path():

# Bad
def addWallpaper():
def GetDefaultArchivePath():
```

[VERIFIED via source - 2026-01-03]

**Constants:** `UPPERCASE_WITH_UNDERSCORES`

```python
# Good
VALID_EXTENSIONS = frozenset(["jpg", "png"])
DEFAULT_TIMEOUT = 30

# Bad
validExtensions = frozenset(["jpg", "png"])
default_timeout = 30
```

[VERIFIED via source - 2026-01-03]

**Private:** Prefix with `_`

```python
def _ensure_archive_exists(self):
    """Private method."""
    pass

_INTERNAL_CONSTANT = "value"
```

[VERIFIED via source - 2026-01-03]

## Type Hints

### Always Use Type Hints

```python
# Good
def add_wallpaper(
    self,
    wallpaper_path: Path,
    overwrite: bool = True,
) -> None:
    pass

# Bad
def add_wallpaper(self, wallpaper_path, overwrite=True):
    pass
```

[VERIFIED via source - 2026-01-03]

### Use typing Module

```python
from typing import List, Optional, Dict, Set, Tuple

def get_items() -> List[str]:
    return []

def find_item(name: str) -> Optional[Path]:
    return None
```

[VERIFIED via source - 2026-01-03]

### Type Aliases

For complex types:

```python
from typing import List, Tuple

WallpaperList = List[str]
Coordinate = Tuple[int, int]

def list_wallpapers() -> WallpaperList:
    pass
```

## Docstrings

### Format

Use Google-style docstrings.

[VERIFIED via source - 2026-01-03]

### Module Docstrings

```python
# src/commands/assets/wallpapers/service.py
"""Core wallpaper management service."""
```

[VERIFIED via source - 2026-01-03]

### Function Docstrings

```python
def add_wallpaper(
    self,
    wallpaper_path: Path,
    overwrite: bool = True,
    validate_extension: bool = True,
) -> None:
    """Add a wallpaper to the archive.

    Args:
        wallpaper_path: Path to the wallpaper file
        overwrite: If True, replace existing wallpaper with same name
        validate_extension: If True, validate file has image extension

    Raises:
        WallpaperNotFoundError: If wallpaper file doesn't exist
        InvalidImageError: If file doesn't have valid image extension
        WallpaperError: If wallpaper exists and overwrite=False

    Examples:
        >>> service = WallpapersService(archive_path)
        >>> service.add_wallpaper(Path("sunset.jpg"))
    """
```

[VERIFIED via source - 2026-01-03]

### Class Docstrings

```python
class WallpapersService:
    """Service for managing wallpapers in a tar.gz archive.

    This class provides methods for adding, listing, and extracting
    wallpapers from a compressed archive.

    Attributes:
        archive_path: Path to the wallpapers.tar.gz archive
    """
```

[VERIFIED via source - 2026-01-03]

## Code Organization

### File Structure

```python
# 1. Module docstring
"""Module description."""

# 2. Imports
import standard_library
import third_party
from local import module

# 3. Constants
CONSTANT_VALUE = "value"

# 4. Exceptions
class MyError(Exception):
    pass

# 5. Classes
class MyClass:
    pass

# 6. Functions
def my_function():
    pass
```

[VERIFIED via source - 2026-01-03]

### Class Structure

```python
class MyClass:
    """Class docstring."""

    # 1. Class constants
    CONSTANT = "value"

    # 2. Constructor
    def __init__(self, param: str) -> None:
        """Initialize."""
        self.param = param

    # 3. Class methods
    @classmethod
    def from_string(cls, s: str) -> "MyClass":
        """Create from string."""
        return cls(s)

    # 4. Public methods
    def public_method(self) -> None:
        """Public method."""
        pass

    # 5. Private methods
    def _private_method(self) -> None:
        """Private method."""
        pass
```

[VERIFIED via source - 2026-01-03]

## Comments

### When to Comment

**Do comment:**
- Why code does something (not what)
- Complex algorithms
- Non-obvious workarounds
- TODOs

**Don't comment:**
- Obvious code
- What code does (use docstrings)
- Commented-out code (delete it)

### Comment Style

```python
# Good: Explains why
# Use temporary directory to ensure atomic updates
with tempfile.TemporaryDirectory() as tmpdir:
    pass

# Bad: Explains what (obvious)
# Create temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    pass

# Good: TODO with context
# TODO: Add support for webp format (issue #123)

# Bad: Vague TODO
# TODO: fix this
```

[VERIFIED via source - 2026-01-03]

## Error Handling

### Use Specific Exceptions

```python
# Good
raise WallpaperNotFoundError(f"Wallpaper file not found: {path}")

# Bad
raise Exception("File not found")
```

[VERIFIED via source - 2026-01-03]

### Exception Hierarchy

```python
class MyError(Exception):
    """Base exception."""
    pass

class SpecificError(MyError):
    """Specific error."""
    pass
```

[VERIFIED via source - 2026-01-03]

### Error Messages

```python
# Good: Specific, actionable
raise InvalidImageError(
    f"File does not have a valid image extension: {filename}. "
    f"Valid extensions: {', '.join(VALID_EXTENSIONS)}"
)

# Bad: Vague
raise InvalidImageError("Invalid file")
```

## Testing Style

### Test Organization

```python
class TestComponentOperation:
    """Tests for component operation."""

    def test_operation_success(self):
        """Operation succeeds with valid input."""
        # Arrange
        # Act
        # Assert

    def test_operation_failure(self):
        """Operation fails with invalid input."""
        # Arrange
        # Act
        # Assert
```

[VERIFIED via tests - 2026-01-03]

### Assertions

```python
# Good: Specific
assert result == expected
assert len(items) == 3
assert "wallpaper.jpg" in wallpapers

# Good: With message
assert result, f"Expected result, got None"

# Bad: Generic
assert result
assert items
```

## Best Practices

### 1. Explicit is Better Than Implicit

```python
# Good
if validate_extension and not self.is_valid_image_extension(filename):
    raise InvalidImageError(...)

# Bad
if validate_extension and not self.is_valid_image_extension(filename):
    raise InvalidImageError(...)  # When is this raised? Not clear
```

### 2. Fail Fast

```python
# Good: Check at start
def add_wallpaper(self, path: Path):
    if not path.exists():
        raise NotFoundError()
    # ... rest of function

# Bad: Check late
def add_wallpaper(self, path: Path):
    # ... lots of processing
    if not path.exists():
        raise NotFoundError()
```

[VERIFIED via source - 2026-01-03]

### 3. Single Responsibility

```python
# Good: One responsibility
def list_wallpapers(self) -> List[str]:
    """List wallpapers."""
    return self._get_archive_members()

# Bad: Multiple responsibilities
def list_and_print_wallpapers(self):
    """List wallpapers and print them."""
    wallpapers = self._get_archive_members()
    for w in wallpapers:
        print(w)  # Mixing concerns
    return wallpapers
```

### 4. Immutable Where Possible

```python
# Good: Immutable
VALID_EXTENSIONS = frozenset(["jpg", "png"])

# Bad: Mutable
VALID_EXTENSIONS = ["jpg", "png"]
```

[VERIFIED via source - 2026-01-03]

### 5. Use Path Objects

```python
# Good
from pathlib import Path
path = Path("file.txt")
if path.exists():
    content = path.read_text()

# Bad
import os
path = "file.txt"
if os.path.exists(path):
    with open(path) as f:
        content = f.read()
```

[VERIFIED via source - 2026-01-03]

## Tools

### Formatting

Currently no automated formatter.

<!-- TODO: Source not available -->

Consider adding black or ruff.

### Linting

Currently no automated linting.

<!-- TODO: Source not available -->

Consider adding pylint or ruff.

### Type Checking

Currently no automated type checking.

<!-- TODO: Source not available -->

Consider adding mypy.

## See Also

- [Design Principles](../../architecture/design-principles.md)
- [Testing Guide](testing.md)
- [Adding Commands](adding-commands.md)
