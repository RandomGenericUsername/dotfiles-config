# Directory Structure

This document describes the complete directory structure of the ansible package.

## Overview

```text
.
├── ansible.cfg
├── DOCS_REQUIREMENTS.md
├── inventory
│   ├── group_vars
│   │   └── all.yml
│   └── localhost.yml
├── playbooks
│   ├── bootstrap.yml
│   └── roles
│       ├── base
│       └── features
│           └── nvim
│               ├── defaults
│               │   └── main.yml
│               ├── tasks
│               │   └── main.yml
│               └── vars
│                   └── main.yml
├── README.md
└── docs/
    ├── index.md
    ├── getting-started/
    ├── architecture/
    ├── reference/
    ├── guides/
    └── examples/
```

## Root Level Files

### `ansible.cfg`

[VERIFIED] Ansible configuration file that defines:
- **inventory**: Path to inventory file (`./inventory/localhost.yml`)
- **roles_path**: Paths to role directories (`./playbooks/roles/base:./playbooks/roles/features`)
- **deprecation_warnings**: Enabled (set to `True`)

### `README.md`

Main project README with quick start information and links to detailed documentation.

### `DOCS_REQUIREMENTS.md`

Documentation requirements specification for this project.

## Inventory Directory

### `inventory/localhost.yml`

[VERIFIED] Defines the localhost host with:
- `ansible_connection: local` - Uses local connection
- `ansible_python_interpreter: /usr/bin/python3` - Python 3 interpreter path

### `inventory/group_vars/all.yml`

[VERIFIED] Global variables available to all hosts. See [Variable System](variable-system.md) for details.

## Playbooks Directory

### `playbooks/bootstrap.yml`

[VERIFIED] Main playbook that:
- Targets localhost
- Gathers facts
- Includes a debug pre-task (tagged with `debug`)
- Executes roles based on tags

### `playbooks/roles/`

Contains all Ansible roles organized into two categories:

#### `playbooks/roles/base/`

[EMPTY DIRECTORY] Reserved for base system roles. No roles have been implemented yet.

#### `playbooks/roles/features/`

[VERIFIED] Contains feature-specific roles:
- **nvim**: Neovim installation and configuration role

## Role Structure

Each role follows standard Ansible role structure:

```text
role_name/
├── defaults/
│   └── main.yml      # Default variables (lowest precedence)
├── vars/
│   └── main.yml      # Role variables (higher precedence)
└── tasks/
    └── main.yml      # Tasks to execute
```

[VERIFIED] The nvim role implements this structure with all three directories.

## Documentation Directory

The `docs/` directory contains comprehensive documentation organized by topic:

- **getting-started/**: Installation and prerequisites
- **architecture/**: System design and organization
- **reference/**: Complete API and variable reference
- **guides/**: How-to guides for common tasks
- **examples/**: Usage examples
