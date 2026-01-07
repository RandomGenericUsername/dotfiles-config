# Adding Distribution Support

This guide explains how to add support for new Linux distributions to existing roles.

## Overview

[VERIFIED] Distribution detection uses Ansible's fact gathering system. The playbook sets `gather_facts: true`, which populates `ansible_facts['distribution']` with the distribution name.

Roles use this fact to select appropriate package names from distribution-specific mappings in `vars/main.yml`.

## How Distribution Detection Works

Ansible automatically detects the distribution and provides it via facts:

```yaml
{{ ansible_facts['distribution'] }}
```

Common distribution names:
- `Debian`
- `Ubuntu`
- `Fedora`
- `CentOS`
- `Archlinux`
- `openSUSE`

## Step-by-Step Guide

### 1. Determine Distribution Name

First, determine how Ansible identifies your distribution:

```bash
ansible localhost -m setup -a "filter=ansible_distribution"
```

Example output:
```json
{
    "ansible_facts": {
        "ansible_distribution": "Ubuntu"
    }
}
```

Note the exact capitalization and spelling.

### 2. Find Package Names

Identify the package names for your distribution:

**Debian/Ubuntu**:
```bash
apt search package-name
apt show package-name
```

**Fedora/CentOS**:
```bash
dnf search package-name
dnf info package-name
```

**Archlinux**:
```bash
pacman -Ss package-name
pacman -Si package-name
```

**openSUSE**:
```bash
zypper search package-name
zypper info package-name
```

### 3. Update vars/main.yml

Add the distribution and package names to the role's `vars/main.yml`:

[VERIFIED] Example based on nvim role:

```yaml
# playbooks/roles/features/nvim/vars/main.yml
nvim_packages_map:
  Debian: [neovim]
  Ubuntu: [neovim]       # Add this line
  Fedora: [neovim]
  Archlinux: [neovim]
```

If the package name is different:

```yaml
my_role_packages_map:
  Debian: [package-debian]
  Ubuntu: [package-ubuntu]     # Different name
  Fedora: [package-fedora]
  Archlinux: [package-arch]
```

If multiple packages are needed:

```yaml
my_role_packages_map:
  Debian: [package1, package2]
  Ubuntu: [package1-ubuntu, package2-ubuntu]
  Fedora: [package1-fedora, package2-fedora]
```

### 4. Test on Target Distribution

Test the role on the new distribution:

```bash
# Verify distribution detection
ansible localhost -m setup -a "filter=ansible_distribution"

# Check syntax
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check

# Run in check mode
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags role_tag --check

# Actually run the role
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags role_tag --ask-become-pass
```

### 5. Verify Installation

After running the playbook, verify:

1. Packages are installed:
   ```bash
   # Debian/Ubuntu
   dpkg -l | grep package-name

   # Fedora/CentOS
   rpm -qa | grep package-name

   # Archlinux
   pacman -Q | grep package-name
   ```

2. Configuration files are in place:
   ```bash
   ls -la ~/.config/app-name/
   ```

3. The application works:
   ```bash
   app-name --version
   ```

## Advanced Cases

### Distribution Families

For distributions in the same family with identical package names, you can add them separately:

```yaml
my_role_packages_map:
  Debian: [package-name]
  Ubuntu: [package-name]       # Same as Debian
  LinuxMint: [package-name]    # Same as Debian/Ubuntu
  Fedora: [package-name]
  CentOS: [package-name]       # Same as Fedora
  Archlinux: [package-name]
```

### Version-Specific Packages

If package names vary by version, you may need to add version detection:

```yaml
my_role_packages_map:
  Debian: "{{ 'new-package' if ansible_facts['distribution_major_version']|int >= 12 else 'old-package' }}"
```

However, this is complex. Consider using separate entries or requiring minimum versions.

### Repository Configuration

If packages require additional repositories:

```yaml
- name: Add repository (Debian/Ubuntu)
  become: true
  ansible.builtin.apt_repository:
    repo: ppa:repository/name
  when: ansible_facts['distribution'] in ['Debian', 'Ubuntu']

- name: Install packages
  become: true
  ansible.builtin.package:
    name: "{{ my_role_packages_map.get(ansible_facts['distribution'], []) }}"
    state: present
```

## Testing Strategy

1. **Local Testing**: Test on the target distribution using a VM or container
2. **Check Mode**: Use `--check` to preview changes without making them
3. **Syntax Check**: Always run `--syntax-check` before actual execution
4. **Incremental**: Test one distribution at a time

## Handling Unsupported Distributions

[VERIFIED] The current implementation uses `.get()` with a default empty list:

```yaml
name: "{{ my_role_packages_map.get(ansible_facts['distribution'], []) }}"
```

This means:
- If distribution is not in the mapping, no packages are installed
- The playbook does not fail
- The role effectively skips package installation

To warn users about unsupported distributions:

```yaml
- name: Check distribution support
  ansible.builtin.fail:
    msg: "Distribution {{ ansible_facts['distribution'] }} is not supported"
  when: ansible_facts['distribution'] not in my_role_packages_map.keys()
```

## Documenting Support

After adding support, update documentation:

1. Update [Distribution Support](../reference/distributions.md)
2. Add distribution to the role's documentation
3. Update the main README if applicable

## See Also

- [Distribution Support Reference](../reference/distributions.md): Currently supported distributions
- [Adding a Role](adding-a-role.md): Creating new roles
- [Neovim Role](../reference/roles/features/nvim.md): Example role implementation
