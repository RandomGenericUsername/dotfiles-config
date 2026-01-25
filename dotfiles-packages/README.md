# dotfiles-packages

Package and role management system for dotfiles configuration using Ansible.

## Overview

`dotfiles-packages` provides a command-line interface and Python API for managing Ansible playbooks and roles. It allows you to:

- **List** available roles and tags from your Ansible playbooks
- **Install** roles with specific tags using Ansible
- **Parse** YAML playbooks for role discovery

## Installation

### From source

```bash
cd dotfiles-packages
uv sync
```

### As a dependency

Add to your project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "dotfiles-packages @ file://path/to/dotfiles-packages",
]
```

## Usage

### Command Line Interface

#### List available roles

```bash
dotfiles-packages list
```

Output:
```
Available roles:
  role-1
  role-2
    Tags: tag-a, tag-b
```

#### Install roles with tags

```bash
dotfiles-packages install --tags core
dotfiles-packages install --tags core --tags optional
```

Pass additional arguments to Ansible:

```bash
dotfiles-packages install --tags core -- --check --diff
```

### Python API

```python
from dotfiles_packages import Packages

packages = Packages()

# List all roles
roles = packages.list_packages()
for role in roles:
    print(f"{role.name}: {role.tags}")

# Install roles with tags
installed = packages.install(tags=["core"])
print(f"Installed: {installed}")

# Use custom playbook path
packages = Packages(playbook_path="/path/to/playbook.yml")
```

## Architecture

### Layered Design

```
CLI Layer          → packages list, packages install
    ↓
API Layer          → Packages class (public interface)
    ↓
Service Layer      → PackagesService (business logic)
```

### Error Handling

The module provides specific exception types:

- **`PackagesError`**: Base exception for all package-related errors
- **`PlaybookNotFoundError`**: Playbook file not found at specified path
- **`AnsibleError`**: Ansible command failed (includes return code)
- **`AnsibleNotFoundError`**: Ansible executable not found

Example:

```python
from dotfiles_packages import Packages, AnsibleError, PlaybookNotFoundError

try:
    packages = Packages(playbook_path="/nonexistent/playbook.yml")
    packages.install(tags=["core"])
except PlaybookNotFoundError as e:
    print(f"Playbook not found: {e}")
except AnsibleError as e:
    print(f"Ansible failed with code {e.return_code}: {e}")
```

## Configuration

### Playbook Path

Set the Ansible playbook path via:

1. **API constructor parameter**:
   ```python
   Packages(playbook_path="/path/to/playbook.yml")
   ```

2. **Environment variable** (if implemented):
   ```bash
   export DOTFILES_PLAYBOOK=/path/to/playbook.yml
   ```

3. **Default location**: `$HOME/.config/dotfiles/playbook.yml`

### Tag Filtering

Roles are discovered from Ansible playbooks and filtered by tags:

```yaml
# playbook.yml
- hosts: localhost
  roles:
    - role: core-role
      tags: [core, essential]
    - role: optional-role
      tags: [optional]
```

## Testing

Run the test suite:

```bash
uv sync
uv run pytest tests/
```

Test coverage:

- **Unit tests**: Service layer, API delegation, data models
- **Integration tests**: CLI commands, Ansible integration
- **Mocking**: Ansible calls use mocks to avoid actual installations

## Development

### Project Structure

```
dotfiles-packages/
├── src/
│   └── dotfiles_packages/
│       ├── __init__.py           # Public API exports
│       ├── api/
│       │   └── packages.py        # Packages class
│       ├── cli/
│       │   └── commands/
│       │       ├── list.py        # List command
│       │       └── install.py     # Install command
│       ├── services/
│       │   └── packages_service.py # Business logic
│       └── exceptions.py          # Error types
├── tests/
│   ├── unit/
│   │   ├── test_packages_service.py
│   │   └── test_packages_api.py
│   └── integration/
│       └── test_packages_cli.py
└── pyproject.toml
```

### Adding New Roles

Add roles to your Ansible playbook with appropriate tags:

```yaml
- hosts: localhost
  roles:
    - role: my-new-role
      tags: [my-category, core]
```

The role will automatically appear in `list` output and can be installed via tags.

## Dependencies

- **Python**: 3.12+
- **pyaml**: YAML parsing for playbooks
- **typer**: CLI framework
- **ansible**: Role installation (runtime dependency)

## License

MIT
