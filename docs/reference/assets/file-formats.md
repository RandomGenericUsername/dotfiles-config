# Asset File Formats

[VERIFIED via CLI - 2026-01-03]

Technical documentation for asset file formats and structures.

## Wallpaper Archive Format

**File:** `assets/wallpapers/wallpapers.tar.gz`

**Format:** gzip-compressed tar archive

**MIME Type:** application/gzip

**Structure:**
```
wallpapers.tar.gz (tar.gz archive)
├── image1.png
├── image2.jpg
└── image3.webp
```

[VERIFIED via source - 2026-01-03]

**Characteristics:**
- Flat structure (no subdirectories)
- Image files only
- Hidden files (starting with `.`) are excluded
- File metadata preserved (timestamps, permissions)

[VERIFIED via source - 2026-01-03]

### Supported Image Formats

**Extensions:** jpg, jpeg, png, gif, bmp, webp, tiff, tif

**Case Sensitivity:** Extensions are case-insensitive (JPG, jpg, JpG all accepted)

[VERIFIED via source - 2026-01-03]

### Archive Operations

**Read operations:** Uses `tarfile.open(path, "r:gz")`

**Write operations:** Uses `tarfile.open(path, "w:gz")`

**Python module:** Standard library `tarfile`

[VERIFIED via source - 2026-01-03]

## Icon File Format

**Format:** SVG (Scalable Vector Graphics)

**MIME Type:** image/svg+xml

**Characteristics:**
- XML-based vector format
- Text files (can be edited in text editors)
- Resolution-independent
- Support for styling and animations

[VERIFIED via CLI - 2026-01-03]

**File extension:** `.svg`

**Total SVG files:** 48

[VERIFIED via CLI - 2026-01-03]

## Bash Script Format

**File:** `assets/wallpapers/manage_wallpapers.sh`

**Format:** Bash shell script

**Shebang:** Must include appropriate shebang line

**Permissions:** Executable bit required

[VERIFIED via CLI - 2026-01-03]

## Configuration Template Format

**File:** `config-files/zsh/.zshrc.j2`

**Format:** Jinja2 template

**File extension:** `.j2`

**Processor:** Ansible template module

**Usage:** Allows variable interpolation during deployment

[VERIFIED via CLI - 2026-01-03]

## See Also

- [Wallpapers Asset](wallpapers.md)
- [Icons Assets](icons.md)
- [Assets Index](index.md)
