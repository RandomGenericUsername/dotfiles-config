# Neovim Configuration

[VERIFIED via CLI - 2026-01-03]

Neovim configuration using Lua and lazy.nvim plugin manager.

## Location

`config-files/nvim/`

## File Structure

```
nvim/
├── init.lua               - Main entry point
└── lua/
    ├── options.lua        - Editor options
    └── plugins/
        ├── catppuccin.lua - Catppuccin theme
        ├── lsp-config.lua - LSP configuration
        ├── lualine.lua    - Status line
        ├── neo-tree.lua   - File tree
        ├── telescope.lua  - Fuzzy finder
        └── treesitter.lua - Syntax highlighting
```

[VERIFIED via CLI - 2026-01-03]

## Deployment

The Neovim configuration is deployed by the Ansible `nvim` role.

**Playbook:** `packages/ansible/playbooks/bootstrap.yml`

**Tag:** `nvim`

**Tasks:**
1. Install neovim package
2. Ensure destination directory exists
3. Copy Neovim config directory to `{{ xdg_config_home }}/nvim`

[VERIFIED via CLI - 2026-01-03]

## Installation

### Using CLI

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

### Using Ansible Directly

```bash
cd packages/ansible
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

## Ansible Variables

[VERIFIED via source - 2026-01-03]

**Role defaults** (`packages/ansible/playbooks/roles/features/nvim/defaults/main.yml`):

- `nvim_config_dest` - Destination for config files (default: `{{ xdg_config_home }}/nvim`)

**Role variables** (`packages/ansible/playbooks/roles/features/nvim/vars/main.yml`):

- `nvim_config_source` - Source config directory (default: `{{ config_files_root }}/nvim`)

## Plugin Manager

The configuration uses lazy.nvim for plugin management. Plugins are automatically installed on first launch.

[VERIFIED via CLI - 2026-01-03]

## Installed Plugins

[VERIFIED via CLI - 2026-01-03]

- **catppuccin** - Color theme
- **lsp-config** - Language Server Protocol support
- **lualine** - Status line
- **neo-tree** - File explorer
- **telescope** - Fuzzy finder
- **treesitter** - Syntax highlighting

## See Also

- [install-packages command](../cli/install-packages.md)
- [Ansible Package Documentation](../../../packages/ansible/README.md)
