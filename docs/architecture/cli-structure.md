# CLI Structure

[VERIFIED via source - 2026-01-03]

How the command-line interface is organized using Typer.

## Application Hierarchy

```
app (Typer)                              [src/main.py]
├── install-packages (command)           [src/commands/install_packages.py]
├── dummy (command)                      [src/commands/dummy.py]
└── assets (Typer sub-app)              [src/commands/assets/__init__.py]
    └── wallpapers (Typer sub-app)      [src/commands/assets/wallpapers/__init__.py]
        ├── add (command)
        ├── list (command)
        └── extract (command)
```

[VERIFIED via source - 2026-01-03]

## Main Application

**File:** [src/main.py:7](../../src/main.py#L7)

```python
app = Typer(help="Dotfiles configuration management CLI")
```

The main app is the top-level Typer application that serves as the entry point for the `config` command.

[VERIFIED via source - 2026-01-03]

## Command Registration Patterns

### Pattern 1: Direct Command Registration

Used for standalone commands.

**Example:** `dummy` command

```python
# src/main.py
from src.commands.dummy import dummy

app.command(help="A dummy command that prints a message")(dummy)
```

[VERIFIED via source - 2026-01-03]

### Pattern 2: Command with Context and Options

Used for commands that need extra arguments or special context handling.

**Example:** `install-packages` command

```python
# src/main.py
from src.commands.install_packages import install_packages

app.command(
    "install-packages",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Install packages using Ansible playbook",
)(install_packages)
```

[VERIFIED via source - 2026-01-03]

**Context Settings:**
- `allow_extra_args: True` - Allows passing additional arguments not defined in function signature
- `ignore_unknown_options: True` - Doesn't raise errors for unknown flags

This enables forwarding arbitrary arguments to the underlying ansible-playbook command.

[VERIFIED via source - 2026-01-03]

### Pattern 3: Sub-Application (Command Groups)

Used for organizing related commands into groups.

**Example:** `assets` command group

```python
# src/main.py
from src.commands.assets import assets_app

app.add_typer(assets_app, name="assets")
```

```python
# src/commands/assets/__init__.py
from typer import Typer
from src.commands.assets.wallpapers import wallpapers_app

assets_app = Typer(help="Manage dotfiles assets")
assets_app.add_typer(wallpapers_app, name="wallpapers")
```

[VERIFIED via source - 2026-01-03]

## Command Implementation Patterns

### Basic Command

**Structure:**

```python
def command_name():
    """Command description."""
    typer.echo("Output")
```

**Example:** [src/commands/dummy.py:4](../../src/commands/dummy.py#L4)

[VERIFIED via source - 2026-01-03]

### Command with Arguments

**Structure:**

```python
def command_name(
    arg: Type = typer.Argument(..., help="Help text"),
):
    """Command description."""
    # Implementation
```

**Example:** [src/commands/assets/wallpapers/__init__.py:32](../../src/commands/assets/wallpapers/__init__.py#L32)

```python
def add_wallpaper(
    path: Path = typer.Argument(
        ...,
        help="Path to the wallpaper image to add",
        exists=True,
        readable=True,
    ),
    # ...
):
```

[VERIFIED via source - 2026-01-03]

### Command with Options

**Structure:**

```python
def command_name(
    option: Type = typer.Option(default, "--flag", "-f", help="Help text"),
):
    """Command description."""
    # Implementation
```

**Example:** [src/commands/assets/wallpapers/__init__.py:39](../../src/commands/assets/wallpapers/__init__.py#L39)

```python
def add_wallpaper(
    # ...
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite if wallpaper with same name exists",
    ),
):
```

[VERIFIED via source - 2026-01-03]

### Command with Context

**Structure:**

```python
def command_name(ctx: typer.Context, ...):
    """Command description."""
    extra_args = ctx.args  # Access forwarded arguments
```

**Example:** [src/commands/install_packages.py:9](../../src/commands/install_packages.py#L9)

```python
def install_packages(
    ctx: typer.Context,
    tags: Optional[List[str]] = typer.Option(None, "--tags", help="Ansible tags to run"),
):
    # ...
    if ctx.args:
        cmd.extend(ctx.args)
```

[VERIFIED via source - 2026-01-03]

## Error Handling in Commands

Commands use `typer.Exit(code)` to exit with specific error codes.

**Pattern:**

```python
try:
    # Operation
except SomeError as e:
    typer.echo(f"Error: {e}", err=True)
    raise typer.Exit(1)
```

**Example:** [src/commands/assets/wallpapers/__init__.py:60](../../src/commands/assets/wallpapers/__init__.py#L60)

```python
def add_wallpaper(...):
    service = get_service()
    try:
        service.add_wallpaper(...)
        typer.echo(f"Successfully added '{path.name}' to wallpapers archive")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
```

[VERIFIED via source - 2026-01-03]

## Service Layer Integration

Commands delegate business logic to service classes.

**Pattern:**

```python
# Command layer (CLI)
def command():
    service = get_service()
    result = service.do_operation()
    typer.echo(result)

# Service layer (business logic)
class Service:
    def do_operation(self):
        # Implementation
        return result
```

**Example:**

- Command: [src/commands/assets/wallpapers/__init__.py:83](../../src/commands/assets/wallpapers/__init__.py#L83)
- Service: [src/commands/assets/wallpapers/service.py:71](../../src/commands/assets/wallpapers/service.py#L71)

[VERIFIED via source - 2026-01-03]

## Helper Functions

Commands can use helper functions for common setup tasks.

**Example:** `get_service()` and `get_default_archive_path()`

```python
def get_default_archive_path() -> Path:
    """Get the default archive path relative to this package."""
    package_dir = Path(__file__).parent
    config_root = package_dir.parent.parent.parent.parent
    return config_root / "assets" / "wallpapers" / "wallpapers.tar.gz"

def get_service() -> WallpapersService:
    """Create a WallpapersService with the default archive path."""
    return WallpapersService(get_default_archive_path())
```

[VERIFIED via source - 2026-01-03]

## Entry Point

The CLI is registered as a console script in pyproject.toml:

```toml
[project.scripts]
config = "src.main:main"
```

[VERIFIED via source - 2026-01-03]

The entry point function:

```python
def main():
    app()
```

[VERIFIED via source - 2026-01-03]

## Shell Completion

Typer provides automatic shell completion support:

```bash
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

## See Also

- [CLI Reference](../reference/cli/index.md)
- [Python API: Commands](../reference/python-api/commands.md)
- [Design Principles](design-principles.md)
