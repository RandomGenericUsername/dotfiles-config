# Roles Reference

This document provides an overview of all available roles in the ansible package.

## Role Categories

Roles are organized into two categories:

### Base Roles

[EMPTY DIRECTORY] No base roles have been implemented yet.

See [Base Roles Index](base/index.md) for details.

### Feature Roles

[VERIFIED] Feature roles install and configure specific software packages.

Currently available feature roles:
- **[nvim](features/nvim.md)**: Neovim text editor installation and configuration

See [Feature Roles Index](features/index.md) for details.

## Role Structure

All roles follow the standard Ansible role structure:

```text
role_name/
├── defaults/
│   └── main.yml      # Default variables
├── vars/
│   └── main.yml      # Role-specific variables
└── tasks/
    └── main.yml      # Tasks to execute
```

## Using Roles

Roles are executed via tags in the main playbook. To run a specific role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags <role-tag>
```

For example, to run the nvim role:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

## Creating New Roles

To create a new role, see the [Adding a Role Guide](../../guides/adding-a-role.md).

## See Also

- [Tags Reference](../tags.md): Complete list of available tags
- [Roles Organization](../../architecture/roles-organization.md): Architecture details
