# Python API Reference

[VERIFIED via source - 2026-01-04]

Complete Python API documentation for the dotfiles-config system.

## Module Structure

```
src/
├── __init__.py                      - Public API exports (Config, Assets, Packages, Wallpapers)
├── main.py                          - CLI application entry point
├── api/                             - Public API layer
│   ├── __init__.py                  - API exports
│   ├── config.py                    - Config entry point class
│   ├── assets.py                    - Assets facade class
│   ├── packages.py                  - Packages API class
│   └── wallpapers.py                - Wallpapers API class
├── services/                        - Business logic layer
│   ├── __init__.py
│   ├── packages_service.py          - PackagesService
│   └── wallpapers_service.py        - WallpapersService (MOVED from commands/)
└── commands/
    ├── __init__.py                  - Commands package
    ├── dummy.py                     - Dummy command implementation
    ├── install_packages.py          - Package installation command
    └── assets/
        ├── __init__.py              - Assets command group
        └── wallpapers/
            ├── __init__.py          - Wallpapers CLI commands
            └── (service moved to src/services/)
```

[VERIFIED via CLI - 2026-01-04]

## Documentation Sections

- [API Classes](api-classes.md) - Public API layer (Config, Assets, Packages, Wallpapers)
- [Commands](commands.md) - CLI command implementations
- [Services](services.md) - Core service layer (WallpapersService, PackagesService)

## Quick Reference

### Top-Level API (Recommended)

**Module:** `src`

```python
from src import Config, Assets, Packages, Wallpapers
```

Entry point for using the library. Start here for most use cases.

[VERIFIED via source - 2026-01-04]

### API Layer

**Module:** `src.api`

```python
from src.api import Config, Assets, Packages, Wallpapers
```

Public API classes providing high-level interfaces to functionality.

[VERIFIED via source - 2026-01-04]

**Config Class** - Entry point for API usage:
```python
from src import Config

cfg = Config()
cfg.assets.wallpapers.list()
cfg.packages.list()
```

**Assets Class** - Facade for asset management:
```python
from src.api import Assets

assets = Assets()
wallpapers = assets.wallpapers
```

**Packages Class** - Package management:
```python
from src.api import Packages

packages = Packages()
roles = packages.list()
packages.install(tags=["nvim"])
```

**Wallpapers Class** - Wallpaper management:
```python
from src.api import Wallpapers

wallpapers = Wallpapers()
wallpapers.list()
wallpapers.add(Path("image.png"))
```

[VERIFIED via source - 2026-01-04]

### Service Layer

**Module:** `src.services.wallpapers_service`

```python
from src.services.wallpapers_service import (
    WallpapersService,
    WallpaperError,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
)
```

[VERIFIED via source - 2026-01-04]

**Module:** `src.services.packages_service`

```python
from src.services.packages_service import (
    PackagesService,
    PackagesError,
    PlaybookNotFoundError,
    AnsibleError,
    AnsibleNotFoundError,
    PackageRole,
)
```

[VERIFIED via source - 2026-01-04]

### Commands (CLI Layer)

**Module:** `src.commands.dummy`

```python
from src.commands.dummy import dummy
```

[VERIFIED via source - 2026-01-04]

**Module:** `src.commands.install_packages`

```python
from src.commands.install_packages import install_packages
```

[VERIFIED via source - 2026-01-04]

**Module:** `src.commands.assets`

```python
from src.commands.assets import assets_app
```

[VERIFIED via source - 2026-01-04]

**Module:** `src.commands.assets.wallpapers`

```python
from src.commands.assets.wallpapers import (
    wallpapers_app,
    add_wallpaper,
    extract_wallpapers,
    list_wallpapers,
    get_service,
    get_default_archive_path,
)
```

[VERIFIED via source - 2026-01-04]

### Main Application

**Module:** `src.main`

```python
from src.main import main, app
```

- `app: Typer` - Main Typer application instance
- `main()` - Entry point function

[VERIFIED via source - 2026-01-04]

## See Also

- [CLI Reference](../cli/index.md) - Command-line interface documentation
