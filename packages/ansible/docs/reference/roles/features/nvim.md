# Neovim Role

The nvim role installs Neovim and copies its configuration files to the appropriate location.

## Tag

[VERIFIED] `nvim`

## Tasks Performed

[VERIFIED] The role executes the following tasks (from `playbooks/roles/features/nvim/tasks/main.yml`):

1. **Install neovim**: Installs the Neovim package using the system package manager
2. **Ensure destination directory exists**: Creates the configuration directory if it doesn't exist
3. **Copy Neovim config directory**: Copies configuration files from the source to the destination

## Variables

### Defaults

[VERIFIED] Defined in `playbooks/roles/features/nvim/defaults/main.yml`:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `nvim_config_dest` | `{{ xdg_config_home }}/nvim` | Destination directory for Neovim configuration |
| `nvim_config_src_dir` | `{{ config_files_root }}/nvim` | Source directory containing Neovim configuration files |

### Role Variables

[VERIFIED] Defined in `playbooks/roles/features/nvim/vars/main.yml`:

| Variable | Description |
|----------|-------------|
| `nvim_packages_map` | Dictionary mapping Linux distributions to Neovim package names |

## Package Mappings

[VERIFIED] Distribution-specific package names:

| Distribution | Package Name(s) |
|--------------|-----------------|
| Debian | `neovim` |
| Fedora | `neovim` |
| Archlinux | `neovim` |

## Usage

### Basic Installation

Install Neovim with default settings:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

The `--ask-become-pass` flag is required because package installation needs root privileges.

### Custom Destination

Override the configuration destination:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass \
  -e nvim_config_dest=/custom/nvim/path
```

### Custom Source Directory

Override the source configuration directory:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass \
  -e nvim_config_src_dir=/custom/source/nvim
```

## Requirements

- Root/sudo privileges for package installation
- Source configuration files must exist at `{{ config_files_root }}/nvim` (or custom path)
- Supported Linux distribution (Debian, Fedora, or Archlinux)

## Task Details

### Task 1: Install neovim

```yaml
- name: Install neovim
  become: true
  ansible.builtin.package:
    name: "{{ nvim_packages_map.get(ansible_facts['distribution'], []) }}"
    state: present
```

Uses `become: true` to gain root privileges and installs the distribution-appropriate package.

### Task 2: Ensure destination directory exists

```yaml
- name: Ensure destination directory exists
  ansible.builtin.file:
    path: "{{ neovim_config_dest }}"
    state: directory
    mode: "0755"
```

Creates the configuration directory with appropriate permissions.

### Task 3: Copy Neovim config directory

```yaml
- name: Copy Neovim config directory
  ansible.builtin.copy:
    src: "{{ neovim_config_src_dir }}/"
    dest: "{{ neovim_config_dest }}/"
    mode: preserve
```

Copies all configuration files from source to destination, preserving file modes.

## See Also

- [Variables Reference](../../variables.md): Global variables documentation
- [Distribution Support](../../distributions.md): Supported distributions
- [Tags Reference](../../tags.md): All available tags
