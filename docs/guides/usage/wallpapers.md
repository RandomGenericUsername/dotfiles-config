# Managing Wallpapers

[VERIFIED via CLI - 2026-01-03]

Complete guide to managing wallpapers with the `config assets wallpapers` commands.

## Overview

Wallpapers are stored in a compressed tar.gz archive at `assets/wallpapers/wallpapers.tar.gz`. The CLI provides commands to list, add, and extract wallpapers.

[VERIFIED via source - 2026-01-03]

## Listing Wallpapers

View all wallpapers in the archive:

```bash
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

**Example output:**
```
Wallpapers in archive (3):
  - mountain.jpg
  - ocean.png
  - sunset.webp
```

**Empty archive:**
```
No wallpapers in archive
```

[VERIFIED via source - 2026-01-03]

## Adding Wallpapers

### Basic Add

Add a wallpaper to the archive:

```bash
config assets wallpapers add ~/Pictures/my-wallpaper.jpg
```

[VERIFIED via CLI - 2026-01-03]

**Success output:**
```
Successfully added 'my-wallpaper.jpg' to wallpapers archive
```

### Overwriting Existing

If a wallpaper with the same name exists, use `--force`:

```bash
config assets wallpapers add --force ~/Pictures/my-wallpaper.jpg
```

[VERIFIED via CLI - 2026-01-03]

Without `--force`, you'll get an error:
```
Error: Wallpaper 'my-wallpaper.jpg' already exists in archive. Use --force to overwrite.
```

[VERIFIED via source - 2026-01-03]

### Skipping Validation

By default, only image files are allowed. To add non-image files:

```bash
config assets wallpapers add --no-validate /path/to/file.txt
```

[VERIFIED via CLI - 2026-01-03]

**Valid image extensions:**
- jpg, jpeg
- png
- gif
- bmp
- webp
- tiff, tif

[VERIFIED via source - 2026-01-03]

Case-insensitive (JPG, Jpg, jpg all work).

## Extracting Wallpapers

Extract all wallpapers to a directory:

```bash
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

This creates `~/Pictures/wallpapers/` and extracts all wallpapers there.

**Example output:**
```
Extracted 3 wallpaper(s) to /home/user/Pictures/wallpapers
```

**Behavior:**
- Creates `wallpapers` subdirectory in target path
- Creates parent directories if needed
- Preserves original filenames

[VERIFIED via source - 2026-01-03]

## Common Workflows

### Workflow 1: Build Wallpaper Collection

```bash
# Start with empty archive
config assets wallpapers list

# Add multiple wallpapers
config assets wallpapers add ~/Downloads/wallpaper1.jpg
config assets wallpapers add ~/Downloads/wallpaper2.png
config assets wallpapers add ~/Downloads/wallpaper3.webp

# Verify they were added
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 2: Deploy to New System

```bash
# Clone repository
git clone <repo-url>
cd dotfiles/config

# Extract wallpapers to Pictures directory
config assets wallpapers extract ~/Pictures

# Wallpapers now available in ~/Pictures/wallpapers/
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 3: Update Existing Wallpaper

```bash
# Update wallpaper (use --force to overwrite)
config assets wallpapers add --force ~/Pictures/new-version.jpg

# Verify update
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

## Error Messages

**File not found:**
```bash
$ config assets wallpapers add /nonexistent/file.jpg
Error: Wallpaper file not found: /nonexistent/file.jpg
```

**Invalid image extension:**
```bash
$ config assets wallpapers add document.txt
Error: File does not have a valid image extension: document.txt
```

**Archive not found:**
```bash
$ config assets wallpapers list
Error: Archive not found: /path/to/wallpapers.tar.gz
```

[VERIFIED via source - 2026-01-03]

## Tips and Best Practices

### 1. Organize Before Adding

Rename files to descriptive names before adding:

```bash
mv IMG_1234.jpg mountain-sunset.jpg
config assets wallpapers add mountain-sunset.jpg
```

### 2. Use Appropriate Formats

Prefer modern formats for better compression:
- webp - Best compression
- png - Lossless quality
- jpg - Good for photos

### 3. Check Before Overwriting

List existing wallpapers before adding with `--force`:

```bash
config assets wallpapers list
config assets wallpapers add --force wallpaper.jpg
```

### 4. Extract to Temporary Location

Test wallpapers before committing:

```bash
config assets wallpapers extract /tmp/test
# Review wallpapers
# If good, commit changes
```

## See Also

- [CLI Reference: wallpapers](../../reference/cli/assets/wallpapers.md)
- [Wallpapers Service API](../../reference/python-api/services.md#wallpapersservice)
- [Wallpapers Asset Reference](../../reference/assets/wallpapers.md)
