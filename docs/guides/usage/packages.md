# Installing Packages

[VERIFIED via CLI - 2026-01-03]

Guide to installing and configuring packages using the `config install-packages` command.

## Overview

The `install-packages` command uses Ansible to install system packages and deploy configuration files. It runs the `packages/ansible/playbooks/bootstrap.yml` playbook.

[VERIFIED via source - 2026-01-03]

## Prerequisites

**Ansible must be installed:**

```bash
ansible --version
```

Required: Ansible 2.20+

[VERIFIED via source - 2026-01-03]

Install if needed:
```bash
pipx install ansible-core
# or
pip install ansible-core
```

## Basic Usage

### Install All Packages

```bash
config install-packages --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

The `--ask-become-pass` flag prompts for your sudo password.

### Install Specific Packages

Use tags to install only certain components:

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

## Available Tags

[VERIFIED via CLI - 2026-01-03]

- `nvim` - Install and configure Neovim
- `debug` - Show debug information (paths, variables)

## Debug Mode

View configuration paths and variables:

```bash
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

**Example output:**
```
TASK [Debug paths]
ok: [localhost] => {
    "msg": [
        "playbook_dir=/path/to/packages/ansible/playbooks",
        "dotfiles_root=/path/to/dotfiles/config",
        "config_files_root=/path/to/dotfiles/config/config-files"
    ]
}
```

## Ansible Options

All Ansible options can be forwarded:

### Increase Verbosity

```bash
config install-packages --tags nvim -v       # Verbose
config install-packages --tags nvim -vv      # More verbose
config install-packages --tags nvim -vvv     # Very verbose
```

[VERIFIED via CLI - 2026-01-03]

### Override Variables

```bash
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test
```

[VERIFIED via CLI - 2026-01-03]

### Multiple Tags

```bash
config install-packages --tags nvim,debug --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

## What Gets Installed

### Neovim (`--tags nvim`)

[VERIFIED via CLI - 2026-01-03]

**Installs:**
1. Neovim package (via system package manager)

**Configures:**
1. Copies `config-files/nvim/` to `~/.config/nvim/`

**Variables:**
- `nvim_config_source` - Source directory (default: `{{ config_files_root }}/nvim`)
- `nvim_config_dest` - Destination directory (default: `{{ xdg_config_home }}/nvim`)

[VERIFIED via source - 2026-01-03]

## Configuration Variables

[VERIFIED via source - 2026-01-03]

**Global variables** (defined in `packages/ansible/inventory/group_vars/all.yml`):

- `dotfiles_root` - Root directory (default: `{{ playbook_dir }}/../../..`)
- `config_files_root` - Config files directory (default: `{{ dotfiles_root }}/config-files`)
- `assets_root` - Assets directory (default: `{{ dotfiles_root }}/assets`)
- `xdg_config_home` - XDG config directory (default: `~/.config`)
- `xdg_data_home` - XDG data directory (default: `~/.local/share`)
- `xdg_bin_home` - User binaries directory (default: `~/.local/bin`)

## Common Workflows

### Workflow 1: New System Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd dotfiles/config

# 2. Install CLI
make install-dev
source .venv/bin/activate

# 3. Install packages
config install-packages --tags nvim --ask-become-pass

# 4. Verify Neovim configuration
nvim --version
ls ~/.config/nvim
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 2: Test Configuration

```bash
# Test in temporary directory
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test

# Verify
ls /tmp/nvim-test

# Clean up
rm -rf /tmp/nvim-test
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 3: Update Configuration

```bash
# Edit config files
vim config-files/nvim/init.lua

# Redeploy
config install-packages --tags nvim

# Configuration updated in ~/.config/nvim/
```

[VERIFIED via CLI - 2026-01-03]

## Error Messages

**Ansible not found:**
```
Error: ansible-playbook command not found. Please install Ansible.
```

**Solution:** Install Ansible (see Prerequisites).

**Permission denied:**
```
fatal: [localhost]: FAILED! => ... Permission denied
```

**Solution:** Use `--ask-become-pass` flag.

## Tips and Best Practices

### 1. Test with Debug First

```bash
config install-packages --tags debug
```

Verify paths before installing.

### 2. Use Verbosity for Troubleshooting

```bash
config install-packages --tags nvim -vv
```

Shows detailed Ansible output.

### 3. Test in Temporary Location

```bash
config install-packages --tags nvim -e nvim_config_dest=/tmp/test
```

Test before deploying to real location.

### 4. Use Specific Tags

Don't install everything at once:

```bash
config install-packages --tags nvim  # Just Neovim
```

Rather than:

```bash
config install-packages  # Everything (may have unintended effects)
```

## See Also

- [CLI Reference: install-packages](../../reference/cli/install-packages.md)
- [Ansible Package Documentation](../../../packages/ansible/README.md)
- [Neovim Configuration](../../reference/config-files/nvim.md)
