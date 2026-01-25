# dotfiles-wallpapers

Wallpaper management system for organizing and extracting wallpaper images from archives.

## Overview

`dotfiles-wallpapers` provides a command-line interface and Python API for managing wallpaper collections. It allows you to:

- **List** available wallpapers in archive files
- **Add** wallpaper images to archive collections
- **Extract** wallpapers to local directories
- **Validate** image formats (auto-detection of corrupt files)

## Installation

### From source

```bash
cd dotfiles-wallpapers
uv sync
```

### As a dependency

Add to your project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "dotfiles-wallpapers @ file://path/to/dotfiles-wallpapers",
]
```

## Usage

### Command Line Interface

#### List wallpapers

```bash
dotfiles-wallpapers list
```

Output:
```
Available wallpapers:
  sunset.jpg
  mountains.png
  forest.webp
```

#### Add wallpaper to archive

```bash
dotfiles-wallpapers add archive.tar.gz /path/to/image.jpg
```

Add without validation:

```bash
dotfiles-wallpapers add --no-validate archive.tar.gz image.jpg
```

Overwrite existing:

```bash
dotfiles-wallpapers add --force archive.tar.gz duplicate.jpg
```

#### Extract wallpapers

```bash
dotfiles-wallpapers extract archive.tar.gz /output/directory
```

### Python API

```python
from dotfiles_wallpapers import Wallpapers

wallpapers = Wallpapers()

# List wallpapers in archive
images = wallpapers.list_wallpapers("wallpapers.tar.gz")
for image in images:
    print(f"  {image}")

# Add wallpaper
wallpapers.add_wallpaper(
    "wallpapers.tar.gz",
    "/path/to/image.jpg",
    force=False,
    validate=True
)

# Extract all wallpapers
extracted = wallpapers.extract_wallpapers("wallpapers.tar.gz", "/output/dir")
print(f"Extracted {len(extracted)} images")

# Use custom archive path
wallpapers = Wallpapers(archive_dir="/path/to/archives")
```

## Architecture

### Layered Design

```
CLI Layer          → wallpapers list, add, extract
    ↓
API Layer          → Wallpapers class (public interface)
    ↓
Service Layer      → WallpapersService (business logic)
```

### Supported Image Formats

- **JPEG**: `.jpg`, `.jpeg`
- **PNG**: `.png`
- **GIF**: `.gif`
- **BMP**: `.bmp`
- **WebP**: `.webp`
- **TIFF**: `.tiff`, `.tif`

### Error Handling

The module provides specific exception types:

- **`WallpapersError`**: Base exception for all wallpaper-related errors
- **`InvalidImageError`**: Invalid image format or corrupt file
- **`ArchiveNotFoundError`**: Archive file not found
- **`ArchiveError`**: Error reading/writing archive

Example:

```python
from dotfiles_wallpapers import Wallpapers, InvalidImageError, ArchiveNotFoundError

try:
    wallpapers = Wallpapers()
    wallpapers.add_wallpaper("archive.tar.gz", "image.jpg")
except InvalidImageError as e:
    print(f"Invalid image: {e}")
except ArchiveNotFoundError as e:
    print(f"Archive not found: {e}")
```

## Configuration

### Archive Location

Set the wallpaper archive directory via:

1. **API constructor parameter**:
   ```python
   Wallpapers(archive_dir="/path/to/archives")
   ```

2. **Default location**: `$HOME/.config/dotfiles/wallpapers/`

### Image Validation

Validation checks:
- File extension matches known image format
- File is readable and not corrupt
- Minimum viable file size

Disable validation for performance:

```python
wallpapers.add_wallpaper("archive.tar.gz", "image.jpg", validate=False)
```

Or via CLI:

```bash
dotfiles-wallpapers add --no-validate archive.tar.gz image.jpg
```

## Archive Format

Archives are standard tar.gz files:

```bash
# Create archive
tar czf wallpapers.tar.gz *.jpg *.png

# List contents
tar tzf wallpapers.tar.gz

# Extract
tar xzf wallpapers.tar.gz -C /output/dir
```

The module manages archive operations automatically.

## Testing

Run the test suite:

```bash
uv sync
uv run pytest tests/
```

Test coverage:

- **Unit tests**: Service layer, extension validation, archive operations
- **Integration tests**: CLI commands, add/extract workflows
- **Mocking**: Archive operations with temporary files

## Development

### Project Structure

```
dotfiles-wallpapers/
├── src/
│   └── dotfiles_wallpapers/
│       ├── __init__.py           # Public API exports
│       ├── api/
│       │   └── wallpapers.py      # Wallpapers class
│       ├── cli/
│       │   └── commands/
│       │       ├── list.py        # List command
│       │       ├── add.py         # Add command
│       │       └── extract.py     # Extract command
│       ├── services/
│       │   └── wallpapers_service.py # Business logic
│       └── exceptions.py          # Error types
├── tests/
│   ├── unit/
│   │   ├── test_wallpapers_service.py
│   │   └── test_wallpapers_api.py
│   └── integration/
│       └── test_wallpapers_cli.py
└── pyproject.toml
```

### Adding New Supported Formats

Update the `VALID_EXTENSIONS` in `services/wallpapers_service.py`:

```python
VALID_EXTENSIONS = {
    "jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "tif",
    # Add new formats here
    "svg", "ico"
}
```

## Dependencies

- **Python**: 3.12+
- **tarfile**: Archive handling (stdlib)
- **pathlib**: Path operations (stdlib)
- **typer**: CLI framework

## License

MIT
