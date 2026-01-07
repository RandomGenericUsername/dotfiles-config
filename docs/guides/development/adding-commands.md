# Adding Commands

[VERIFIED via source - 2026-01-03]

How to add new CLI commands to the dotfiles-config system.

## Overview

Adding a command involves:
1. Create command implementation
2. Register command with app
3. Add service layer (if needed)
4. Write tests
5. Update documentation

## Quick Example

Adding a simple command `config hello`:

```python
# src/commands/hello.py
import typer

def hello(name: str = typer.Argument(..., help="Name to greet")):
    """Greet someone."""
    typer.echo(f"Hello, {name}!")
```

```python
# src/main.py
from src.commands.hello import hello

app.command(help="Greet someone")(hello)
```

[VERIFIED via source - 2026-01-03]

## Step-by-Step Guide

### Step 1: Create Command File

Create a new file in `src/commands/`:

```python
# src/commands/mycommand.py
import typer
from pathlib import Path
from typing import Optional

def mycommand(
    arg: str = typer.Argument(..., help="Description"),
    option: bool = typer.Option(False, "--flag", "-f", help="Optional flag"),
) -> None:
    """
    Command description.

    This command does something useful.
    """
    # Implementation
    typer.echo(f"Running mycommand with {arg}")
```

[VERIFIED via source - 2026-01-03]

### Step 2: Register Command

Add to `src/main.py`:

```python
from src.commands.mycommand import mycommand

app.command(help="Command description")(mycommand)
```

[VERIFIED via source - 2026-01-03]

### Step 3: Test Manually

```bash
config mycommand --help
config mycommand test-value
```

## Adding a Command Group

For related commands, create a command group.

### Step 1: Create Package

```bash
mkdir -p src/commands/mygroup
touch src/commands/mygroup/__init__.py
```

### Step 2: Create Group App

```python
# src/commands/mygroup/__init__.py
from typer import Typer

mygroup_app = Typer(help="Manage mygroup resources")

@mygroup_app.command("list")
def list_items() -> None:
    """List items."""
    typer.echo("Listing items...")

@mygroup_app.command("add")
def add_item(name: str = typer.Argument(...)):
    """Add an item."""
    typer.echo(f"Adding {name}")
```

[VERIFIED via source - 2026-01-03]

### Step 3: Register Group

```python
# src/main.py
from src.commands.mygroup import mygroup_app

app.add_typer(mygroup_app, name="mygroup")
```

[VERIFIED via source - 2026-01-03]

### Usage

```bash
config mygroup list
config mygroup add item-name
```

## Adding Service Layer

For complex business logic, create a service class.

### Step 1: Create Service File

```python
# src/commands/mygroup/service.py
from pathlib import Path
from typing import List

class MyServiceError(Exception):
    """Base exception for myservice operations."""
    pass

class MyService:
    """Service for managing resources."""

    def __init__(self, data_path: Path) -> None:
        """Initialize the service.

        Args:
            data_path: Path to data file
        """
        self.data_path = data_path

    def list_items(self) -> List[str]:
        """List all items.

        Returns:
            List of item names

        Raises:
            MyServiceError: If data file doesn't exist
        """
        if not self.data_path.exists():
            raise MyServiceError(f"Data file not found: {self.data_path}")

        # Implementation
        return []

    def add_item(self, name: str) -> None:
        """Add an item.

        Args:
            name: Item name

        Raises:
            MyServiceError: If item already exists
        """
        # Implementation
        pass
```

[VERIFIED via source - 2026-01-03]

### Step 2: Use Service in Commands

```python
# src/commands/mygroup/__init__.py
from typer import Typer
from src.commands.mygroup.service import MyService, MyServiceError

mygroup_app = Typer(help="Manage mygroup resources")

def get_service() -> MyService:
    """Create service instance."""
    return MyService(Path("data.json"))

@mygroup_app.command("list")
def list_items() -> None:
    """List items."""
    service = get_service()
    try:
        items = service.list_items()
        for item in items:
            typer.echo(f"  - {item}")
    except MyServiceError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
```

[VERIFIED via source - 2026-01-03]

## Adding Tests

### Unit Tests

Test service layer in `tests/unit/`:

