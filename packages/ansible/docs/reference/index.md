# Reference Documentation

This section contains complete reference documentation for the ansible package.

## Contents

### [Variables Reference](variables.md)

Complete listing of all global and role-specific variables with their default values and descriptions.

### [Tags Reference](tags.md)

All available tags for selective playbook execution.

### [Distribution Support](distributions.md)

Supported Linux distributions and package mappings.

### [Roles Reference](roles/index.md)

Detailed documentation for all available roles:
- [Base Roles](roles/base/index.md)
- [Feature Roles](roles/features/index.md)
  - [Neovim Role](roles/features/nvim.md)

## Quick Reference

### Common Variables

| Variable | Default |
|----------|---------|
| `dotfiles_root` | `{{ playbook_dir }}/../../..` |
| `config_files_root` | `{{ dotfiles_root }}/config-files` |
| `xdg_config_home` | `$XDG_CONFIG_HOME` or `~/.config` |

### Available Tags

| Tag | Purpose |
|-----|---------|
| `debug` | Display path information |
| `nvim` | Install and configure Neovim |

### Supported Distributions

- Debian
- Fedora
- Archlinux

## See Also

- [Architecture Documentation](../architecture/index.md): System design
- [Getting Started](../getting-started/index.md): Installation and setup
- [Examples](../examples/index.md): Usage examples
