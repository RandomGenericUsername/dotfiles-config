# Roles Organization

Structure and organization of Ansible roles in the dotfiles configuration.

## Role Directory Structure

```
packages/ansible/playbooks/roles/
├── base/                           - Foundation system components
│   └── zsh/                        - Zsh shell configuration
│       ├── defaults/
│       │   └── main.yml            - Default variables
│       ├── vars/
│       │   └── main.yml            - Distribution-specific mappings
│       └── tasks/
│           └── main.yml            - Installation and configuration tasks
├── features/                       - Optional features and enhancements
│   └── nvim/                       - Neovim editor configuration
│       ├── defaults/
│       │   └── main.yml
│       ├── vars/
│       │   └── main.yml
│       └── tasks/
│           └── main.yml
```

## Role Categories

### Base Roles

**Purpose:** Foundation system components that provide core functionality.

**Location:** `packages/ansible/playbooks/roles/base/`

**Current roles:**
- **[Zsh](../reference/roles/base/zsh.md)** - Shell configuration and setup
  - Installs zsh and related plugins
  - Configures distribution-specific paths
  - Renders customized .zshrc

**Characteristics:**
- Essential for system setup
- May be used as dependencies by other roles
- Include distribution-specific package and path mappings

### Feature Roles

**Purpose:** Optional features and enhanced functionality.

**Location:** `packages/ansible/playbooks/roles/features/`

**Current roles:**
- **Neovim** - Code editor and development environment

**Characteristics:**
- Optional functionality
- Can depend on base roles
- User explicitly chooses to install

## Role File Organization

Each role follows the standard Ansible role structure:

### `defaults/main.yml`

Contains default variables that can be overridden by the user.

**Includes:**
- Destination paths
- Template source paths
- Feature toggles
- Default configuration values

**Example:**
```yaml
zsh_config_dest: "{{ home_root }}/.zshrc"
zsh_use_distro_paths: true
PYENV_CONFIGURED: false
```

### `vars/main.yml`

Contains distribution-specific mappings and variable lists.

**Includes:**
- Package mappings per distribution
- Distribution-specific plugin paths
- System-specific configuration

**Example:**
```yaml
zsh_packages_map:
  Archlinux:
    - zsh
    - zsh-syntax-highlighting
  Debian:
    - zsh
    - zsh-syntax-highlighting
```

### `tasks/main.yml`

Contains Ansible tasks that perform the role's actions.

**Typical flow:**
1. Install system packages
2. Set distribution-specific variables
3. Render configuration templates
4. Create necessary directories
5. Set proper permissions

**Example:**
```yaml
- name: Install packages
  ansible.builtin.package:
    name: "{{ packages_for_distro }}"
    state: present

- name: Render configuration
  ansible.builtin.template:
    src: "{{ template_src }}"
    dest: "{{ config_dest }}"
```

## Distribution Support

Roles should support multiple distributions through:

1. **Package Mapping:** Different package names per distribution
2. **Path Mapping:** Different installation/config paths per distribution
3. **Conditional Tasks:** Tasks that only run on specific distributions

**Supported distributions:**
- Archlinux
- Debian
- Fedora

## Tag System

Each role is associated with tags for selective execution:

- Base roles: `[base_role_name, never]`
  - Example: `[zsh, never]`
- Feature roles: `[feature_name, never]`
  - Example: `[nvim, never]`

The `never` modifier prevents accidental execution - tags must be explicitly selected.

**Usage:**
```bash
# Run specific role
ansible-playbook playbooks/bootstrap.yml --tags zsh --ask-become-pass

# Run multiple roles
ansible-playbook playbooks/bootstrap.yml --tags zsh,nvim --ask-become-pass
```

See [Tags Reference](../reference/tags.md) for complete tag documentation.

## Bootstrap Playbook Integration

Roles are called from the bootstrap playbook:

```yaml
- name: Dotfiles engine (local)
  hosts: localhost
  gather_facts: true

  roles:
    - role: zsh
      tags: [zsh, never]
    - role: nvim
      tags: [nvim, never]
```

**Features:**
- Runs on localhost only
- Gathers Ansible facts for distribution detection
- Uses tags for selective execution
- Pre-tasks provide help and debug information

## Variable Precedence

Variables are resolved in this order (highest to lowest):

1. Command-line: `-e "VAR=value"`
2. Playbook variables: `playbooks/bootstrap.yml`
3. Role defaults: `defaults/main.yml`
4. Role vars: `vars/main.yml`
5. Distribution mappings
6. Ansible facts

This allows:
- Users to override everything via command-line
- Playbooks to set playbook-level defaults
- Roles to define sensible defaults
- Distribution-specific values to be applied automatically

## Adding a New Role

To add a new role, follow this checklist:

1. Create role directory: `packages/ansible/playbooks/roles/{category}/{role_name}/`
2. Create required directories:
   - `defaults/main.yml` - Define all user-overridable variables
   - `vars/main.yml` - Define distribution mappings
   - `tasks/main.yml` - Implement role logic
3. Add to `playbooks/bootstrap.yml`:
   - Add role call with appropriate tags
   - Update pre_tasks with help message
4. Document the role:
   - Create `docs/reference/roles/{category}/{role_name}.md`
   - Update `docs/reference/tags.md`
   - Update `docs/reference/roles/{category}/index.md`
5. Test on supported distributions

## See Also

- [Zsh Role Reference](../reference/roles/base/zsh.md)
- [Tags Reference](../reference/tags.md)
- [Bootstrap Playbook](../../packages/ansible/playbooks/bootstrap.yml)
