# Integration Points

[VERIFIED via source - 2026-01-03]

How different components interact with each other and with external systems.

## System Integration Overview

```
┌────────────────────────────────────────────────────┐
│              User Interface Layer                   │
│                                                     │
│  ┌──────────────┐         ┌──────────────┐        │
│  │  config CLI  │────────▶│    Shell     │        │
│  │   (Typer)    │◀────────│  Completion  │        │
│  └──────────────┘         └──────────────┘        │
└────────────────────────────────────────────────────┘
         │                              │
         │ [1] Subprocess call          │ [2] Python API
         ▼                              ▼
┌──────────────────┐         ┌─────────────────────┐
│     Ansible      │         │  Service Layer      │
│   ansible-       │         │                     │
│   playbook       │         │  WallpapersService  │
└──────────────────┘         └─────────────────────┘
         │                              │
         │                              │
         ▼                              ▼
┌──────────────────┐         ┌─────────────────────┐
│  System Level    │         │   File System       │
│                  │         │                     │
│  Package Manager │         │  tar.gz Archives    │
│  Config Files    │         │  Image Files        │
└──────────────────┘         └─────────────────────┘
```

[VERIFIED via source - 2026-01-03]

## Integration Point 1: CLI → Ansible

### Description

The `config install-packages` command integrates with Ansible to install system packages and deploy configuration files.

[VERIFIED via source - 2026-01-03]

### Implementation

