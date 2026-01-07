# Variables Reference

This document provides a complete reference of all variables used in the ansible package.

## Global Variables

[VERIFIED] Defined in `inventory/group_vars/all.yml`:

| Variable | Default | Description | Source File |
|----------|---------|-------------|-------------|
| `dotfiles_root` | `{{ playbook_dir }}/../../..` | Root directory of the dotfiles repository | `inventory/group_vars/all.yml` |
| `assets_root` | `{{ dotfiles_root }}/assets` | Directory containing asset files | `inventory/group_vars/all.yml` |
| `config_files_root` | `{{ dotfiles_root }}/config-files` | Directory containing configuration files to be copied | `inventory/group_vars/all.yml` |
| `home_root` | `{{ ansible_facts['env']['HOME'] }}` | User's home directory from environment | `inventory/group_vars/all.yml` |
| `xdg_config_home` | `{{ ansible_facts['env'].get('XDG_CONFIG_HOME', home_root + '/.config') }}` | XDG config directory (defaults to `~/.config` if not set) | `inventory/group_vars/all.yml` |
| `xdg_data_home` | `{{ ansible_facts['env'].get('XDG_DATA_HOME', home_root + '/.local/share') }}` | XDG data directory (defaults to `~/.local/share` if not set) | `inventory/group_vars/all.yml` |
| `xdg_bin_home` | `{{ home_root }}/.local/bin` | XDG binary directory | `inventory/group_vars/all.yml` |

## Role-Specific Variables

### Neovim Role

#### Defaults

[VERIFIED] Defined in `playbooks/roles/features/nvim/defaults/main.yml`:

| Variable | Default | Description | Source File |
|----------|---------|-------------|-------------|
| `nvim_config_dest` | `{{ xdg_config_home }}/nvim` | Destination directory for Neovim configuration | `playbooks/roles/features/nvim/defaults/main.yml` |
| `nvim_config_src_dir` | `{{ config_files_root }}/nvim` | Source directory containing Neovim configuration files | `playbooks/roles/features/nvim/defaults/main.yml` |

#### Variables

[VERIFIED] Defined in `playbooks/roles/features/nvim/vars/main.yml`:

| Variable | Value | Description | Source File |
|----------|-------|-------------|-------------|
| `nvim_packages_map` | Dictionary mapping distributions to package names | Maps Linux distribution names to their respective Neovim package names | `playbooks/roles/features/nvim/vars/main.yml` |

**Package Mappings**:

| Distribution | Package Names |
|--------------|---------------|
| Debian | `neovim` |
| Fedora | `neovim` |
| Archlinux | `neovim` |

## Variable Usage

### Overriding Variables

Variables can be overridden at runtime using the `-e` flag:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/dotfiles/path \
  -e nvim_config_dest=/tmp/nvim-config
```

### Variable Interpolation

Variables support Jinja2 template syntax:
- Reference other variables: `{{ dotfiles_root }}/assets`
- Access Ansible facts: `{{ ansible_facts['env']['HOME'] }}`
- Conditional defaults: `{{ ansible_facts['env'].get('XDG_CONFIG_HOME', default_value) }}`

### Variable Precedence

From lowest to highest priority:
1. Role defaults (`defaults/main.yml`)
2. Inventory group variables (`group_vars/all.yml`)
3. Role variables (`vars/main.yml`)
4. Extra variables (`-e` flag)

See [Variable System](../architecture/variable-system.md) for detailed information on variable precedence.
