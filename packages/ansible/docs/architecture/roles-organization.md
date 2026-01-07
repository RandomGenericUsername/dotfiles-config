# Roles Organization

This document explains how roles are organized in the ansible package.

## Role Categories

Roles are organized into two main categories under `playbooks/roles/`:

### Base Roles (`playbooks/roles/base/`)

[EMPTY DIRECTORY] Reserved for fundamental system configuration roles that provide base functionality.

Currently, no base roles have been implemented.

### Feature Roles (`playbooks/roles/features/`)

[VERIFIED] Contains feature-specific roles for installing and configuring software packages.

Currently implemented roles:
- **nvim**: Neovim text editor installation and configuration

## Standard Role Structure

[VERIFIED] Each role follows the standard Ansible role directory structure:

```text
role_name/
├── defaults/
│   └── main.yml      # Default variables (lowest precedence)
├── vars/
│   └── main.yml      # Role-specific variables (higher precedence)
└── tasks/
    └── main.yml      # Tasks to execute
```

### `defaults/main.yml`

Contains default variable values that can be easily overridden. These have the lowest precedence in Ansible's variable system.

**Example from nvim role**:
```yaml
nvim_config_dest: "{{ xdg_config_home }}/nvim"
nvim_config_src_dir: "{{ config_files_root }}/nvim"
```

### `vars/main.yml`

Contains role-specific variables with higher precedence. Typically used for:
- Distribution-specific package mappings
- Constants that shouldn't be easily overridden

**Example from nvim role**:
```yaml
nvim_packages_map:
  Debian: [neovim]
  Fedora: [neovim]
  Archlinux: [neovim]
```

### `tasks/main.yml`

Contains the actual tasks that the role executes. Tasks are executed in order from top to bottom.

[VERIFIED] The nvim role includes three tasks:
1. Install neovim
2. Ensure destination directory exists
3. Copy Neovim config directory

## Role Invocation

[VERIFIED] Roles are invoked in the `playbooks/bootstrap.yml` playbook:

```yaml
roles:
  - role: nvim
    tags: [nvim]
```

Each role is associated with tags for selective execution. See [Tags Reference](../reference/tags.md) for details.

## Role Paths Configuration

[VERIFIED] The `ansible.cfg` file defines where Ansible looks for roles:

```ini
roles_path = ./playbooks/roles/base:./playbooks/roles/features
```

This allows Ansible to find roles in both the `base/` and `features/` directories without requiring the full path in the playbook.

## Adding New Roles

When adding a new role:

1. Determine if it belongs in `base/` or `features/`
2. Create the role directory structure
3. Define variables in `defaults/main.yml`
4. Define distribution mappings in `vars/main.yml` (if needed)
5. Implement tasks in `tasks/main.yml`
6. Add the role to `playbooks/bootstrap.yml` with appropriate tags

See the [Adding a Role Guide](../guides/adding-a-role.md) for detailed instructions.
