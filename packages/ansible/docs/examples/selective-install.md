# Selective Installation Examples

This document demonstrates using tags for selective installation of software packages.

## Overview

[VERIFIED] Tags allow you to install specific software without running the entire playbook. This is useful for:
- Installing only what you need
- Testing individual roles
- Incremental installation
- Updating specific configurations

## Available Tags

[VERIFIED] Current available tags (via `ansible-playbook --list-tags`):

- `debug`: Display path information
- `nvim`: Install and configure Neovim

## Basic Tag Usage

### Install Single Package

Install only Neovim:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass
```

### Install Multiple Packages

Install multiple packages by combining tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git,tmux \
  --ask-become-pass
```

Note: Separate tags with commas, no spaces.

### Run Only Debug

Display configuration paths without installing anything:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags debug
```

## Excluding Tags

### Skip Specific Tags

Run everything except debug tasks:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --skip-tags debug \
  --ask-become-pass
```

### Skip Multiple Tags

Run everything except specific roles:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --skip-tags debug,nvim \
  --ask-become-pass
```

## Preview What Will Run

### List Tasks for Tag

[VERIFIED] See what tasks will execute for a specific tag:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --list-tasks
```

Output shows:
```
nvim : Install neovim
nvim : Ensure destination directory exists
nvim : Copy Neovim config directory
```

### List Tasks for Multiple Tags

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git \
  --list-tasks
```

### List All Available Tags

See all tags in the playbook:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --list-tags
```

## Dry Run with Tags

### Check Mode for Specific Tag

Preview what would change for a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --check \
  --ask-become-pass
```

### Check Mode with Diff

See file changes for a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --check \
  --diff \
  --ask-become-pass
```

## Incremental Installation Workflow

### Step-by-Step Installation

Install software incrementally, one at a time:

```bash
# Step 1: Install Neovim
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass

# Step 2: Install Git (when that role exists)
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags git \
  --ask-become-pass

# Step 3: Install tmux (when that role exists)
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags tmux \
  --ask-become-pass
```

### Install Essential First, Others Later

Install critical tools first:

```bash
# Essential tools first
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git,shell \
  --ask-become-pass

# Optional tools later
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags docker,kubernetes,extras \
  --ask-become-pass
```

## Testing New Roles

### Test New Role Alone

When adding a new role, test it independently:

```bash
# Check syntax first
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check

# List tasks to verify role appears
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags new_role \
  --list-tasks

# Dry run
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags new_role \
  --check \
  --ask-become-pass

# Actually run
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags new_role \
  --ask-become-pass
```

### Test Multiple New Roles

Test several new roles together:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags new_role1,new_role2,new_role3 \
  --check \
  --ask-become-pass
```

## Updating Configurations

### Update Single Configuration

Re-run a role to update just its configuration:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass
```

Ansible is idempotent:
- If package is already installed, it won't reinstall
- If config files haven't changed, they won't be copied
- Only changes are applied

### Update Multiple Configurations

Update configurations for multiple tools:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git,shell \
  --ask-become-pass
```

## Combining Tags with Other Options

### Tags with Custom Paths

Combine tag selection with path overrides:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  -e nvim_config_dest=/custom/nvim/path \
  --ask-become-pass
```

### Tags with Verbose Output

Debug specific role execution:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  -vv \
  --ask-become-pass
```

### Tags with Check and Diff

Preview changes for specific roles with details:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git \
  --check \
  --diff \
  --ask-become-pass
```

## Use Cases

### Minimal Installation

Install only essential tools on a minimal system:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass
```

### Development Workstation

Install development-focused tools:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim,git,docker,python,node \
  --ask-become-pass
```

### Server Installation

Install server-specific tools (skip desktop apps):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags server,monitoring,security \
  --skip-tags desktop,gui \
  --ask-become-pass
```

### Quick Debug

Debug paths without installing anything:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags debug
```

## External Installer Integration

### User-Selected Software

Allow users to select what to install:

```bash
#!/bin/bash

# User selection
echo "Select software to install:"
echo "1. Neovim"
echo "2. Git"
echo "3. Both"
read -p "Choice: " choice

case $choice in
  1) TAGS="nvim" ;;
  2) TAGS="git" ;;
  3) TAGS="nvim,git" ;;
  *) echo "Invalid choice"; exit 1 ;;
esac

# Install selected software
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags "$TAGS" \
  --ask-become-pass
```

### Configuration File Driven

Use a configuration file to determine what to install:

```bash
#!/bin/bash

# Read from config file
CONFIG_FILE="install-config.txt"
TAGS=$(cat "$CONFIG_FILE" | tr '\n' ',' | sed 's/,$//')

ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags "$TAGS" \
  --ask-become-pass
```

Where `install-config.txt` contains:
```
nvim
git
tmux
```

## Tag Naming Conventions

[VERIFIED] Current convention:
- Tag names match role names
- Use lowercase
- Use underscores for multi-word names
- Descriptive and clear

Examples:
- `nvim` for Neovim role
- `debug` for debugging tasks
- Future: `python_dev`, `docker_compose`, etc.

## See Also

- [Tags Reference](../reference/tags.md): Complete tag documentation
- [Basic Usage](basic-usage.md): General usage examples
- [Custom Paths](custom-paths.md): Variable override examples
- [Adding a Role](../guides/adding-a-role.md): Creating new roles with tags
