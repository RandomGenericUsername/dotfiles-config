# Examples

[VERIFIED via CLI - 2026-01-03]

Practical, tested examples for using the dotfiles-config system.

## Contents

- [CLI Examples](#cli-examples) - Command-line usage examples
- [Python API Examples](#python-api-examples) - Using the Python API programmatically
- [Ansible Examples](#ansible-examples) - Using Ansible integration

## CLI Examples

All examples are verified and can be copy-pasted directly into your terminal.

### Basic Commands

**Show help:**

```bash
config --help
```

[VERIFIED via CLI - 2026-01-03]

**Test CLI installation:**

```bash
config dummy
```

Output: `This is a dummy command! It doesn't do much, but it works!`

[VERIFIED via CLI - 2026-01-03]

### Wallpaper Management

**List all wallpapers:**

```bash
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

Example output:
```
Wallpapers in archive (3):
  - mountain.jpg
  - ocean.png
  - sunset.webp
```

**Add a wallpaper:**

```bash
config assets wallpapers add ~/Pictures/my-wallpaper.png
```

[VERIFIED via CLI - 2026-01-03]

Output: `Successfully added 'my-wallpaper.png' to wallpapers archive`

**Add with force overwrite:**

```bash
config assets wallpapers add --force ~/Pictures/my-wallpaper.png
```

[VERIFIED via CLI - 2026-01-03]

**Add non-image file (skip validation):**

```bash
config assets wallpapers add --no-validate /path/to/file.txt
```

[VERIFIED via CLI - 2026-01-03]

**Extract wallpapers:**

```bash
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

Creates `~/Pictures/wallpapers/` with all wallpapers.

### Package Installation

**Install Neovim:**

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

**Show debug information:**

```bash
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

**Install with verbose output:**

```bash
config install-packages --tags nvim -vv --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

**Override destination:**

```bash
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test
```

[VERIFIED via CLI - 2026-01-03]

### Shell Completion

**Install completion:**

```bash
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

**Show completion script:**

```bash
config --show-completion
```

[VERIFIED via CLI - 2026-01-03]

## Python API Examples

Examples using the Python API directly.

### Using the API Classes (Recommended)

```python
from pathlib import Path
from src import Config

# Create Config instance (entry point)
cfg = Config()

# List wallpapers
wallpapers = cfg.assets.wallpapers.list()
print(f"Found {len(wallpapers)} wallpapers:")
for name in sorted(wallpapers):
    print(f"  - {name}")

# Add a wallpaper
wallpaper_path = Path("~/Pictures/sunset.jpg").expanduser()
cfg.assets.wallpapers.add(wallpaper_path, force=True)
print(f"Added {wallpaper_path.name}")

# Extract wallpapers
output_dir = cfg.assets.wallpapers.extract(Path("~/wallpapers").expanduser())
print(f"Extracted to {output_dir}")

# List packages
packages = cfg.packages.list()
for pkg in packages:
    print(f"Package: {pkg.name} (tags: {', '.join(pkg.tags)})")

# Install packages with tags
cfg.packages.install(tags=["nvim"])
```

[VERIFIED via source - 2026-01-04]

### WallpapersService Example (Lower-level)

```python
from pathlib import Path
from src.services.wallpapers_service import WallpapersService

# Initialize service
archive_path = Path("assets/wallpapers/wallpapers.tar.gz")
service = WallpapersService(archive_path)

# List wallpapers
wallpapers = service.list_wallpapers()
print(f"Found {len(wallpapers)} wallpapers:")
for name in sorted(wallpapers):
    print(f"  - {name}")

# Add a wallpaper
wallpaper_path = Path("~/Pictures/sunset.jpg").expanduser()
service.add_wallpaper(wallpaper_path, overwrite=True, validate_extension=True)
print(f"Added {wallpaper_path.name}")

# Extract wallpapers
output_dir = service.extract_wallpapers(Path("~/wallpapers").expanduser())
print(f"Extracted to {output_dir}")
```

[VERIFIED via source - 2026-01-04]

### Error Handling Example

```python
from pathlib import Path
from src.services.wallpapers_service import (
    WallpapersService,
    ArchiveNotFoundError,
    WallpaperNotFoundError,
    InvalidImageError,
    WallpaperError,
)

archive_path = Path("assets/wallpapers/wallpapers.tar.gz")
service = WallpapersService(archive_path)

try:
    service.add_wallpaper(Path("image.png"), overwrite=False)
except WallpaperNotFoundError:
    print("Image file doesn't exist")
except InvalidImageError as e:
    print(f"Not a valid image: {e}")
except WallpaperError as e:
    print(f"Wallpaper operation failed: {e}")
```

[VERIFIED via source - 2026-01-04]

### Validation Example

```python
from src.services.wallpapers_service import WallpapersService

# Check if file is a valid image
print(WallpapersService.is_valid_image_extension("sunset.jpg"))    # True
print(WallpapersService.is_valid_image_extension("sunset.PNG"))    # True
print(WallpapersService.is_valid_image_extension("document.txt"))  # False
print(WallpapersService.is_valid_image_extension("noextension"))   # False
```

[VERIFIED via source - 2026-01-04]

## Ansible Examples

Examples for using Ansible directly.

### Run Playbook Directly

From `packages/ansible/` directory:

```bash
cd packages/ansible
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

### List Available Tags

```bash
cd packages/ansible
ansible-playbook --list-tags -i inventory/localhost.yml playbooks/bootstrap.yml
```

[VERIFIED via CLI - 2026-01-03]

Output:
```
playbook: playbooks/bootstrap.yml

  play #1 (localhost): Dotfiles engine (local)	TAGS: []
      TASK TAGS: [debug, nvim]
```

### List Available Tasks

```bash
cd packages/ansible
ansible-playbook --list-tasks -i inventory/localhost.yml playbooks/bootstrap.yml
```

[VERIFIED via CLI - 2026-01-03]

Output:
```
playbook: playbooks/bootstrap.yml

  play #1 (localhost): Dotfiles engine (local)	TAGS: []
    tasks:
      Debug paths	TAGS: [debug]
      nvim : Install neovim	TAGS: [nvim]
      nvim : Ensure destination directory exists	TAGS: [nvim]
      nvim : Copy Neovim config directory	TAGS: [nvim]
```

## Complete Workflows

### Workflow 1: New System Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd dotfiles/config

# 2. Setup development environment
make install-dev

# 3. Activate virtual environment
make shell

# 4. Verify installation
config --help

# 5. Install packages
config install-packages --tags nvim --ask-become-pass

# 6. Extract wallpapers
config assets wallpapers extract ~/Pictures

# 7. Enable shell completion
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 2: Add and Manage Wallpapers

```bash
# 1. Check current wallpapers
config assets wallpapers list

# 2. Add new wallpapers
config assets wallpapers add ~/Downloads/wallpaper1.jpg
config assets wallpapers add ~/Downloads/wallpaper2.png
config assets wallpapers add ~/Downloads/wallpaper3.webp

# 3. Verify additions
config assets wallpapers list

# 4. Extract for use
config assets wallpapers extract ~/Pictures

# 5. Check extracted files
ls ~/Pictures/wallpapers/
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 3: Test Configuration Changes

```bash
# 1. Make changes to config files
vim config-files/nvim/init.lua

# 2. Test in temporary location
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test

# 3. Verify changes
ls -la /tmp/nvim-test
cat /tmp/nvim-test/init.lua

# 4. If good, deploy to real location
config install-packages --tags nvim

# 5. Clean up test
rm -rf /tmp/nvim-test
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 4: Development and Testing

```bash
# 1. Setup development environment
make install-dev
make shell

# 2. Make code changes
vim src/commands/mycommand.py

# 3. Run tests
make test-cov

# 4. Test CLI manually
config mycommand --help
config mycommand test-value

# 5. Update documentation
vim docs/reference/cli/mycommand.md

# 6. Final test
make test-cov
```

[VERIFIED via source - 2026-01-03]

## Testing Examples

### Run All Tests

```bash
uv run pytest -v
```

[VERIFIED via tests - 2026-01-03]

### Run with Coverage

```bash
uv run pytest -v --cov=src --cov-report=term-missing
```

[VERIFIED via tests - 2026-01-03]

### Run Specific Test File

```bash
uv run pytest tests/unit/test_wallpapers_service.py -v
```

[VERIFIED via tests - 2026-01-03]

### Run Specific Test

```bash
uv run pytest tests/unit/test_wallpapers_service.py::TestWallpapersServiceAdd::test_add_wallpaper_to_existing_archive -v
```

[VERIFIED via tests - 2026-01-03]

### List Tests

```bash
uv run pytest --collect-only
```

[VERIFIED via tests - 2026-01-03]

## Make Targets

All available Make commands:

```bash
make help              # Show available targets
make install           # Install package
make install-dev       # Install with dev dependencies
make shell             # Activate virtual environment
make clean             # Remove venv and build artifacts
make test              # Run all tests
make test-unit         # Run unit tests
make test-integration  # Run integration tests
make test-cov          # Run tests with coverage
```

[VERIFIED via source - 2026-01-03]

## See Also

- [CLI Reference](../reference/cli/index.md)
- [Python API Reference](../reference/python-api/index.md)
- [Usage Guides](../guides/usage/index.md)
- [First Steps](../getting-started/first-steps.md)
