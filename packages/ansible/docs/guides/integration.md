# Integration with External Installers

This guide explains how external installer systems can integrate with the ansible package.

## Overview

The ansible package is designed as a configuration-only system that external installers invoke via the `ansible-playbook` command. All paths and configurations can be overridden using command-line variables.

## Integration Architecture

```text
External Installer
       │
       ├─ Determines paths (dotfiles location, install targets)
       ├─ Selects which software to install (tags)
       ├─ Constructs ansible-playbook command
       │
       ▼
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/path/to/dotfiles \
  -e nvim_config_dest=/custom/nvim/path \
  --tags nvim \
  --ask-become-pass
```

## Command Construction

### Basic Command Structure

[VERIFIED] Based on `ansible.cfg` paths:

```bash
ansible-playbook \
  -i <inventory_path> \
  <playbook_path> \
  [options]
```

**Required**:
- **Inventory**: `-i inventory/localhost.yml` (relative to ansible package root)
- **Playbook**: `playbooks/bootstrap.yml` (relative to ansible package root)

### Common Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--tags <tags>` | Select specific roles | `--tags nvim` |
| `--ask-become-pass` | Prompt for sudo password | Required for package installation |
| `-e key=value` | Override variables | `-e dotfiles_root=/custom/path` |
| `--check` | Dry run mode | Preview changes |
| `--diff` | Show file differences | See what files will change |
| `-v`, `-vv`, `-vvv` | Increase verbosity | Debugging |

## Variable Override Strategy

### Essential Variables

[VERIFIED] Variables that external installers typically override:

| Variable | Default | When to Override |
|----------|---------|------------------|
| `dotfiles_root` | `{{ playbook_dir }}/../../..` | Always override with actual dotfiles location |
| `config_files_root` | `{{ dotfiles_root }}/config-files` | If config files are in a non-standard location |
| `assets_root` | `{{ dotfiles_root }}/assets` | If assets are in a non-standard location |

### Role-Specific Variables

Override destination paths for specific roles:

```bash
-e nvim_config_dest=/custom/nvim/path
-e nvim_config_src_dir=/custom/nvim/source
```

### Multiple Variable Overrides

Combine multiple overrides:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/home/user/dotfiles \
  -e config_files_root=/home/user/dotfiles/configs \
  -e nvim_config_dest=/tmp/nvim-test \
  --tags nvim \
  --ask-become-pass
```

## Tag Selection

### List Available Tags

External installers should query available tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags
```

[VERIFIED] Current tags:
- `debug`: Display path information
- `nvim`: Install Neovim

### Selective Installation

Install specific software by tags:

```bash
# Single role
--tags nvim

# Multiple roles
--tags nvim,other_role

# All except some
--skip-tags debug
```

### Dynamic Tag Selection

Example pseudo-code for external installer:

```python
# Determine what to install
selected_software = ["nvim", "git", "tmux"]

# Construct tag argument
tags_arg = ",".join(selected_software)

# Build command
cmd = [
    "ansible-playbook",
    "-i", "inventory/localhost.yml",
    "playbooks/bootstrap.yml",
    "--tags", tags_arg,
    "--ask-become-pass"
]
```

## Privilege Escalation

### When Required

[VERIFIED] Root privileges are needed for:
- Package installation (all roles that install software)

### Options

**Interactive password prompt**:
```bash
--ask-become-pass
```

**Passwordless sudo** (if configured):
```bash
# No additional flag needed
```

**Provide password via variable**:
```bash
--extra-vars "ansible_become_pass=password"
```

Note: Storing passwords in variables is insecure. Use with caution.

## Error Handling

### Check Syntax Before Execution

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check
```

Exit code 0 = valid syntax.

### Dry Run Mode

Preview changes without applying them:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --check \
  -e dotfiles_root=/path/to/dotfiles \
  --tags nvim
```

### Exit Codes

Ansible uses standard exit codes:
- `0`: Success
- `1`: Error occurred
- `2`: Host or task failure

External installers should check exit codes:

```bash
if ! ansible-playbook ...; then
    echo "Ansible playbook failed"
    exit 1
fi
```

## Working Directory

[VERIFIED] Commands should be run from the ansible package root:

```bash
cd /path/to/dotfiles/config/packages/ansible
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml ...
```

Or use absolute paths:

```bash
ansible-playbook \
  -i /path/to/dotfiles/config/packages/ansible/inventory/localhost.yml \
  /path/to/dotfiles/config/packages/ansible/playbooks/bootstrap.yml \
  ...
```

## Example Integration

### Python Installer Example

```python
#!/usr/bin/env python3
import subprocess
import sys

def run_ansible(dotfiles_root, tags, ask_pass=True):
    """Run ansible playbook with custom variables."""

    ansible_dir = f"{dotfiles_root}/config/packages/ansible"

    cmd = [
        "ansible-playbook",
        "-i", f"{ansible_dir}/inventory/localhost.yml",
        f"{ansible_dir}/playbooks/bootstrap.yml",
        "-e", f"dotfiles_root={dotfiles_root}",
        "--tags", ",".join(tags),
    ]

    if ask_pass:
        cmd.append("--ask-become-pass")

    result = subprocess.run(cmd, cwd=ansible_dir)
    return result.returncode

if __name__ == "__main__":
    dotfiles = "/home/user/dotfiles"
    software = ["nvim"]

    exit_code = run_ansible(dotfiles, software)
    sys.exit(exit_code)
```

### Bash Installer Example

```bash
#!/bin/bash

DOTFILES_ROOT="/home/user/dotfiles"
ANSIBLE_DIR="${DOTFILES_ROOT}/config/packages/ansible"
TAGS="nvim"

cd "${ANSIBLE_DIR}" || exit 1

ansible-playbook \
  -i inventory/localhost.yml \
  playbooks/bootstrap.yml \
  -e "dotfiles_root=${DOTFILES_ROOT}" \
  --tags "${TAGS}" \
  --ask-become-pass

exit $?
```

## Debugging Integration

### Enable Verbose Output

```bash
ansible-playbook ... -vvv
```

### Debug Paths

Run the debug task to verify paths:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/path \
  --tags debug
```

[VERIFIED] This displays:
- `playbook_dir`
- `dotfiles_root`
- `config_files_root`

### List Tasks

Verify what will be executed:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  --list-tasks
```

## Best Practices

1. **Always override `dotfiles_root`**: Don't rely on the default calculated path
2. **Validate paths exist**: Check that source directories exist before running
3. **Use check mode first**: Run with `--check` to preview changes
4. **Handle exit codes**: Always check ansible-playbook exit status
5. **Log output**: Capture ansible output for debugging
6. **Use absolute paths**: Avoid ambiguity with absolute paths in overrides
7. **Query tags dynamically**: Use `--list-tags` rather than hardcoding tag names

## See Also

- [Variable System](../architecture/variable-system.md): Variable precedence details
- [Tags Reference](../reference/tags.md): Available tags
- [Variables Reference](../reference/variables.md): All variables
- [Examples](../examples/index.md): Usage examples