**File:** [src/commands/install_packages.py:39](../../src/commands/install_packages.py#L39)

```python
result = subprocess.run(
    cmd,
    cwd=ansible_dir,
    check=True,
)
```

[VERIFIED via source - 2026-01-03]

### Data Flow

1. User runs `config install-packages --tags nvim`
2. Command builds ansible-playbook command:
   ```bash
   ansible-playbook playbooks/bootstrap.yml --tags nvim
   ```
3. subprocess.run() executes command from `packages/ansible/` directory
4. Ansible playbook runs with specified tags
5. Exit code returned to user

[VERIFIED via source - 2026-01-03]

### Argument Forwarding

Extra CLI arguments are forwarded to ansible-playbook:

```python
# Context settings enable forwarding
context_settings={"allow_extra_args": True, "ignore_unknown_options": True}

# Extra arguments added to command
if ctx.args:
    cmd.extend(ctx.args)
```

[VERIFIED via source - 2026-01-03]

**Example:**

```bash
config install-packages --tags nvim --ask-become-pass -v
```

Becomes:

```bash
ansible-playbook playbooks/bootstrap.yml --tags nvim --ask-become-pass -v
```

[VERIFIED via CLI - 2026-01-03]

### Working Directory

Ansible commands execute from `packages/ansible/` directory to ensure proper relative path resolution for:
- Playbook paths
- Inventory paths
- Role paths

[VERIFIED via source - 2026-01-03]

## Integration Point 2: Ansible → Configuration Files

### Description

Ansible deploys configuration files from `config-files/` to user's system.

[VERIFIED via source - 2026-01-03]

### Implementation

**Playbook:** [packages/ansible/playbooks/bootstrap.yml:15](../../packages/ansible/playbooks/bootstrap.yml#L15)

```yaml
roles:
  - role: nvim
    tags: [nvim]
```

**Role tasks:** `packages/ansible/playbooks/roles/features/nvim/tasks/main.yml`

[VERIFIED via source - 2026-01-03]

### Data Flow

1. Ansible role executes
2. Installs neovim package via system package manager
3. Copies files from `{{ config_files_root }}/nvim` to `{{ xdg_config_home }}/nvim`

[VERIFIED via CLI - 2026-01-03]

### Variable Resolution

**Global variables** (`packages/ansible/inventory/group_vars/all.yml`):

```yaml
dotfiles_root: "{{ playbook_dir }}/../../.."
config_files_root: "{{ dotfiles_root }}/config-files"
xdg_config_home: "{{ ansible_facts['env'].get('XDG_CONFIG_HOME', home_root + '/.config') }}"
```

[VERIFIED via source - 2026-01-03]

**Role variables** (`packages/ansible/playbooks/roles/features/nvim/vars/main.yml`):

- `nvim_config_source: "{{ config_files_root }}/nvim"`

**Role defaults** (`packages/ansible/playbooks/roles/features/nvim/defaults/main.yml`):

- `nvim_config_dest: "{{ xdg_config_home }}/nvim"`

[VERIFIED via source - 2026-01-03]

### XDG Base Directory Compliance

The system follows XDG Base Directory Specification:
- `XDG_CONFIG_HOME` - User configuration files (default: `~/.config`)
- `XDG_DATA_HOME` - User data files (default: `~/.local/share`)
- `XDG_BIN_HOME` - User binaries (default: `~/.local/bin`)

[VERIFIED via source - 2026-01-03]

## Integration Point 3: CLI → WallpapersService

### Description

Wallpaper CLI commands delegate business logic to `WallpapersService`.

[VERIFIED via source - 2026-01-03]

### Implementation

**Command layer** [src/commands/assets/wallpapers/__init__.py:52](../../src/commands/assets/wallpapers/__init__.py#L52):

```python
def add_wallpaper(...):
    service = get_service()
    try:
        service.add_wallpaper(path, overwrite=force, validate_extension=not no_validate)
        typer.echo(f"Successfully added '{path.name}' to wallpapers archive")
    except WallpaperError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
```

[VERIFIED via source - 2026-01-03]

**Service layer** [src/commands/assets/wallpapers/service.py:90](../../src/commands/assets/wallpapers/service.py#L90):

```python
def add_wallpaper(self, wallpaper_path: Path, overwrite: bool = True, validate_extension: bool = True) -> None:
    # Business logic implementation
```

[VERIFIED via source - 2026-01-03]

### Responsibilities

**Command layer:**
- Argument parsing and validation
- User output formatting
- Error display
- Exit code management

**Service layer:**
- Archive operations
- File validation
- Error raising
- Business logic

[VERIFIED via source - 2026-01-03]

### Error Flow

1. Service raises domain-specific exception (e.g., `WallpaperNotFoundError`)
2. Command catches exception
3. Command formats error message for user
4. Command exits with code 1

[VERIFIED via source - 2026-01-03]

## Integration Point 4: Service → File System

### Description

WallpapersService interacts with tar.gz archives and image files.

[VERIFIED via source - 2026-01-03]

### Implementation

Uses Python standard library modules:
- `tarfile` - Archive operations
- `pathlib.Path` - File path manipulation
- `shutil` - File copying
- `tempfile` - Temporary directory management

[VERIFIED via source - 2026-01-03]

### Archive Operations

**Read archive:**

```python
with tarfile.open(self.archive_path, "r:gz") as tar:
    members = tar.getmembers()
```

[VERIFIED via source - 2026-01-03]

**Write archive:**

```python
with tarfile.open(self.archive_path, "w:gz") as tar:
    for file_path in tmp_path.iterdir():
        tar.add(file_path, arcname=file_path.name)
```

[VERIFIED via source - 2026-01-03]

### Atomic Updates

Add operation uses atomic update pattern:

1. Create temporary directory
2. Extract existing archive to temp
3. Add/update files in temp
4. Create new archive from temp
5. Temp directory auto-deleted on exit

This ensures archive is never in a partial state.

[VERIFIED via source - 2026-01-03]

## Integration Point 5: Python Package → System

### Description

The project is installed as a Python package with console script entry point.

[VERIFIED via source - 2026-01-03]

### Implementation

**pyproject.toml:**

```toml
[project.scripts]
config = "src.main:main"
```

[VERIFIED via source - 2026-01-03]

### Installation

```bash
uv pip install -e .
```

This creates a `config` executable in the virtual environment's bin directory that calls `src.main:main()`.

[VERIFIED via source - 2026-01-03]

### Entry Point

```python
# src/main.py
def main():
    app()

if __name__ == "__main__":
    main()
```

[VERIFIED via source - 2026-01-03]

## Integration Point 6: Test Framework → Code

### Description

pytest integrates with source code for testing.

[VERIFIED via tests - 2026-01-03]

### Configuration

**pyproject.toml:**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

[VERIFIED via source - 2026-01-03]

### Test Discovery

pytest discovers tests by:
- Searching `tests/` directory
- Finding files matching `test_*.py`
- Collecting functions/classes matching `test_*` or `Test*`

[VERIFIED via tests - 2026-01-03]

### Fixture System

Shared fixtures in `tests/conftest.py` are automatically available to all tests.

[VERIFIED via source - 2026-01-03]

## External Dependencies

### Required

- **Python 3.12+** - Runtime
- **Typer** - CLI framework
- **Ansible 2.20+** - Configuration management

[VERIFIED via source - 2026-01-03]

### Optional (Development)

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **uv** - Package manager

[VERIFIED via source - 2026-01-03]

## See Also

- [CLI Structure](cli-structure.md)
- [Design Principles](design-principles.md)
- [Development Guide](../guides/development/index.md)
