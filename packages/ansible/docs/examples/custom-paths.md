# Custom Paths Examples

This document shows how to override default paths using variable overrides.

## Overview

[VERIFIED] All paths can be overridden at runtime using the `-e` flag. This is useful when:
- Integrating with external installers
- Testing with non-standard paths
- Managing multiple dotfiles configurations
- Installing to temporary locations

## Global Path Overrides

### Override Dotfiles Root

[VERIFIED] Change the dotfiles repository location:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/dotfiles/path \
  --ask-become-pass
```

This affects:
- `assets_root` → `/custom/dotfiles/path/assets`
- `config_files_root` → `/custom/dotfiles/path/config-files`

### Override Configuration Files Root

Change where configuration files are read from:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e config_files_root=/custom/configs \
  --tags nvim \
  --ask-become-pass
```

### Override Assets Root

Change the assets directory location:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e assets_root=/custom/assets \
  --ask-become-pass
```

### Override Multiple Global Paths

Combine multiple global overrides:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/home/user/my-dotfiles \
  -e config_files_root=/etc/dotfiles-configs \
  -e assets_root=/usr/share/dotfiles-assets \
  --ask-become-pass
```

## XDG Directory Overrides

### Override XDG Config Home

[VERIFIED] Change the XDG config directory (normally `~/.config`):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e xdg_config_home=/tmp/test-config \
  --tags nvim \
  --ask-become-pass
```

This changes where all config files are installed.

### Override XDG Data Home

Change the XDG data directory (normally `~/.local/share`):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e xdg_data_home=/custom/data \
  --ask-become-pass
```

### Override XDG Bin Home

Change the binary installation directory:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e xdg_bin_home=/custom/bin \
  --ask-become-pass
```

## Role-Specific Path Overrides

### Neovim Custom Destination

[VERIFIED] Install Neovim config to a custom location:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e nvim_config_dest=/tmp/nvim-test \
  --tags nvim \
  --ask-become-pass
```

### Neovim Custom Source

Read Neovim config from a custom source:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e nvim_config_src_dir=/custom/nvim-source \
  --tags nvim \
  --ask-become-pass
```

### Both Source and Destination

Override both source and destination:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e nvim_config_src_dir=/custom/source/nvim \
  -e nvim_config_dest=/custom/dest/nvim \
  --tags nvim \
  --ask-become-pass
```

## Testing Scenarios

### Test in Isolated Location

Test the playbook without affecting your actual config:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e xdg_config_home=/tmp/ansible-test-config \
  -e xdg_data_home=/tmp/ansible-test-data \
  --tags nvim \
  --ask-become-pass
```

After testing, remove the test directories:

```bash
rm -rf /tmp/ansible-test-config /tmp/ansible-test-data
```

### Test with Custom Dotfiles

Test with a different dotfiles repository:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/tmp/test-dotfiles \
  -e xdg_config_home=/tmp/test-output \
  --check \
  --ask-become-pass
```

### Preview Installation Paths

Use debug mode to see where files would be installed:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/path \
  -e xdg_config_home=/custom/config \
  --tags debug
```

## External Installer Integration

### Installer Script Example

Example of how an external installer might call ansible:

```bash
#!/bin/bash

# Installer determines paths
DOTFILES_ROOT="/home/user/dotfiles"
CONFIG_HOME="/home/user/.config"
DATA_HOME="/home/user/.local/share"
SOFTWARE_TO_INSTALL="nvim"

# Run ansible with overrides
ansible-playbook \
  -i "${DOTFILES_ROOT}/config/packages/ansible/inventory/localhost.yml" \
  "${DOTFILES_ROOT}/config/packages/ansible/playbooks/bootstrap.yml" \
  -e "dotfiles_root=${DOTFILES_ROOT}" \
  -e "xdg_config_home=${CONFIG_HOME}" \
  -e "xdg_data_home=${DATA_HOME}" \
  --tags "${SOFTWARE_TO_INSTALL}" \
  --ask-become-pass
```

### Python Installer Example

```python
#!/usr/bin/env python3
import subprocess
import os

def install_with_ansible(dotfiles_root, software_tags):
    """Run ansible with custom paths."""

    ansible_dir = os.path.join(dotfiles_root, "config/packages/ansible")
    config_home = os.path.expanduser("~/.config")
    data_home = os.path.expanduser("~/.local/share")

    cmd = [
        "ansible-playbook",
        "-i", f"{ansible_dir}/inventory/localhost.yml",
        f"{ansible_dir}/playbooks/bootstrap.yml",
        "-e", f"dotfiles_root={dotfiles_root}",
        "-e", f"xdg_config_home={config_home}",
        "-e", f"xdg_data_home={data_home}",
        "--tags", ",".join(software_tags),
        "--ask-become-pass"
    ]

    subprocess.run(cmd, cwd=ansible_dir, check=True)

if __name__ == "__main__":
    install_with_ansible(
        dotfiles_root="/home/user/dotfiles",
        software_tags=["nvim"]
    )
```

## Environment-Specific Configurations

### Development Environment

Install to development-specific locations:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/workspace/dotfiles \
  -e xdg_config_home=/workspace/.config \
  --ask-become-pass
```

### CI/CD Environment

Install to CI-specific locations without interactive prompts:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root="${CI_PROJECT_DIR}/dotfiles" \
  -e xdg_config_home="${CI_PROJECT_DIR}/.config" \
  --tags nvim
```

Note: Assumes passwordless sudo or packages are already installed.

## Multiple Configurations

### User-Specific Paths

Install different configurations for different users:

```bash
# User 1
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e home_root=/home/user1 \
  -e xdg_config_home=/home/user1/.config \
  --ask-become-pass

# User 2
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e home_root=/home/user2 \
  -e xdg_config_home=/home/user2/.config \
  --ask-become-pass
```

### Profile-Based Paths

Different configurations for work vs personal:

```bash
# Work profile
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e config_files_root=/dotfiles/profiles/work \
  -e xdg_config_home=~/.config-work \
  --ask-become-pass

# Personal profile
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e config_files_root=/dotfiles/profiles/personal \
  -e xdg_config_home=~/.config \
  --ask-become-pass
```

## Verification

### Verify Custom Paths

After running with custom paths, verify files are in the correct location:

```bash
# Run with custom path
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e nvim_config_dest=/tmp/nvim-custom \
  --tags nvim \
  --ask-become-pass

# Verify files exist
ls -la /tmp/nvim-custom/
```

### Debug Custom Paths

Use debug tag to verify path calculations:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/dotfiles \
  -e xdg_config_home=/custom/config \
  --tags debug
```

## Common Patterns

### All Variables from File

Create a variables file and load it:

```bash
# Create vars.yml
cat > /tmp/custom-vars.yml <<EOF
dotfiles_root: /home/user/dotfiles
xdg_config_home: /home/user/.config
xdg_data_home: /home/user/.local/share
nvim_config_dest: /home/user/.config/nvim
EOF

# Use it
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e @/tmp/custom-vars.yml \
  --ask-become-pass
```

## See Also

- [Variable System](../architecture/variable-system.md): Variable precedence details
- [Variables Reference](../reference/variables.md): All available variables
- [Integration Guide](../guides/integration.md): External installer integration
- [Basic Usage](basic-usage.md): Common commands
