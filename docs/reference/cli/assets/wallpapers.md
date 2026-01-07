# wallpapers

[VERIFIED via CLI - 2026-01-03]

Manage wallpaper assets stored in a tar.gz archive.

## Synopsis

```bash
config assets wallpapers [OPTIONS] COMMAND [ARGS]...
```

## Description

Command group for managing wallpapers stored in `assets/wallpapers/wallpapers.tar.gz`. Operations include adding new wallpapers, listing existing ones, and extracting them to directories.

## Options

| Option | Description |
|--------|-------------|
| `--help` | Show this message and exit |

## Subcommands

### add

Add a wallpaper to the archive.

```bash
config assets wallpapers add [OPTIONS] PATH
```

**Arguments:**

| Argument | Type | Description |
|----------|------|-------------|
| `PATH` | Path (required) | Path to the wallpaper image to add |

**Options:**

| Option | Description |
|--------|-------------|
| `--force`, `-f` | Overwrite if wallpaper with same name exists |
| `--no-validate` | Skip image extension validation |
| `--help` | Show this message and exit |

[VERIFIED via CLI - 2026-01-03]

**Valid Image Extensions (by default):**

jpg, jpeg, png, gif, bmp, webp, tiff, tif (case-insensitive)

[VERIFIED via source - 2026-01-03]

**Examples:**

```bash
# Add a wallpaper
config assets wallpapers add ~/Pictures/sunset.png
```

```bash
# Add and overwrite if exists
config assets wallpapers add --force ~/Pictures/sunset.png
```

```bash
# Add without validating file extension
config assets wallpapers add --no-validate /path/to/file.txt
```

### extract

Extract all wallpapers to the specified directory.

```bash
config assets wallpapers extract [OPTIONS] PATH
```

**Arguments:**

| Argument | Type | Description |
|----------|------|-------------|
| `PATH` | Path (required) | Directory where wallpapers will be extracted (creates 'wallpapers' subdirectory) |

**Options:**

| Option | Description |
|--------|-------------|
| `--help` | Show this message and exit |

[VERIFIED via CLI - 2026-01-03]

**Behavior:**

- Creates a `wallpapers` subdirectory inside the specified PATH
- Extracts all wallpapers into this subdirectory
- Creates parent directories if they don't exist

[VERIFIED via tests - 2026-01-03]

**Examples:**

```bash
# Extract to ~/Pictures (creates ~/Pictures/wallpapers/)
config assets wallpapers extract ~/Pictures
```

### list

List all wallpapers in the archive.

```bash
config assets wallpapers list [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--help` | Show this message and exit |

[VERIFIED via CLI - 2026-01-03]

**Output Format:**

```
Wallpapers in archive (N):
  - filename1.png
  - filename2.jpg
  ...
```

[VERIFIED via source - 2026-01-03]

If the archive is empty:

```
No wallpapers in archive
```

[VERIFIED via source - 2026-01-03]

**Example:**

```bash
config assets wallpapers list
```

## Error Handling

[VERIFIED via source - 2026-01-03]

**Exit Code 1 scenarios:**

- **ArchiveNotFoundError**: The wallpapers archive doesn't exist (for `list` and `extract`)
- **WallpaperNotFoundError**: The specified wallpaper file doesn't exist (for `add`)
- **InvalidImageError**: File doesn't have a valid image extension (for `add` without `--no-validate`)
- **WallpaperError**: Duplicate wallpaper exists in archive (for `add` without `--force`)

## Archive Location

Default: `assets/wallpapers/wallpapers.tar.gz`

[VERIFIED via source - 2026-01-03]

## Source Code

- CLI Implementation: [src/commands/assets/wallpapers/__init__.py](../../../../src/commands/assets/wallpapers/__init__.py)
- Service Layer: [src/commands/assets/wallpapers/service.py](../../../../src/commands/assets/wallpapers/service.py)

## See Also

- [Wallpapers Asset Documentation](../../assets/wallpapers.md)
- [WallpapersService API](../../python-api/services.md#wallpapersservice)
