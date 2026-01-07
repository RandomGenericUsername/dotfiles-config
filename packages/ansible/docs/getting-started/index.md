# Getting Started

This guide will help you quickly get started with the ansible package.

## Quick Start

The fastest way to get started is to run the playbook with a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

This command will:
1. Install Neovim using your distribution's package manager
2. Create the configuration directory (`~/.config/nvim` by default)
3. Copy Neovim configuration files from the dotfiles repository

## Prerequisites

Before running the playbook, ensure you have:
- Ansible installed (version 2.20+ recommended)
- Python 3 installed
- Root/sudo privileges for package installation

See [Prerequisites](prerequisites.md) for detailed requirements.

## Installation

If you don't have Ansible installed yet, see the [Installation Guide](installation.md) for instructions.

## Basic Commands

### List Available Tags

See what roles are available:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags
```

### Run Specific Roles

Roles require explicit tags to execute:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

Running without tags will display available options but won't install anything.

### Debug Mode

Display configuration paths without making changes:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug
```

### Check Mode

Preview what would be changed without actually making changes:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --check --ask-become-pass
```

## Next Steps

- Read the [Architecture Overview](../architecture/index.md) to understand how the system works
- Check [Available Tags](../reference/tags.md) to see what you can install
- Review [Examples](../examples/index.md) for common usage patterns
- Learn about [Variable Overrides](../examples/custom-paths.md) for custom configurations

## Common Issues

### Permission Denied

If you get permission denied errors, ensure you're using `--ask-become-pass` for operations that require root privileges.

### Python Not Found

If Ansible can't find Python, verify that Python 3 is installed at `/usr/bin/python3` or override the interpreter path:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e ansible_python_interpreter=/path/to/python3 \
  --ask-become-pass
```

### Configuration Files Not Found

If the playbook can't find configuration files, verify that the source directory exists or override the path:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e config_files_root=/path/to/config-files \
  --ask-become-pass
```

See [Integration Guide](../guides/integration.md) for more details on variable overrides.
