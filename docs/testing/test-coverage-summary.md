# Test Coverage Summary

[VERIFIED via tests - 2026-01-04]

Complete behavior-by-behavior breakdown of all tested functionality.

## Test Statistics

- **Total Tests**: 183 passing
- **Unit Tests**: 133 tests (API and service layer)
- **Integration Tests**: 50 tests (CLI layer)
- **Code Coverage**: 96% overall, 100% for API layer and services

[VERIFIED via tests - 2026-01-04]

---

## Service Layer Behaviors (Unit Tests)

### Initialization
- ✅ Service initializes with existing archive path
- ✅ Service initializes with nonexistent archive path (archive created on first add)

### List Operation
- ✅ Lists all wallpaper filenames from archive
- ✅ Returns empty list for empty archive
- ✅ Raises `ArchiveNotFoundError` when archive doesn't exist
- ✅ Filters out hidden files (files starting with `.`)
- ✅ Filters out directory entries (only returns files)

### Add Operation
- ✅ Adds new wallpaper to existing archive
- ✅ Creates archive if it doesn't exist
- ✅ Raises `WallpaperNotFoundError` for missing source file
- ✅ Overwrites existing wallpaper when `overwrite=True` (default)
- ✅ Raises `WallpaperError` when duplicate exists and `overwrite=False`
- ✅ Validates image extension by default (raises `InvalidImageError` for non-images)
- ✅ Skips validation when `validate_extension=False`
- ✅ Handles both relative and absolute paths
- ✅ Preserves all existing wallpapers when adding new ones
- ✅ Preserves original filename from source path
- ✅ Stores only basename, not full directory path
- ✅ Creates parent directories for archive if needed
- ✅ Supports multiple image formats in same archive

### Extract Operation
- ✅ Creates 'wallpapers' subdirectory in target location
- ✅ Places extracted files in the wallpapers subdirectory
- ✅ Creates parent directories if they don't exist
- ✅ Handles empty archives (creates empty directory)
- ✅ Raises `ArchiveNotFoundError` when archive doesn't exist
- ✅ Returns Path object pointing to wallpapers directory
- ✅ Allows extracting multiple times to same location (overwrites)

### Image Validation
- ✅ Validates these image extensions: jpg, jpeg, png, gif, bmp, webp, tiff, tif
- ✅ Validation is case-insensitive (JPG, PNG, etc. work)
- ✅ Handles filenames with multiple dots correctly (uses last extension)
- ✅ Rejects non-image extensions: txt, py, tar.gz, mp4
- ✅ Rejects filenames without extensions

### Archive Format
- ✅ Creates gzip-compressed tar archives (.tar.gz)
- ✅ Archives are valid tar format

---

## CLI Layer Behaviors (Integration Tests)

### Command Hierarchy
- ✅ `assets` command exists in main CLI
- ✅ `wallpapers` subcommand exists under assets
- ✅ Full command path `config assets wallpapers` works

### Add Command (`config assets wallpapers add`)
- ✅ Appears in wallpapers help menu
- ✅ Successfully adds wallpaper with valid image
- ✅ Fails with nonexistent file (exit code != 0)
- ✅ Fails when duplicate exists without `--force` flag
- ✅ Succeeds when duplicate exists with `--force` flag
- ✅ Short form `-f` works as alias for `--force`
- ✅ Fails for invalid image extension
- ✅ Accepts non-image files with `--no-validate` flag
- ✅ Accepts both `--force` and `--no-validate` together
- ✅ Shows success message with filename
- ✅ Requires path argument (fails without it)
- ✅ Uses default archive path at `assets/wallpapers/wallpapers.tar.gz`

### Extract Command (`config assets wallpapers extract`)
- ✅ Appears in wallpapers help menu
- ✅ Creates wallpapers subdirectory in target location
- ✅ Extracts files successfully
- ✅ Fails when archive doesn't exist
- ✅ Shows count of extracted wallpapers in output
- ✅ Shows destination path in output
- ✅ Requires path argument (fails without it)

### List Command (`config assets wallpapers list`)
- ✅ Appears in wallpapers help menu
- ✅ Displays wallpaper names
- ✅ Shows count of wallpapers in output
- ✅ Shows "No wallpapers" message for empty archive
- ✅ Fails when archive doesn't exist
- ✅ Displays wallpapers in sorted alphabetical order

### Error Messages
- ✅ Nonexistent file error is clear and helpful
- ✅ Duplicate error mentions `--force` flag
- ✅ Invalid extension error mentions "extension"
- ✅ All errors show "Error:" prefix

### Help Messages
- ✅ Add help describes `--force` flag (mentions "overwrite")
- ✅ Add help describes `--no-validate` flag (mentions "validation")
- ✅ Add help shows `-f` as short form
- ✅ Extract help describes behavior
- ✅ List help describes behavior

---

## Supported Image Formats

The following image formats are validated and supported:
- `jpg` / `jpeg` - JPEG images
- `png` - PNG images
- `gif` - GIF images
- `bmp` - Bitmap images
- `webp` - WebP images
- `tiff` / `tif` - TIFF images

All formats are case-insensitive (e.g., `.PNG`, `.Jpg` work).

[VERIFIED via source - 2026-01-04]

---

## Default Behaviors

### Service Layer Defaults
- `add_wallpaper()` defaults to `overwrite=True` (replaces duplicates)
- `add_wallpaper()` defaults to `validate_extension=True` (validates image format)

### CLI Layer Defaults
- Archive location: `{config_root}/assets/wallpapers/wallpapers.tar.gz`
- `--force` flag defaults to `False` (must be explicit)
- `--no-validate` flag defaults to `False` (validation enabled)

[VERIFIED via source - 2026-01-04]

---

## Edge Cases Tested

### Filename Handling
- ✅ Filenames with multiple dots (`photo.final.v2.png`)
- ✅ Mixed case extensions (`IMAGE.PNG`)
- ✅ Files in nested directories (preserves basename only)
- ✅ Hidden files (filtered from list)

### Path Handling
- ✅ Relative paths
- ✅ Absolute paths
- ✅ Nonexistent parent directories (created automatically)

### Archive States
- ✅ Nonexistent archive (created on first add)
- ✅ Empty archive
- ✅ Archive with multiple files
- ✅ Multiple extractions to same location

[VERIFIED via tests - 2026-01-04]

---

## Test Files

### Unit Tests
- `tests/unit/test_wallpapers_service.py` - Core service layer tests (34 tests)
- `tests/unit/test_wallpapers_service_comprehensive.py` - Edge cases and behaviors (14 tests)

### Integration Tests
- `tests/integration/test_wallpapers_cli.py` - Core CLI tests (16 tests)
- `tests/integration/test_wallpapers_cli_comprehensive.py` - CLI edge cases (17 tests)

### Test Fixtures
- `tests/conftest.py` - Shared fixtures (temp dirs, sample images, archives)

[VERIFIED via CLI - 2026-01-04]

---

## Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run with coverage report
make test-cov

# Run specific test file
uv run pytest tests/unit/test_wallpapers_service.py -v

# Run specific test class
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd -v

# Run specific test
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd::test_add_wallpaper_creates_archive_if_missing -v
```

[VERIFIED via source - 2026-01-04]

---

## See Also

- [Testing Documentation](index.md) - Main testing documentation
- [Development Guide](../guides/development/testing.md) - Testing best practices
- [Python API Reference](../reference/python-api/services.md) - WallpapersService API
