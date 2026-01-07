# Commands API

[VERIFIED via source - 2026-01-03]

API documentation for CLI command implementations.

## src.main

Main application entry point.

**Source:** [src/main.py:1](../../../src/main.py#L1)

### `app: Typer`

Main Typer application instance.

```python
app = Typer(help="Dotfiles configuration management CLI")
```

[VERIFIED via source - 2026-01-03]

### `main()`

CLI entry point function. Called when running `config` command.

```python
def main() -> None
```

[VERIFIED via source - 2026-01-03]

---

## src.commands.dummy

Example dummy command.

**Source:** [src/commands/dummy.py:1](../../../src/commands/dummy.py#L1)

### `dummy()`

A dummy command that prints a message.

```python
def dummy() -> None
```

**Output:** `"This is a dummy command! It doesn't do much, but it works!"`

[VERIFIED via source - 2026-01-03]

---

## src.commands.install_packages

Ansible package installation command.

**Source:** [src/commands/install_packages.py:1](../../../src/commands/install_packages.py#L1)

### `install_packages()`

Install packages using Ansible playbook.

```python
def install_packages(
    ctx: typer.Context,
    tags: Optional[List[str]] = typer.Option(None, "--tags", help="Ansible tags to run"),
) -> None
```

**Parameters:**

- `ctx` - Typer context containing extra arguments
- `tags` - Optional list of Ansible tags to execute

**Behavior:**

1. Locates the Ansible playbook at `packages/ansible/playbooks/bootstrap.yml`
2. Builds an `ansible-playbook` command with optional tags
3. Forwards any extra arguments from context
4. Executes the command from `packages/ansible` directory

[VERIFIED via source - 2026-01-03]

**Exit Codes:**

- Returns ansible-playbook exit code on success
- Exit 1 if ansible-playbook command not found

[VERIFIED via source - 2026-01-03]

---

## src.commands.assets

Assets command group.

**Source:** [src/commands/assets/__init__.py:1](../../../src/commands/assets/__init__.py#L1)

### `assets_app: Typer`

Typer application for asset management commands.

```python
assets_app = Typer(help="Manage dotfiles assets")
```

[VERIFIED via source - 2026-01-03]

---

## src.commands.assets.wallpapers

Wallpaper management commands.

**Source:** [src/commands/assets/wallpapers/__init__.py:1](../../../src/commands/assets/wallpapers/__init__.py#L1)

### `wallpapers_app: Typer`

Typer application for wallpaper commands.

```python
wallpapers_app = typer.Typer(help="Manage wallpaper assets")
```

[VERIFIED via source - 2026-01-03]

### `get_default_archive_path()`

Get the default archive path relative to the package.

```python
def get_default_archive_path() -> Path
```

**Returns:** Path to `assets/wallpapers/wallpapers.tar.gz` relative to config root

**Algorithm:**
1. Gets package directory from `__file__`
2. Navigates up 4 levels to config root
3. Returns `config_root/assets/wallpapers/wallpapers.tar.gz`

[VERIFIED via source - 2026-01-03]

### `get_service()`

Create a WallpapersService with the default archive path.

```python
def get_service() -> WallpapersService
```

**Returns:** Configured WallpapersService instance

[VERIFIED via source - 2026-01-03]

### `add_wallpaper()`

Add a wallpaper to the archive.

```python
def add_wallpaper(
    path: Path = typer.Argument(..., help="Path to the wallpaper image to add", exists=True, readable=True),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite if wallpaper with same name exists"),
    no_validate: bool = typer.Option(False, "--no-validate", help="Skip image extension validation"),
) -> None
```

**Parameters:**

- `path` - Path to wallpaper image (must exist and be readable)
- `force` - If True, overwrite existing wallpaper with same name
- `no_validate` - If True, skip image extension validation

**Raises:**

- `typer.Exit(1)` on WallpaperError

[VERIFIED via source - 2026-01-03]

### `extract_wallpapers()`

Extract all wallpapers to the specified directory.

```python
def extract_wallpapers(
    path: Path = typer.Argument(..., help="Directory where wallpapers will be extracted (creates 'wallpapers' subdirectory)"),
) -> None
```

**Parameters:**

- `path` - Target directory (creates `wallpapers` subdirectory inside)

**Raises:**

- `typer.Exit(1)` on ArchiveNotFoundError

[VERIFIED via source - 2026-01-03]

### `list_wallpapers()`

List all wallpapers in the archive.

```python
def list_wallpapers() -> None
```

**Output:**

- If archive has wallpapers: Lists count and names (sorted alphabetically)
- If archive is empty: "No wallpapers in archive"

**Raises:**

- `typer.Exit(1)` on ArchiveNotFoundError

[VERIFIED via source - 2026-01-03]

## See Also

- [Services API](services.md) - WallpapersService implementation
- [CLI Reference](../cli/index.md) - Command-line usage
