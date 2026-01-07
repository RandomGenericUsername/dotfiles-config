# Architecture Overview

This section provides a comprehensive overview of the ansible package architecture.

## System Purpose

The ansible package is a configuration-only system designed to:
- Install and configure software packages on the local machine
- Copy configuration files from the dotfiles repository to their target locations
- Support multiple Linux distributions (Debian, Fedora, Archlinux)
- Enable selective role execution using tags

## Design Philosophy

### Configuration, Not Installation

This package contains **only configuration files** and does not include installation logic for the ansible tool itself. It is designed to be invoked via CLI by an external installer project.

### Variable Override System

[VERIFIED] All paths and configurations can be overridden by external installers using Ansible's extra variables mechanism (`-e` flag). This allows the same configuration to adapt to different environments.

Default variables are defined in `inventory/group_vars/all.yml` and can be overridden at runtime:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  -e dotfiles_root=/custom/path
```

### Tag-Based Selective Execution

[VERIFIED] Roles are tagged to allow selective execution. Users can install specific packages without running the entire playbook:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

## Component Relationships

```text
┌─────────────────────────────────────────────────────────┐
│ External Installer                                      │
│ (Calls ansible-playbook with custom variables)         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ ansible.cfg                                             │
│ • Defines inventory path                               │
│ • Defines roles paths                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Inventory (inventory/localhost.yml)                     │
│ • Defines local connection                             │
│ • Sets Python interpreter                              │
│ • Loads global variables from group_vars/all.yml       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Playbook (playbooks/bootstrap.yml)                      │
│ • Gathers system facts                                 │
│ • Runs pre-tasks (debug)                               │
│ • Executes roles based on tags                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Roles (playbooks/roles/base & features)                 │
│ • Install packages based on distribution               │
│ • Create required directories                          │
│ • Copy configuration files to destinations             │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### Configuration (`ansible.cfg`)

[VERIFIED] Defines:
- Inventory location: `./inventory/localhost.yml`
- Roles paths: `./playbooks/roles/base:./playbooks/roles/features`
- Deprecation warnings: Enabled

### Inventory System

[VERIFIED] Consists of:
- **localhost.yml**: Host definition with local connection
- **group_vars/all.yml**: Global variables for all hosts

### Playbook System

[VERIFIED] Single main playbook:
- **bootstrap.yml**: Orchestrates role execution with tag-based filtering

### Role System

Organized into categories:
- **base/**: Fundamental system roles (currently empty)
- **features/**: Feature-specific software installation roles

## Documentation Structure

- **[Directory Structure](directory-structure.md)**: Complete file and folder layout
- **[Variable System](variable-system.md)**: Variable precedence and override mechanisms
- **[Roles Organization](roles-organization.md)**: How roles are structured and invoked

## Integration Points

External installers interact with this system by:

1. Calling `ansible-playbook` with appropriate inventory and playbook paths
2. Overriding default variables using `-e` flags
3. Selecting specific roles using `--tags`
4. Optionally requesting privilege escalation with `--ask-become-pass`

See [Integration Guide](../guides/integration.md) for detailed integration instructions.
