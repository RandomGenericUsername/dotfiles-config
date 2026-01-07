# Variable System

This document explains how variables are organized, their precedence, and how they can be overridden.

## Variable Precedence

Ansible follows a specific precedence order for variables (from lowest to highest priority):

1. Role defaults (`roles/*/defaults/main.yml`)
2. Inventory variables (`inventory/group_vars/all.yml`)
3. Role variables (`roles/*/vars/main.yml`)
4. Extra variables (via `-e` flag at runtime)

This means variables can be overridden by external installers using the `-e` flag when invoking `ansible-playbook`.

## Global Variables

[VERIFIED] Defined in `inventory/group_vars/all.yml`:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `dotfiles_root` | `{{ playbook_dir }}/../../..` | Root directory of the dotfiles repository |
| `assets_root` | `{{ dotfiles_root }}/assets` | Directory containing asset files |
| `config_files_root` | `{{ dotfiles_root }}/config-files` | Directory containing configuration files |
| `home_root` | `{{ ansible_facts['env']['HOME'] }}` | User's home directory |
| `xdg_config_home` | `{{ ansible_facts['env'].get('XDG_CONFIG_HOME', home_root + '/.config') }}` | XDG config directory (defaults to `~/.config`) |
| `xdg_data_home` | `{{ ansible_facts['env'].get('XDG_DATA_HOME', home_root + '/.local/share') }}` | XDG data directory (defaults to `~/.local/share`) |
| `xdg_bin_home` | `{{ home_root }}/.local/bin` | XDG binary directory |

## Role Variables

Each role can define its own variables in two locations:

### Role Defaults (`defaults/main.yml`)

[VERIFIED] The nvim role defines:

| Variable | Default Value | Source File |
|----------|---------------|-------------|
| `nvim_config_dest` | `{{ xdg_config_home }}/nvim` | `playbooks/roles/features/nvim/defaults/main.yml` |
| `nvim_config_src_dir` | `{{ config_files_root }}/nvim` | `playbooks/roles/features/nvim/defaults/main.yml` |

These have the lowest precedence and can be easily overridden.

### Role Vars (`vars/main.yml`)

[VERIFIED] The nvim role defines:

| Variable | Value | Source File |
|----------|-------|-------------|
| `nvim_packages_map` | See distribution mapping | `playbooks/roles/features/nvim/vars/main.yml` |

These have higher precedence than defaults and inventory variables.

## Variable Override Mechanism

External installers can override any variable using the `-e` (extra vars) flag:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/path \
  -e nvim_config_dest=/custom/nvim/location
```

This mechanism allows the dotfiles configuration system to be flexible and adapt to different installation environments.

## Variable Interpolation

[VERIFIED] Variables support Jinja2 template interpolation:

- Variables can reference other variables (e.g., `{{ dotfiles_root }}/assets`)
- Ansible facts can be accessed (e.g., `{{ ansible_facts['env']['HOME'] }}`)
- Conditional defaults using `get()` method (e.g., `{{ ansible_facts['env'].get('XDG_CONFIG_HOME', ...) }}`)

## Best Practices

1. **Override at runtime**: Use `-e` flags for environment-specific values
2. **Default paths**: Global variables provide sensible defaults based on XDG specifications
3. **Fact gathering**: The playbook sets `gather_facts: true` to enable fact-based variables
