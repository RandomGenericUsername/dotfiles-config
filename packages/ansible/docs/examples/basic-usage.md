# Basic Usage Examples

This document provides common usage patterns for the ansible package.

## Simple Installation

### List Available Roles

Run without tags to see what's available:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml
```

This will display available tags and example commands.

### Install Specific Software

[VERIFIED] Install only Neovim:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

### Install Multiple Software Packages

Install multiple roles by combining tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim,git,tmux --ask-become-pass
```

## Checking Before Running

### Syntax Check

Verify the playbook syntax is valid:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check
```

Expected output:
```
playbook: playbooks/bootstrap.yml
```

### List Available Tags

[VERIFIED] See what software can be installed:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags
```

Output shows:
```
TASK TAGS: [debug, never, nvim]
```

### List All Tasks

See what tasks will be executed without tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tasks
```

[VERIFIED] Shows tasks that run when no tags are specified (help message and debug paths).

### List Tasks for Specific Tags

See tasks for a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --list-tasks
```

## Dry Run Mode

### Check Mode

Preview what changes would be made without actually making them:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --check --ask-become-pass
```

### Check Mode with Diff

See what changes would be made to files:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --check --diff --ask-become-pass
```

### Check Specific Role

Preview changes for a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --check --ask-become-pass
```

## Debugging

### Display Path Information

[VERIFIED] Run the debug task to see configured paths:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug
```

This displays:
- `playbook_dir`: Directory containing the playbook
- `dotfiles_root`: Root of dotfiles repository
- `config_files_root`: Configuration files directory

### Verbose Output

Increase verbosity for troubleshooting:

```bash
# Level 1 verbosity
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim -v --ask-become-pass

# Level 2 verbosity (shows task results)
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim -vv --ask-become-pass

# Level 3 verbosity (shows detailed execution)
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim -vvv --ask-become-pass
```

### Show File Differences

See what changes will be made to files:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --diff --ask-become-pass
```

## Skipping Tasks

### Skip Specific Tags

Run everything except certain tasks:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --skip-tags debug --ask-become-pass
```

### Skip Multiple Tags

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --skip-tags debug,nvim --ask-become-pass
```

## Non-Interactive Mode

### With Passwordless Sudo

If you have passwordless sudo configured:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

### With Password in Variable

**Warning**: This is insecure. Only use in trusted environments.

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags nvim \
  -e ansible_become_pass=your_password
```

## Running from Different Directories

### Using Absolute Paths

Run from any directory using absolute paths:

```bash
ansible-playbook \
  -i /home/user/dotfiles/config/packages/ansible/inventory/localhost.yml \
  /home/user/dotfiles/config/packages/ansible/playbooks/bootstrap.yml \
  --tags nvim \
  --ask-become-pass
```

### Using Environment Variables

Set environment variable for ansible config:

```bash
export ANSIBLE_CONFIG=/path/to/dotfiles/config/packages/ansible/ansible.cfg
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

## Common Workflows

### Initial Setup

First time setting up on a new machine:

```bash
# 1. See available roles
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags

# 2. Check paths
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug

# 3. Preview changes for a specific role
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --check --ask-become-pass

# 4. Install the role
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

### Testing New Role

When testing a newly added role:

```bash
# 1. Check syntax
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check

# 2. List tasks to verify role appears
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags new_role --list-tasks

# 3. Dry run
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags new_role --check --ask-become-pass

# 4. Run with verbose output
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags new_role -vv --ask-become-pass
```

### Updating Configuration

When updating configuration files only (no package installation):

```bash
# Skip package installation if packages are already installed
# Just copy updated config files
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

Note: Ansible is idempotent, so re-running won't reinstall packages if they're already present.

## See Also

- [Custom Paths](custom-paths.md): Overriding default paths
- [Selective Installation](selective-install.md): More tag usage examples
- [Tags Reference](../reference/tags.md): Complete tag listing
- [Getting Started](../getting-started/index.md): Installation and setup