```python
# tests/unit/test_myservice.py
import pytest
from pathlib import Path
from src.commands.mygroup.service import MyService, MyServiceError

class TestMyService:
    """Tests for MyService."""

    def test_list_items_success(self, temp_dir: Path):
        """List items successfully."""
        data_path = temp_dir / "data.json"
        data_path.write_text("[]")

        service = MyService(data_path)
        items = service.list_items()

        assert isinstance(items, list)

    def test_list_items_missing_file_raises(self, temp_dir: Path):
        """List raises error if file missing."""
        data_path = temp_dir / "nonexistent.json"

        service = MyService(data_path)

        with pytest.raises(MyServiceError):
            service.list_items()
```

[VERIFIED via tests - 2026-01-03]

### Integration Tests

Test CLI commands in `tests/integration/`:

```python
# tests/integration/test_mygroup_cli.py
import subprocess

class TestMyGroupListCommand:
    """Tests for 'config mygroup list' command."""

    def test_list_shows_in_help(self):
        """List command appears in help."""
        result = subprocess.run(
            ["uv", "run", "config", "mygroup", "--help"],
            capture_output=True,
            text=True,
        )
        assert "list" in result.stdout

    def test_list_command_works(self):
        """List command executes successfully."""
        result = subprocess.run(
            ["uv", "run", "config", "mygroup", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
```

[VERIFIED via tests - 2026-01-03]

### Run Tests

```bash
make test-cov
```

Ensure all tests pass and coverage is high.

## Command Patterns

### Pattern: Argument

Required positional argument:

```python
def command(
    path: Path = typer.Argument(..., help="Path to file", exists=True),
):
```

[VERIFIED via source - 2026-01-03]

### Pattern: Option with Flag

Optional boolean flag:

```python
def command(
    force: bool = typer.Option(False, "--force", "-f", help="Force operation"),
):
```

[VERIFIED via source - 2026-01-03]

### Pattern: Option with Value

Optional value with default:

```python
def command(
    output: Path = typer.Option(Path("."), "--output", "-o", help="Output directory"),
):
```

[VERIFIED via source - 2026-01-03]

### Pattern: List Option

Multiple values:

```python
def command(
    tags: Optional[List[str]] = typer.Option(None, "--tags", help="Tags to run"),
):
    if tags:
        tag_str = ",".join(tags)
```

[VERIFIED via source - 2026-01-03]

### Pattern: Context for Extra Args

Forward unknown arguments:

```python
def command(
    ctx: typer.Context,
):
    extra_args = ctx.args
    # Forward to another command
```

[VERIFIED via source - 2026-01-03]

Register with context settings:

```python
app.command(
    "mycommand",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)(command)
```

[VERIFIED via source - 2026-01-03]

## Error Handling

### Raise Exit Code

```python
def command():
    try:
        # Operation
        service.do_something()
        typer.echo("Success")
    except ServiceError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
```

[VERIFIED via source - 2026-01-03]

### Domain-Specific Exceptions

```python
class MyCommandError(Exception):
    """Base exception."""
    pass

class NotFoundError(MyCommandError):
    """Resource not found."""
    pass

class ValidationError(MyCommandError):
    """Invalid input."""
    pass
```

[VERIFIED via source - 2026-01-03]

## Documentation

### Docstrings

All functions must have docstrings:

```python
def command(arg: str, option: bool = False) -> None:
    """
    One-line summary.

    Longer description if needed.

    Args:
        arg: Description of argument
        option: Description of option

    Raises:
        CommandError: When error occurs

    Examples:
        $ config mycommand value
        $ config mycommand value --option
    """
```

[VERIFIED via source - 2026-01-03]

### CLI Documentation

Add to `docs/reference/cli/`:

```markdown
# mycommand

[VERIFIED via CLI - 2026-01-03]

Description of the command.

## Synopsis

\`\`\`bash
config mycommand [OPTIONS] ARG
\`\`\`

## Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `ARG` | String (required) | Description |

## Options

| Option | Description |
|--------|-------------|
| `--option`, `-o` | Enable option |
| `--help` | Show help |

## Examples

\`\`\`bash
config mycommand value
\`\`\`

[VERIFIED via CLI - 2026-01-03]

## Source Code

Implementation: [src/commands/mycommand.py](../../src/commands/mycommand.py)
```

## Checklist

Before submitting:

- [ ] Command implementation complete
- [ ] Command registered in main.py
- [ ] Service layer added (if needed)
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Coverage >80% for new code
- [ ] Docstrings complete
- [ ] CLI documentation added
- [ ] Manual testing done
- [ ] Help output verified

## See Also

- [CLI Structure](../../architecture/cli-structure.md)
- [Testing Guide](testing.md)
- [Design Principles](../../architecture/design-principles.md)
- [CLI Reference](../../reference/cli/index.md)
