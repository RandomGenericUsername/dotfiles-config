# Public API Classes

[VERIFIED via source - 2026-01-04]

High-level API classes providing the recommended interface for using the dotfiles-config system programmatically.

## Overview

The public API is organized around the `Config` class, which serves as the entry point. All functionality is accessed through properties and methods of this class and its related facades.

**Recommended import:**

```python
from src import Config

cfg = Config()
cfg.assets.wallpapers.list()
cfg.packages.list()
```

[VERIFIED via source - 2026-01-04]

---

## Config Class

The primary entry point for programmatic access to the system.

**Source:** [src/api/config.py:1](../../../src/api/config.py#L1)

### Description

`Config` provides lazy-loaded access to all system subsystems (assets, packages). It's designed to be simple to instantiate and use.

### Constructor

#### `__init__()`

Create a new Config instance.

```python
cfg = Config()
```

No parameters required.

[VERIFIED via source - 2026-01-04]

### Properties

#### `assets`

Lazy-loaded Assets instance for managing application assets.

```python
@property
def assets(self) -> Assets
```

**Returns:** `Assets` instance

**Behavior:**
- Created on first access
- Same instance returned on subsequent accesses (singleton per Config instance)
- Never raises errors during construction

**Example:**

```python
cfg = Config()
wallpapers = cfg.assets.wallpapers.list()
```

[VERIFIED via source - 2026-01-04]

#### `packages`

Lazy-loaded Packages instance for managing package installation.

```python
@property
def packages(self) -> Packages
```

**Returns:** `Packages` instance

**Behavior:**
- Created on first access
- Same instance returned on subsequent accesses (singleton per Config instance)
- Never raises errors during construction

**Example:**

```python
cfg = Config()
roles = cfg.packages.list()
```

[VERIFIED via source - 2026-01-04]

### Usage Examples

#### Basic Usage

```python
from src import Config

# Create Config instance
cfg = Config()

# Access wallpapers via assets
wallpapers = cfg.assets.wallpapers.list()
print(f"Found {len(wallpapers)} wallpapers")

# Access packages
packages = cfg.packages.list()
for pkg in packages:
    print(f"  - {pkg.name}")

# Install packages
cfg.packages.install(tags=["nvim"])

# Add a wallpaper
from pathlib import Path
cfg.assets.wallpapers.add(Path("image.jpg"), force=True)
```

[VERIFIED via source - 2026-01-04]

#### Multiple Instances

```python
from src import Config

# Each Config instance has its own subsystem instances
cfg1 = Config()
cfg2 = Config()

# Different Config instances have different Assets/Packages
assert cfg1 is not cfg2
assert cfg1.assets is not cfg2.assets
assert cfg1.packages is not cfg2.packages

# But within same Config, accessing the same property returns same object
assert cfg1.assets is cfg1.assets
```

[VERIFIED via source - 2026-01-04]

---

## Assets Class

Facade providing access to asset management functionality.

**Source:** [src/api/assets.py:1](../../../src/api/assets.py#L1)

### Description

`Assets` provides access to asset-related operations, primarily wallpaper management through the `wallpapers` property.

### Constructor

#### `__init__()`

Create a new Assets instance.

```python
assets = Assets()
```

Can be instantiated independently, though typically accessed via `Config.assets`.

[VERIFIED via source - 2026-01-04]

### Properties

#### `wallpapers`

Lazy-loaded Wallpapers instance for wallpaper management.

```python
@property
def wallpapers(self) -> Wallpapers
```

**Returns:** `Wallpapers` instance

**Behavior:**
- Created on first access
- Same instance returned on subsequent accesses

**Example:**

```python
assets = Assets()
wallpapers = assets.wallpapers.list()
```

[VERIFIED via source - 2026-01-04]

---

## Packages Class

API for managing package installation via Ansible.

**Source:** [src/api/packages.py:1](../../../src/api/packages.py#L1)

### Description

`Packages` provides high-level methods for listing available packages and installing them by tag.

### Constructor

#### `__init__(playbook_path=None, ansible_dir=None)`

Create a new Packages instance.

```python
packages = Packages(
    playbook_path=None,      # Uses default if not provided
    ansible_dir=None,        # Uses default if not provided
)
```

**Parameters:**

- `playbook_path: Optional[Path]` - Path to Ansible playbook (default: `{cwd}/packages/ansible/playbooks/bootstrap.yml`)
- `ansible_dir: Optional[Path]` - Path to Ansible directory (default: `{cwd}/packages/ansible`)

**Default Behavior:**
If parameters are not provided, defaults are constructed relative to the current working directory.

[VERIFIED via source - 2026-01-04]

### Methods

#### `list()`

List all available packages with their tags.

```python
def list(self) -> List[PackageRole]
```

**Returns:** List of `PackageRole` objects

**Example:**

```python
packages = Packages()
roles = packages.list()
for role in roles:
    print(f"{role.name}: {', '.join(role.tags)}")
```

[VERIFIED via source - 2026-01-04]

#### `install(tags=None, extra_args=None)`

Install packages by running Ansible with specified tags.

```python
def install(
    self,
    tags: Optional[List[str]] = None,
    extra_args: Optional[List[str]] = None,
) -> None
```

**Parameters:**

- `tags: Optional[List[str]]` - Tags to select which packages to install
- `extra_args: Optional[List[str]]` - Additional arguments to pass to Ansible

**Example:**

```python
packages = Packages()
# Install specific packages
packages.install(tags=["nvim", "zsh"])

# Install with additional Ansible arguments
packages.install(tags=["nvim"], extra_args=["--ask-become-pass"])
```

[VERIFIED via source - 2026-01-04]

---

## Wallpapers Class

API for managing wallpapers.

**Source:** [src/api/wallpapers.py:1](../../../src/api/wallpapers.py#L1)

### Description

`Wallpapers` provides methods for managing wallpapers stored in a compressed archive.

### Constructor

#### `__init__(archive_path=None)`

Create a new Wallpapers instance.

```python
wallpapers = Wallpapers(
    archive_path=None,  # Uses default if not provided
)
```

**Parameters:**

- `archive_path: Optional[Path]` - Path to wallpapers archive (default: `{config_root}/assets/wallpapers/wallpapers.tar.gz`)

**Default Behavior:**
If not provided, uses the default archive location relative to the config root.

[VERIFIED via source - 2026-01-04]

### Methods

#### `list()`

List all wallpaper filenames.

```python
def list(self) -> List[str]
```

**Returns:** List of wallpaper filenames

**Example:**

```python
wallpapers = Wallpapers()
names = wallpapers.list()
for name in sorted(names):
    print(f"  - {name}")
```

[VERIFIED via source - 2026-01-04]

#### `add(path, force=False, validate=True)`

Add a wallpaper to the archive.

```python
def add(
    self,
    path: Path,
    force: bool = False,
    validate: bool = True,
) -> None
```

**Parameters:**

- `path: Path` - Path to the wallpaper file
- `force: bool` - If True, overwrite existing wallpaper with same name (default: False)
- `validate: bool` - If True, validate file has image extension (default: True)

**Raises:**
- `WallpaperNotFoundError` - If wallpaper file doesn't exist
- `InvalidImageError` - If file doesn't have valid image extension (when validate=True)
- `WallpaperError` - If wallpaper exists and force=False

**Example:**

```python
from pathlib import Path
wallpapers = Wallpapers()

# Add with defaults (no overwrite, validation enabled)
wallpapers.add(Path("image.jpg"))

# Add with force overwrite
wallpapers.add(Path("image.jpg"), force=True)

# Add without validation
wallpapers.add(Path("file.txt"), validate=False)
```

[VERIFIED via source - 2026-01-04]

#### `extract(path)`

Extract all wallpapers to a directory.

```python
def extract(self, path: Path) -> Path
```

**Parameters:**

- `path: Path` - Destination directory

**Returns:** Path to the extracted wallpapers subdirectory

**Example:**

```python
from pathlib import Path
wallpapers = Wallpapers()
result_dir = wallpapers.extract(Path.home() / "Pictures")
print(f"Extracted to: {result_dir}")
```

[VERIFIED via source - 2026-01-04]

---

## PackageRole Dataclass

Represents a package role with its metadata.

**Source:** [src/services/packages_service.py:1](../../../src/services/packages_service.py#L1)

```python
@dataclass
class PackageRole:
    name: str           # Role name (e.g., 'nvim')
    tags: List[str]     # Available tags for this role
```

[VERIFIED via source - 2026-01-04]

### Attributes

#### `name: str`

The name of the package role.

**Example:** `"nvim"`, `"zsh"`

#### `tags: List[str]`

List of tags available for this role.

**Example:** `["editor", "development"]`

### Usage

```python
from src import Config

cfg = Config()
roles = cfg.packages.list()

for role in roles:
    print(f"Role: {role.name}")
    print(f"  Tags: {', '.join(role.tags)}")
```

[VERIFIED via source - 2026-01-04]

---

## Error Handling

### Wallpaper Errors

```python
from src import Config
from src.services.wallpapers_service import (
    WallpaperError,
    WallpaperNotFoundError,
    InvalidImageError,
    ArchiveNotFoundError,
)

cfg = Config()

try:
    cfg.assets.wallpapers.add(Path("image.jpg"))
except WallpaperNotFoundError:
    print("Image file not found")
except InvalidImageError:
    print("Not a valid image format")
except WallpaperError as e:
    print(f"Wallpaper error: {e}")
```

[VERIFIED via source - 2026-01-04]

### Package Errors

```python
from src import Config
from src.services.packages_service import (
    PackagesError,
    PlaybookNotFoundError,
    AnsibleNotFoundError,
    AnsibleError,
)

cfg = Config()

try:
    cfg.packages.list()
except PlaybookNotFoundError:
    print("Playbook not found")
except AnsibleNotFoundError:
    print("Ansible not installed")
except AnsibleError as e:
    print(f"Ansible failed with code {e.return_code}")
except PackagesError as e:
    print(f"Package error: {e}")
```

[VERIFIED via source - 2026-01-04]

---

## Import Patterns

### Recommended: Top-level imports

```python
from src import Config, Assets, Packages, Wallpapers
```

Simplest and most convenient for most use cases.

[VERIFIED via source - 2026-01-04]

### Alternative: Direct API imports

```python
from src.api import Config, Assets, Packages, Wallpapers
```

Explicit about importing from the API layer.

[VERIFIED via source - 2026-01-04]

### Advanced: Service layer imports

For direct service access when needed:

```python
from src.services.wallpapers_service import WallpapersService
from src.services.packages_service import PackagesService
```

[VERIFIED via source - 2026-01-04]

---

## Design Principles

### Lazy Loading

Properties like `Config.assets` and `Config.packages` use lazy loading:
- Created only when first accessed
- Cached for subsequent accesses
- Enables efficient resource usage

[VERIFIED via source - 2026-01-04]

### Facade Pattern

`Assets` provides a facade pattern, abstracting away implementation details and providing a simplified interface.

[VERIFIED via source - 2026-01-04]

### Single Responsibility

Each class has a clear, focused responsibility:
- `Config` - Entry point and property access
- `Assets` - Asset management facade
- `Packages` - Package installation interface
- `Wallpapers` - Wallpaper management

[VERIFIED via source - 2026-01-04]

---

## See Also

- [Services](services.md) - Lower-level service layer documentation
- [Python API Reference](index.md) - Complete API documentation
- [Examples](../../../docs/examples/index.md) - Practical usage examples
