# Services API

[VERIFIED via source - 2026-01-04]

Core service layer for business logic operations.

## src.services.wallpapers_service

Wallpaper management service.

**Source:** [src/services/wallpapers_service.py:1](../../../src/services/wallpapers_service.py#L1)

---

## Exception Classes

### `WallpaperError`

Base exception for wallpaper operations.

```python
class WallpaperError(Exception):
    pass
```

[VERIFIED via source - 2026-01-03]

### `ArchiveNotFoundError`

Raised when the wallpaper archive doesn't exist.

```python
class ArchiveNotFoundError(WallpaperError):
    pass
```

[VERIFIED via source - 2026-01-03]

### `WallpaperNotFoundError`

Raised when a wallpaper file doesn't exist.

```python
class WallpaperNotFoundError(WallpaperError):
    pass
```

[VERIFIED via source - 2026-01-03]

### `InvalidImageError`

Raised when a file is not a valid image.

```python
class InvalidImageError(WallpaperError):
    pass
```

[VERIFIED via source - 2026-01-03]

---

## WallpapersService

Service for managing wallpapers in a tar.gz archive.

**Source:** [src/commands/assets/wallpapers/service.py:34](../../../src/commands/assets/wallpapers/service.py#L34)

### Class Attributes

#### `VALID_EXTENSIONS: frozenset`

Set of recognized image file extensions (case-insensitive).

```python
VALID_EXTENSIONS = frozenset([
    "jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff", "tif"
])
```

[VERIFIED via source - 2026-01-03]

### Constructor

#### `__init__(archive_path)`

Initialize the service with the archive path.

```python
def __init__(self, archive_path: Path) -> None
```

**Parameters:**

- `archive_path: Path` - Path to the wallpapers.tar.gz archive

[VERIFIED via source - 2026-01-03]

### Class Methods

#### `is_valid_image_extension(filename)`

Check if a filename has a valid image extension.

```python
@classmethod
def is_valid_image_extension(cls, filename: str) -> bool
```

**Parameters:**

- `filename: str` - The filename to check

**Returns:** `True` if the extension is a recognized image format, `False` otherwise

**Algorithm:**

1. Returns `False` if filename has no extension
2. Extracts extension (everything after last `.`)
3. Converts extension to lowercase
4. Checks if extension is in `VALID_EXTENSIONS`

[VERIFIED via source - 2026-01-03]

**Examples:**

```python
WallpapersService.is_valid_image_extension("sunset.png")      # True
WallpapersService.is_valid_image_extension("sunset.PNG")      # True
WallpapersService.is_valid_image_extension("document.txt")    # False
WallpapersService.is_valid_image_extension("noextension")     # False
```

[VERIFIED via tests - 2026-01-03]

### Instance Methods

#### `list_wallpapers()`

List all wallpaper names in the archive.

```python
def list_wallpapers(self) -> List[str]
```

**Returns:** List of wallpaper filenames

**Raises:** `ArchiveNotFoundError` if archive doesn't exist

**Behavior:**

1. Checks if archive exists
2. Opens tar.gz archive
3. Filters for files only (excludes directories)
4. Excludes hidden files (starting with `.`)
5. Returns list of filenames

[VERIFIED via source - 2026-01-03]

#### `add_wallpaper(wallpaper_path, overwrite, validate_extension)`

Add a wallpaper to the archive.

```python
def add_wallpaper(
    self,
    wallpaper_path: Path,
    overwrite: bool = True,
    validate_extension: bool = True,
) -> None
```

**Parameters:**

- `wallpaper_path: Path` - Path to the wallpaper file
- `overwrite: bool` - If True, replace existing wallpaper with same name (default: True)
- `validate_extension: bool` - If True, validate file has image extension (default: True)

**Raises:**

- `WallpaperNotFoundError` - If wallpaper file doesn't exist
- `InvalidImageError` - If file doesn't have valid image extension (when validate_extension=True)
- `WallpaperError` - If wallpaper exists and overwrite=False

[VERIFIED via source - 2026-01-03]

**Algorithm:**

1. Resolves wallpaper_path to absolute path (handles relative paths)
2. Checks if file exists
3. Validates extension if validate_extension=True
4. If archive exists, checks for duplicate and raises if overwrite=False
5. Creates temporary directory
6. Extracts existing archive to temp directory (if archive exists)
7. Copies new wallpaper to temp directory (overwrites if exists)
8. Creates parent directory for archive if needed
9. Creates new tar.gz archive with all files in temp directory
10. Excludes hidden files (starting with `.`)

[VERIFIED via source - 2026-01-03]

#### `extract_wallpapers(output_path)`

Extract all wallpapers to a directory.

```python
def extract_wallpapers(self, output_path: Path) -> Path
```

**Parameters:**

- `output_path: Path` - Parent directory for extraction

**Returns:** Path to the 'wallpapers' subdirectory containing extracted files

**Raises:** `ArchiveNotFoundError` if archive doesn't exist

**Behavior:**

1. Checks if archive exists
2. Creates `wallpapers` subdirectory in output_path
3. Creates parent directories if they don't exist
4. Extracts all archive contents to wallpapers subdirectory
5. Returns path to wallpapers subdirectory

[VERIFIED via source - 2026-01-03]

**Example:**

```python
service = WallpapersService(Path("wallpapers.tar.gz"))
result = service.extract_wallpapers(Path("/home/user/Pictures"))
# Creates /home/user/Pictures/wallpapers/
# Returns Path("/home/user/Pictures/wallpapers")
```

[VERIFIED via tests - 2026-01-03]

---

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from src.services.wallpapers_service import WallpapersService

# Initialize service
service = WallpapersService(Path("assets/wallpapers/wallpapers.tar.gz"))

# List wallpapers
wallpapers = service.list_wallpapers()
print(f"Found {len(wallpapers)} wallpapers")

# Add a wallpaper
service.add_wallpaper(Path("~/Pictures/sunset.jpg"))

# Add with validation disabled
service.add_wallpaper(Path("file.txt"), validate_extension=False)

# Extract wallpapers
output_dir = service.extract_wallpapers(Path("~/wallpapers"))
print(f"Extracted to {output_dir}")
```

[VERIFIED via source - 2026-01-04]

### Error Handling

```python
from src.services.wallpapers_service import (
    WallpapersService,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
    WallpaperError,
)

service = WallpapersService(Path("wallpapers.tar.gz"))

try:
    service.add_wallpaper(Path("image.png"), overwrite=False)
except WallpaperNotFoundError:
    print("Image file doesn't exist")
except InvalidImageError:
    print("Not a valid image file")
except WallpaperError as e:
    print(f"Duplicate wallpaper: {e}")
```

[VERIFIED via source - 2026-01-04]

---

## src.services.packages_service

Package management service for Ansible playbook execution.

**Source:** [src/services/packages_service.py:1](../../../src/services/packages_service.py#L1)

### Exception Classes

#### `PackagesError`

Base exception for package operations.

```python
class PackagesError(Exception):
    pass
```

[VERIFIED via source - 2026-01-04]

#### `PlaybookNotFoundError`

Raised when the Ansible playbook doesn't exist.

```python
class PlaybookNotFoundError(PackagesError):
    pass
```

[VERIFIED via source - 2026-01-04]

#### `AnsibleError`

Raised when Ansible command execution fails.

```python
class AnsibleError(PackagesError):
    def __init__(self, message: str, return_code: int) -> None:
        self.return_code = return_code
        super().__init__(message)
```

[VERIFIED via source - 2026-01-04]

#### `AnsibleNotFoundError`

Raised when Ansible is not installed.

```python
class AnsibleNotFoundError(PackagesError):
    pass
```

[VERIFIED via source - 2026-01-04]

### PackageRole Dataclass

Represents a package role with its metadata.

```python
@dataclass
class PackageRole:
    name: str           # Role name (e.g., 'nvim')
    tags: List[str]     # Available tags for this role
```

[VERIFIED via source - 2026-01-04]

### PackagesService

Service for managing package installation via Ansible.

**Source:** [src/services/packages_service.py:60](../../../src/services/packages_service.py#L60)

#### Constructor

#### `__init__(playbook_path, ansible_dir)`

Initialize the service with playbook and Ansible directory paths.

```python
def __init__(
    self,
    playbook_path: Path,
    ansible_dir: Path,
) -> None
```

**Parameters:**

- `playbook_path: Path` - Path to the Ansible playbook file
- `ansible_dir: Path` - Path to the Ansible directory

[VERIFIED via source - 2026-01-04]

#### Instance Methods

#### `list_packages()`

List all available package roles with their tags.

```python
def list_packages(self) -> List[PackageRole]
```

**Returns:** List of `PackageRole` objects

**Raises:** `PlaybookNotFoundError` if playbook doesn't exist, `AnsibleNotFoundError` if Ansible is not installed

**Behavior:**

1. Validates that playbook exists
2. Validates that Ansible is installed
3. Parses Ansible playbook for available roles
4. Extracts tags for each role
5. Returns list of PackageRole objects

[VERIFIED via source - 2026-01-04]

#### `install(tags, extra_args)`

Install packages by running Ansible with specified tags.

```python
def install(
    self,
    tags: Optional[List[str]] = None,
    extra_args: Optional[List[str]] = None,
) -> subprocess.CompletedProcess
```

**Parameters:**

- `tags: Optional[List[str]]` - Tags to select which packages to install (default: None, runs all)
- `extra_args: Optional[List[str]]` - Additional arguments to pass to Ansible (default: None)

**Returns:** `subprocess.CompletedProcess` with returncode, stdout, stderr

**Raises:**

- `PlaybookNotFoundError` - If playbook doesn't exist
- `AnsibleNotFoundError` - If Ansible is not installed
- `AnsibleError` - If Ansible execution fails (return code != 0)

**Behavior:**

1. Validates that playbook exists
2. Validates that Ansible is installed
3. Constructs Ansible command with tags
4. Appends extra arguments
5. Executes Ansible playbook
6. Raises AnsibleError if command fails

[VERIFIED via source - 2026-01-04]

### Usage Examples

#### List Available Packages

```python
from pathlib import Path
from src.services.packages_service import PackagesService

service = PackagesService(
    playbook_path=Path("packages/ansible/playbooks/bootstrap.yml"),
    ansible_dir=Path("packages/ansible"),
)

# List all available packages
packages = service.list_packages()
for pkg in packages:
    print(f"{pkg.name}: {', '.join(pkg.tags)}")
```

[VERIFIED via source - 2026-01-04]

#### Install Packages with Tags

```python
from src.services.packages_service import PackagesService

service = PackagesService(
    playbook_path=Path("packages/ansible/playbooks/bootstrap.yml"),
    ansible_dir=Path("packages/ansible"),
)

# Install specific packages by tag
result = service.install(tags=["nvim", "zsh"])
print(f"Installation exit code: {result.returncode}")
```

[VERIFIED via source - 2026-01-04]

#### Error Handling

```python
from src.services.packages_service import (
    PackagesService,
    PlaybookNotFoundError,
    AnsibleNotFoundError,
    AnsibleError,
    PackagesError,
)

service = PackagesService(
    playbook_path=Path("packages/ansible/playbooks/bootstrap.yml"),
    ansible_dir=Path("packages/ansible"),
)

try:
    packages = service.list_packages()
except PlaybookNotFoundError:
    print("Playbook file not found")
except AnsibleNotFoundError:
    print("Ansible is not installed")
except PackagesError as e:
    print(f"Package error: {e}")

try:
    result = service.install(tags=["nvim"])
except AnsibleError as e:
    print(f"Installation failed with code {e.return_code}")
```

[VERIFIED via source - 2026-01-04]

---

## See Also

- [Commands API](commands.md) - CLI command implementations
- [API Classes](api-classes.md) - Public API layer documentation
- [Wallpapers CLI](../cli/assets/wallpapers.md) - Command-line usage
