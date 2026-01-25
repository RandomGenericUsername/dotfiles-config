# Feature Specifications

> **Document ID**: FS-001  
> **Version**: 1.0  
> **Date**: 2026-01-24  
> **Status**: Draft  
> **Source**: [001-refactoring-knowledge-base.md](001-refactoring-knowledge-base.md)

---

## Table of Contents

1. [Packages Module Features](#1-packages-module-features)
2. [Wallpapers Module Features](#2-wallpapers-module-features)
3. [Icon Templates Module Features](#3-icon-templates-module-features)
4. [Root Wrapper Features](#4-root-wrapper-features)

---

## 1. Packages Module Features

### FS-PKG-001: List Available Packages

**Feature ID**: FS-PKG-001  
**Requirement**: REQ-PKG-001  
**Priority**: High

#### Description
Display all available Ansible roles and their associated tags from the bootstrap playbook. This allows users to see what packages can be installed and which tags to use.

#### User Stories
- As a user, I want to see all available packages so I know what I can install
- As a user, I want to see the tags for each package so I can run specific installations

#### Acceptance Criteria
1. Command lists all roles defined in the playbook
2. Each role shows its name and associated tags
3. Output is formatted for readability
4. Shows total count of roles
5. Provides usage hint for install command

#### CLI Interface
```bash
$ dotfiles-packages list

Available packages (roles):

  • nvim                  [nvim]
  • zsh                   [zsh, shell]
  • docker                [docker, containers]

Total: 3 role(s)

Usage: dotfiles-packages install --tags <tag1,tag2>
```

#### Python API
```python
from dotfiles_packages import Packages, PackageRole

packages = Packages()
roles: list[PackageRole] = packages.list()

for role in roles:
    print(f"{role.name}: {role.tags}")
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Playbook not found | Raise `PlaybookNotFoundError`, CLI exits with code 1 |
| Playbook has no roles | Return empty list, CLI shows "No roles found" |
| Invalid YAML | Raise `PackagesError`, CLI exits with code 1 |

---

### FS-PKG-002: Install Packages

**Feature ID**: FS-PKG-002  
**Requirement**: REQ-PKG-002, REQ-PKG-003, REQ-PKG-004  
**Priority**: High

#### Description
Install system packages by executing the Ansible playbook with specified tags. Supports forwarding arbitrary arguments to ansible-playbook for full flexibility.

#### User Stories
- As a user, I want to install packages by tag so I can set up specific tools
- As a user, I want to pass additional ansible options so I can customize execution
- As a user, I want to see what command is being run for transparency

#### Acceptance Criteria
1. Executes ansible-playbook with the bootstrap playbook
2. Passes `--tags` option when tags are specified
3. Forwards all extra arguments to ansible-playbook
4. Shows the command being executed
5. Shows working directory
6. Returns ansible-playbook exit code

#### CLI Interface
```bash
# Basic usage with tags
$ dotfiles-packages install --tags nvim,zsh

Running: ansible-playbook --tags nvim,zsh
Working directory: /path/to/ansible
[ansible output...]

# With extra arguments
$ dotfiles-packages install --tags nvim --ask-become-pass --check

Running: ansible-playbook --tags nvim --ask-become-pass --check
Working directory: /path/to/ansible
[ansible output...]
```

#### Python API
```python
from dotfiles_packages import Packages

packages = Packages()

# Basic install
result = packages.install(tags=["nvim", "zsh"])
print(f"Exit code: {result.returncode}")

# With extra arguments
result = packages.install(
    tags=["nvim"],
    extra_args=["--ask-become-pass", "--check"]
)
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Ansible not installed | Raise `AnsibleNotFoundError`, CLI exits with code 1 |
| Playbook execution fails | Raise `AnsibleError` with return code, CLI exits with that code |
| Invalid tags | Ansible handles this, error propagates |

---

## 2. Wallpapers Module Features

### FS-WP-001: List Wallpapers

**Feature ID**: FS-WP-001  
**Requirement**: REQ-WP-001  
**Priority**: High

#### Description
Display all wallpaper filenames stored in the archive. Provides a quick overview of available wallpapers.

#### User Stories
- As a user, I want to see all my wallpapers so I know what's in the archive
- As a user, I want to see the count of wallpapers

#### Acceptance Criteria
1. Lists all files in the tar.gz archive
2. Excludes hidden files (starting with `.`)
3. Shows sorted list of filenames
4. Shows total count
5. Handles empty archive gracefully

#### CLI Interface
```bash
$ dotfiles-wallpapers list

Wallpapers in archive (3):
  - forest-morning.jpg
  - mountain-sunset.png
  - ocean-waves.jpg

# Empty archive
$ dotfiles-wallpapers list
No wallpapers in archive
```

#### Python API
```python
from dotfiles_wallpapers import Wallpapers

wallpapers = Wallpapers()
names: list[str] = wallpapers.list()

for name in names:
    print(name)
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Archive not found | Raise `ArchiveNotFoundError`, CLI exits with code 1 |
| Corrupted archive | Raise `WallpaperError`, CLI exits with code 1 |

---

### FS-WP-002: Add Wallpaper

**Feature ID**: FS-WP-002  
**Requirement**: REQ-WP-002, REQ-WP-004, REQ-WP-006  
**Priority**: High

#### Description
Add a wallpaper image to the archive. Supports validation, duplicate handling, and archive creation.

#### User Stories
- As a user, I want to add a wallpaper to my collection
- As a user, I want to be warned about invalid file types
- As a user, I want to optionally overwrite existing wallpapers
- As a user, I want the archive created automatically if it doesn't exist

#### Acceptance Criteria
1. Adds wallpaper file to tar.gz archive
2. Creates archive if it doesn't exist
3. Validates image extension by default (jpg, jpeg, png, gif, bmp, webp, tiff, tif)
4. Rejects duplicates unless `--force` is used
5. Supports `--no-validate` to skip extension check
6. Shows success message with filename

#### CLI Interface
```bash
# Basic add
$ dotfiles-wallpapers add ~/Pictures/new-wallpaper.jpg
Successfully added 'new-wallpaper.jpg' to wallpapers archive

# Force overwrite
$ dotfiles-wallpapers add ~/Pictures/existing.jpg --force
Successfully added 'existing.jpg' to wallpapers archive

# Skip validation
$ dotfiles-wallpapers add ~/Pictures/custom.svg --no-validate
Successfully added 'custom.svg' to wallpapers archive

# Error: duplicate
$ dotfiles-wallpapers add ~/Pictures/existing.jpg
Error: Wallpaper 'existing.jpg' already exists in archive. Use --force to overwrite.

# Error: invalid extension
$ dotfiles-wallpapers add ~/Documents/readme.txt
Error: File does not have a valid image extension: readme.txt
```

#### Python API
```python
from dotfiles_wallpapers import Wallpapers
from pathlib import Path

wallpapers = Wallpapers()

# Basic add
wallpapers.add(Path("~/Pictures/new.jpg"))

# Force overwrite
wallpapers.add(Path("~/Pictures/existing.jpg"), force=True)

# Skip validation
wallpapers.add(Path("~/Pictures/custom.svg"), validate=False)
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Source file not found | Raise `WallpaperNotFoundError`, CLI exits with code 1 |
| Invalid extension (validation on) | Raise `InvalidImageError`, CLI exits with code 1 |
| Duplicate without force | Raise `WallpaperError`, CLI exits with code 1 |

---

### FS-WP-003: Extract Wallpapers

**Feature ID**: FS-WP-003  
**Requirement**: REQ-WP-003  
**Priority**: High

#### Description
Extract all wallpapers from the archive to a specified directory. Creates a `wallpapers/` subdirectory in the target location.

#### User Stories
- As a user, I want to extract all wallpapers to use them
- As a user, I want to know where the wallpapers were extracted
- As a user, I want to know how many wallpapers were extracted

#### Acceptance Criteria
1. Extracts all files from archive
2. Creates `wallpapers/` subdirectory in target path
3. Creates target directory if it doesn't exist
4. Shows count and destination path
5. Overwrites existing files in destination

#### CLI Interface
```bash
$ dotfiles-wallpapers extract /tmp/my-wallpapers
Extracted 3 wallpaper(s) to /tmp/my-wallpapers/wallpapers

# Directory structure created:
# /tmp/my-wallpapers/
# └── wallpapers/
#     ├── forest-morning.jpg
#     ├── mountain-sunset.png
#     └── ocean-waves.jpg
```

#### Python API
```python
from dotfiles_wallpapers import Wallpapers
from pathlib import Path

wallpapers = Wallpapers()
result_path: Path = wallpapers.extract(Path("/tmp/my-wallpapers"))
print(f"Extracted to: {result_path}")
# result_path = /tmp/my-wallpapers/wallpapers
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Archive not found | Raise `ArchiveNotFoundError`, CLI exits with code 1 |
| Permission denied | Raise `WallpaperError`, CLI exits with code 1 |

---

## 3. Icon Templates Module Features

### FS-ICON-001: List Icon Templates

**Feature ID**: FS-ICON-001  
**Requirement**: REQ-ICON-001, REQ-ICON-002  
**Priority**: High

#### Description
List available icon templates, optionally filtered by category. Shows categories and icons within them.

#### User Stories
- As a user, I want to see all available icon categories
- As a user, I want to see icons within a specific category
- As a user, I want to see icon counts

#### Acceptance Criteria
1. Lists all categories when no filter applied
2. Lists icons in category when `--category` specified
3. Shows icon count per category
4. Shows total count

#### CLI Interface
```bash
# List categories
$ dotfiles-icon-templates list

Available icon categories:

  • screenshot-tool       (5 icons)
  • status-bar           (12 icons)
  • wlogout              (8 icons)

Total: 3 categories, 25 icons

# List icons in category
$ dotfiles-icon-templates list --category status-bar

Icons in 'status-bar':

  • battery-charging.svg
  • battery-full.svg
  • battery-low.svg
  • network-connected.svg
  • network-disconnected.svg
  ...

Total: 12 icons
```

#### Python API
```python
from dotfiles_icon_templates import IconTemplates

icons = IconTemplates()

# Get categories
categories: list[str] = icons.categories()

# Get all icons
all_icons = icons.list()

# Get icons in category
status_icons = icons.list(category="status-bar")
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Data directory not found | Raise `IconTemplateError`, CLI exits with code 1 |
| Category not found | Raise `CategoryNotFoundError`, CLI exits with code 1 |

---

### FS-ICON-002: Copy Icon Templates

**Feature ID**: FS-ICON-002  
**Requirement**: REQ-ICON-004  
**Priority**: High

#### Description
Copy icon templates to a target directory. Supports filtering by category and specific icon names.

#### User Stories
- As a user, I want to copy all icons to my config directory
- As a user, I want to copy only icons from a specific category
- As a user, I want to copy specific icons by name

#### Acceptance Criteria
1. Copies icons to target directory
2. Creates target directory if needed
3. Supports `--category` filter
4. Supports `--icons` filter for specific icons
5. Shows list of copied files
6. Shows total count

#### CLI Interface
```bash
# Copy all icons
$ dotfiles-icon-templates copy ~/.config/icons/
Copied 25 icon(s) to /home/user/.config/icons/

# Copy specific category
$ dotfiles-icon-templates copy ~/.config/waybar/icons --category status-bar
Copied 12 icon(s) to /home/user/.config/waybar/icons/

# Copy specific icons
$ dotfiles-icon-templates copy ~/.config/wlogout/ --icons lock,logout,shutdown
Copied 3 icon(s) to /home/user/.config/wlogout/
```

#### Python API
```python
from dotfiles_icon_templates import IconTemplates
from pathlib import Path

icons = IconTemplates()

# Copy all
copied = icons.copy(Path("~/.config/icons"))

# Copy category
copied = icons.copy(
    Path("~/.config/waybar/icons"),
    category="status-bar"
)

# Copy specific icons
copied = icons.copy(
    Path("~/.config/wlogout"),
    icons=["lock", "logout", "shutdown"]
)
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Target not writable | Raise `IconTemplateError`, CLI exits with code 1 |
| Category not found | Raise `CategoryNotFoundError`, CLI exits with code 1 |
| Icon not found | Raise `IconNotFoundError`, CLI exits with code 1 |

---

### FS-ICON-003: Show Icon Details

**Feature ID**: FS-ICON-003  
**Requirement**: REQ-ICON-003  
**Priority**: Medium

#### Description
Display detailed information about a specific icon template.

#### User Stories
- As a user, I want to see details about a specific icon
- As a user, I want to know the file path of an icon
- As a user, I want to see available variants

#### Acceptance Criteria
1. Shows icon name
2. Shows category
3. Shows file path
4. Shows available variants (if any)

#### CLI Interface
```bash
$ dotfiles-icon-templates show battery-full

Icon: battery-full

  Category:  status-bar
  Path:      /path/to/data/status-bar/battery-full.svg
  Variants:  default, rounded, sharp
```

#### Python API
```python
from dotfiles_icon_templates import IconTemplates, IconInfo

icons = IconTemplates()
info: IconInfo = icons.show("battery-full")

print(f"Name: {info.name}")
print(f"Category: {info.category}")
print(f"Path: {info.path}")
print(f"Variants: {info.variants}")
```

#### Error Scenarios
| Scenario | Behavior |
|----------|----------|
| Icon not found | Raise `IconNotFoundError`, CLI exits with code 1 |

---

## 4. Root Wrapper Features

### FS-ROOT-001: CLI Aggregation

**Feature ID**: FS-ROOT-001  
**Requirement**: REQ-ROOT-002  
**Priority**: High

#### Description
The root `dotfiles-config` CLI aggregates all subproject CLIs under a single command.

#### User Stories
- As a user, I want a single command to access all functionality
- As a user, I want familiar subcommand structure

#### Acceptance Criteria
1. `dotfiles-config packages` routes to dotfiles-packages CLI
2. `dotfiles-config wallpapers` routes to dotfiles-wallpapers CLI
3. `dotfiles-config icon-templates` routes to dotfiles-icon-templates CLI
4. Help text shows all available subcommands

#### CLI Interface
```bash
$ dotfiles-config --help

Usage: dotfiles-config [OPTIONS] COMMAND [ARGS]...

  Dotfiles configuration management

Options:
  --help  Show this message and exit.

Commands:
  packages        Manage system packages
  wallpapers      Manage wallpaper assets
  icon-templates  Manage icon templates

$ dotfiles-config packages list
[same as: dotfiles-packages list]

$ dotfiles-config wallpapers add ~/pic.jpg
[same as: dotfiles-wallpapers add ~/pic.jpg]
```

---

### FS-ROOT-002: API Re-exports

**Feature ID**: FS-ROOT-002  
**Requirement**: REQ-ROOT-003  
**Priority**: High

#### Description
The root package re-exports public APIs from all subprojects for convenience.

#### User Stories
- As a developer, I want to import all APIs from one package
- As a developer, I want consistent access to all functionality

#### Acceptance Criteria
1. `Packages` class importable from `dotfiles_config`
2. `Wallpapers` class importable from `dotfiles_config`
3. `IconTemplates` class importable from `dotfiles_config`

#### Python API
```python
# All from root
from dotfiles_config import Packages, Wallpapers, IconTemplates

# Or individually
from dotfiles_packages import Packages
from dotfiles_wallpapers import Wallpapers
from dotfiles_icon_templates import IconTemplates
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | AI Assistant | Initial creation |
