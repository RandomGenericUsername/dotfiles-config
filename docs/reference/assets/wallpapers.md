# Wallpapers Asset

[VERIFIED via CLI - 2026-01-03]

Wallpaper collection stored in a compressed tar.gz archive.

## Location

`assets/wallpapers/`

## Files

- `wallpapers.tar.gz` - Compressed archive containing wallpaper images
- `manage_wallpapers.sh` - Bash script for wallpaper management
- `README.md` - User documentation

[VERIFIED via CLI - 2026-01-03]

## Archive Format

**Format:** tar.gz (gzip-compressed tar archive)

**Contents:** Image files only (no subdirectories)

**Supported Image Formats:**
- jpg, jpeg
- png
- gif
- bmp
- webp
- tiff, tif

[VERIFIED via source - 2026-01-03]

## Management Tools

### CLI Tool

The Python-based `config` CLI provides wallpaper management commands.

```bash
config assets wallpapers list      # List wallpapers
config assets wallpapers add PATH  # Add wallpaper
config assets wallpapers extract PATH  # Extract wallpapers
```

[VERIFIED via CLI - 2026-01-03]

**Documentation:** [CLI Reference: wallpapers](../cli/assets/wallpapers.md)

**Implementation:** [WallpapersService](../python-api/services.md#wallpapersservice)

### Bash Script

Legacy bash script for wallpaper management.

```bash
./manage_wallpapers.sh list
./manage_wallpapers.sh add /path/to/image.jpg
./manage_wallpapers.sh extract /output/directory
```

[VERIFIED via source - 2026-01-03]

**Documentation:** [assets/wallpapers/README.md](../../../assets/wallpapers/README.md)

## Operations

### List Wallpapers

View all wallpapers in the archive:

```bash
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

**Output format:**
```
Wallpapers in archive (N):
  - filename1.png
  - filename2.jpg
```

[VERIFIED via source - 2026-01-03]

### Add Wallpaper

Add a new wallpaper to the archive:

```bash
config assets wallpapers add /path/to/image.png
```

[VERIFIED via CLI - 2026-01-03]

**Behavior:**
- Validates image file extension by default
- Checks for duplicates
- Requires `--force` flag to overwrite existing wallpaper
- Use `--no-validate` to skip extension validation

[VERIFIED via source - 2026-01-03]

### Extract Wallpapers

Extract all wallpapers to a directory:

```bash
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

**Behavior:**
- Creates `wallpapers` subdirectory in target path
- Extracts all wallpapers to subdirectory
- Creates parent directories if needed

[VERIFIED via source - 2026-01-03]

## Archive Structure

The archive contains image files at the root level (no subdirectories):

```
wallpapers.tar.gz
├── image1.png
├── image2.jpg
└── image3.webp
```

[VERIFIED via source - 2026-01-03]

Hidden files (starting with `.`) are excluded from archive operations.

[VERIFIED via source - 2026-01-03]

## Implementation Details

### Service Layer

**Class:** `WallpapersService`

**Source:** [src/commands/assets/wallpapers/service.py](../../../src/commands/assets/wallpapers/service.py)

**Key methods:**
- `list_wallpapers()` - Returns list of wallpaper filenames
- `add_wallpaper(path, overwrite, validate_extension)` - Adds wallpaper to archive
- `extract_wallpapers(output_path)` - Extracts wallpapers to directory
- `is_valid_image_extension(filename)` - Validates image file extension

[VERIFIED via source - 2026-01-03]

### Archive Operations

All archive operations use Python's `tarfile` module with gzip compression (`r:gz` and `w:gz` modes).

Adding wallpapers follows this algorithm:
1. Extract existing archive to temporary directory
2. Copy new wallpaper to temporary directory
3. Create new archive from temporary directory contents
4. Clean up temporary directory

[VERIFIED via source - 2026-01-03]

## Error Handling

**ArchiveNotFoundError:** Raised when archive doesn't exist (for list/extract operations)

**WallpaperNotFoundError:** Raised when wallpaper file doesn't exist (for add operation)

**InvalidImageError:** Raised when file has invalid image extension (for add with validation enabled)

**WallpaperError:** Raised for duplicate wallpapers (for add without --force flag)

[VERIFIED via source - 2026-01-03]

## Testing

Test coverage: 100% for WallpapersService

[VERIFIED via tests - 2026-01-03]

**Test suites:**
- Unit tests: [tests/unit/test_wallpapers_service.py](../../../tests/unit/test_wallpapers_service.py)
- Integration tests: [tests/integration/test_wallpapers_cli.py](../../../tests/integration/test_wallpapers_cli.py)

Total tests: 81 passing

[VERIFIED via tests - 2026-01-03]

## See Also

- [CLI Reference: wallpapers](../cli/assets/wallpapers.md)
- [Python API: WallpapersService](../python-api/services.md#wallpapersservice)
- [User Documentation](../../../assets/wallpapers/README.md)
