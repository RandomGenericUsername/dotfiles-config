# Distribution Support

This document details the Linux distributions supported by the ansible package.

## Supported Distributions

[VERIFIED] The following distributions are supported, as defined in role variable files:

| Distribution | Support Level | Package Manager |
|--------------|---------------|-----------------|
| Debian | Supported | apt |
| Fedora | Supported | dnf |
| Archlinux | Supported | pacman |

## Distribution Detection

[VERIFIED] Distribution detection uses Ansible's built-in fact gathering system. The playbook sets `gather_facts: true`, which populates `ansible_facts['distribution']` with the distribution name.

Roles use this fact to select the appropriate package names from distribution-specific mappings.

## Package Mappings

### Neovim Role

[VERIFIED] Defined in `playbooks/roles/features/nvim/vars/main.yml`:

```yaml
nvim_packages_map:
  Debian: [neovim]
  Fedora: [neovim]
  Archlinux: [neovim]
```

The role installs packages using:

```yaml
ansible.builtin.package:
  name: "{{ nvim_packages_map.get(ansible_facts['distribution'], []) }}"
  state: present
```

This retrieves the package list for the detected distribution, or an empty list if the distribution is not in the mapping.

## Adding Distribution Support

To add support for a new distribution:

1. Identify the package names for that distribution
2. Add the distribution and package names to the appropriate role's `vars/main.yml`
3. Test on the target distribution

Example for adding Ubuntu support to the nvim role:

```yaml
nvim_packages_map:
  Debian: [neovim]
  Ubuntu: [neovim]  # Add this line
  Fedora: [neovim]
  Archlinux: [neovim]
```

See [Adding Distribution Support Guide](../guides/adding-distribution-support.md) for detailed instructions.

## Distribution-Specific Notes

### Debian

- Uses APT package manager
- Package names typically match upstream project names

### Fedora

- Uses DNF package manager
- Package names typically match upstream project names

### Archlinux

- Uses Pacman package manager
- Package names typically match upstream project names
- Official repositories provide recent versions

## Unsupported Distributions

If a distribution is not listed in the package mapping, the `get()` method returns an empty list `[]`, and no packages will be installed. The playbook will not fail, but the role will effectively do nothing.

To verify which distribution Ansible detects on your system:

```bash
ansible localhost -m setup -a "filter=ansible_distribution"
```
