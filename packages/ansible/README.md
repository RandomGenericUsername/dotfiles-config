# Ansible Package

Ansible-based configuration system for installing and configuring software packages as part of the dotfiles configuration system.

## Quick Start

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --ask-become-pass --tags nvim
```

## Documentation

Complete documentation is available in the [docs/](docs/index.md) directory.

- [Getting Started](docs/getting-started/index.md): Installation and prerequisites
- [Architecture](docs/architecture/index.md): System design and organization
- [Reference](docs/reference/index.md): Variables, tags, and roles reference
- [Guides](docs/guides/index.md): How-to guides for common tasks
- [Examples](docs/examples/index.md): Usage examples

## Features

- Multi-distribution support (Debian, Fedora, Archlinux)
- Tag-based selective role execution
- XDG Base Directory compliant
- Variable override system for external integration
- Local-only execution (no remote hosts)

## Requirements

- Ansible 2.20+ (tested with ansible-core 2.20.1)
- Python 3
- Root/sudo privileges for package installation

## Basic Usage

Run specific roles (roles require explicit tags):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

Run with debug output:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug
```

Run multiple roles:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim,other-role --ask-become-pass
```

Override variables:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --ask-become-pass \
  -e dotfiles_root=/custom/path \
  -e nvim_config_dest=/tmp/nvim-test
```

See the [documentation](docs/index.md) for detailed usage instructions.
