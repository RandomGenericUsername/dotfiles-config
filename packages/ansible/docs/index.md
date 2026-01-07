# Ansible Package Documentation

Welcome to the ansible package documentation. This package provides an Ansible-based system for installing and configuring software packages on the local machine as part of a larger dotfiles configuration system.

## What is This?

The ansible package is a configuration-only system that:
- Installs software packages on the local machine using Ansible
- Copies configuration files from the dotfiles repository to their target locations
- Supports multiple Linux distributions (Debian, Fedora, Archlinux)
- Enables selective execution using tags
- Integrates with external installer systems via variable overrides

This is **not** a standalone tool. It's designed to be invoked by an external installer that calls the ansible-playbook command with appropriate variables and tags.

## How It Fits Into the Dotfiles System

This package is part of a larger dotfiles configuration system:

1. The dotfiles repository contains configuration files in `config-files/`
2. The ansible package defines how to install software and where to copy configs
3. An external installer invokes the ansible playbook with custom paths
4. Ansible installs packages and copies configs to the appropriate XDG directories

The variable override mechanism allows the same Ansible configuration to work in different environments by providing custom paths at runtime.

## Quick Navigation

### Getting Started
- [Quick Start Guide](getting-started/index.md)
- [Prerequisites](getting-started/prerequisites.md)
- [Installation](getting-started/installation.md)

### Architecture
- [Overview](architecture/index.md)
- [Directory Structure](architecture/directory-structure.md)
- [Variable System](architecture/variable-system.md)
- [Roles Organization](architecture/roles-organization.md)

### Reference
- [Variables Reference](reference/variables.md)
- [Tags Reference](reference/tags.md)
- [Distribution Support](reference/distributions.md)
- [Roles Documentation](reference/roles/index.md)

### Guides
- [Adding a Role](guides/adding-a-role.md)
- [Adding Distribution Support](guides/adding-distribution-support.md)
- [Integration with External Installers](guides/integration.md)

### Examples
- [Basic Usage](examples/basic-usage.md)
- [Custom Paths](examples/custom-paths.md)
- [Selective Installation](examples/selective-install.md)

## Quick Start

Install Neovim with its configuration:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

See [Getting Started](getting-started/index.md) for more details.

## Key Concepts

### Tags

Tags are required to execute roles. Each role must be explicitly requested via tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

Running without tags displays available options without installing anything. See [Tags Reference](reference/tags.md) for all available tags.

### Variable Overrides

All paths and configurations can be overridden at runtime using the `-e` flag:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/path \
  -e nvim_config_dest=/custom/nvim/location
```

See [Variable System](architecture/variable-system.md) for details.

### Distribution Support

The package automatically detects your Linux distribution and installs the appropriate packages:

```bash
# Same command works on Debian, Fedora, or Archlinux
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

See [Distribution Support](reference/distributions.md) for supported distributions.

## Need Help?

- Check the [Getting Started Guide](getting-started/index.md) for installation and basic usage
- See [Examples](examples/index.md) for common usage patterns
- Review [Architecture Documentation](architecture/index.md) for system design details
- Consult [Reference Documentation](reference/index.md) for complete API documentation
