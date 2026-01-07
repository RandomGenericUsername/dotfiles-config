# Configuration Files Reference

[VERIFIED via CLI - 2026-01-03]

Documentation for all configuration files included in the repository.

## Overview

The `config-files/` directory contains configuration files for various tools and applications managed by the dotfiles system.

## Directory Structure

```
config-files/
├── nvim/              - Neovim configuration
│   ├── init.lua
│   └── lua/
│       ├── options.lua
│       └── plugins/
└── zsh/               - Zsh shell configuration
    └── .zshrc.j2
```

[VERIFIED via CLI - 2026-01-03]

## Configuration Files

### [Neovim](nvim.md)

Neovim text editor configuration using Lua.

**Location:** `config-files/nvim/`

**Files:**
- `init.lua` - Main configuration entry point
- `lua/options.lua` - Editor options
- `lua/plugins/*.lua` - Plugin configurations (catppuccin, lsp-config, lualine, neo-tree, telescope, treesitter)

[VERIFIED via CLI - 2026-01-03]

### [Zsh](zsh.md)

Z shell configuration.

**Location:** `config-files/zsh/`

**Files:**
- `.zshrc.j2` - Zsh configuration template (Jinja2 format)

[VERIFIED via CLI - 2026-01-03]

## Usage in Ansible

Configuration files are deployed using the Ansible package system. Variables control where files are installed:

- `config_files_root` - Root directory containing config files (default: `{{ dotfiles_root }}/config-files`)
- `xdg_config_home` - XDG config directory (default: `~/.config`)

[VERIFIED via source - 2026-01-03]

## See Also

- [Ansible Package Documentation](../../../packages/ansible/README.md)
- [Architecture: Integration Points](../../architecture/integration-points.md)
