# Adding a Role

This guide walks you through creating a new role to install and configure additional software.

## Overview

[VERIFIED] Roles follow a standard structure based on the existing nvim role:

```text
role_name/
├── defaults/
│   └── main.yml      # Default variables
├── vars/
│   └── main.yml      # Role-specific variables
└── tasks/
    └── main.yml      # Tasks to execute
```

## Step-by-Step Guide

### 1. Choose Role Category

Decide whether your role belongs in:
- `playbooks/roles/base/`: Fundamental system configuration
- `playbooks/roles/features/`: Feature-specific software

Most software installation roles belong in `features/`.

### 2. Create Role Directory

Create the role directory structure:

```bash
cd playbooks/roles/features  # or base/
mkdir -p my_role/{defaults,vars,tasks}
```

### 3. Define Default Variables

Create `defaults/main.yml` with default variable values:

[VERIFIED] Example based on nvim role:

```yaml
# defaults/main.yml
my_role_config_dest: "{{ xdg_config_home }}/my_app"
my_role_config_src_dir: "{{ config_files_root }}/my_app"
```

**Guidelines**:
- Use descriptive variable names prefixed with the role name
- Reference global variables for paths
- Provide sensible defaults that work in most cases
- These variables have lowest precedence and can be easily overridden

### 4. Define Distribution Package Mappings

Create `vars/main.yml` with distribution-specific package names:

[VERIFIED] Example based on nvim role:

```yaml
# vars/main.yml
my_role_packages_map:
  Debian: [package-name-debian]
  Fedora: [package-name-fedora]
  Archlinux: [package-name-arch]
```

**Guidelines**:
- Map each supported distribution to its package names
- Use exact package names from each distribution's repositories
- List can contain multiple packages if needed
- Verify package names on each distribution before adding

### 5. Define Tasks

Create `tasks/main.yml` with the tasks to execute:

[VERIFIED] Example based on nvim role structure:

```yaml
# tasks/main.yml
- name: Install my_app packages
  become: true
  ansible.builtin.package:
    name: "{{ my_role_packages_map.get(ansible_facts['distribution'], []) }}"
    state: present

- name: Ensure destination directory exists
  ansible.builtin.file:
    path: "{{ my_role_config_dest }}"
    state: directory
    mode: "0755"

- name: Copy my_app config directory
  ansible.builtin.copy:
    src: "{{ my_role_config_src_dir }}/"
    dest: "{{ my_role_config_dest }}/"
    mode: preserve
```

**Guidelines**:
- Use descriptive task names
- Use `become: true` for tasks requiring root privileges
- Use `ansible.builtin.*` modules for better compatibility
- Handle missing distributions gracefully with `.get()`
- Ensure idempotency (tasks can be run multiple times safely)

### 6. Add Role to Playbook

Edit `playbooks/bootstrap.yml` to include your role:

```yaml
roles:
  - role: nvim
    tags: [nvim]
  - role: my_role      # Add this
    tags: [my_role]    # Add this
```

**Guidelines**:
- Choose a descriptive tag name
- Tag name typically matches role name
- Tags enable selective execution

### 7. Test the Role

Test your role before committing:

```bash
# Check syntax
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check

# List tasks to verify it appears
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tasks

# Run in check mode (dry run)
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags my_role --check

# Actually run the role
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags my_role --ask-become-pass
```

### 8. Test on Multiple Distributions

If possible, test on all supported distributions:

```bash
# On Debian/Ubuntu
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags my_role --ask-become-pass

# On Fedora
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags my_role --ask-become-pass

# On Archlinux
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags my_role --ask-become-pass
```

## Common Patterns

### Package Installation Only

If you only need to install packages without configuration:

```yaml
# tasks/main.yml
- name: Install packages
  become: true
  ansible.builtin.package:
    name: "{{ my_role_packages_map.get(ansible_facts['distribution'], []) }}"
    state: present
```

### Configuration Only

If you only need to copy configuration files:

```yaml
# tasks/main.yml
- name: Ensure destination directory exists
  ansible.builtin.file:
    path: "{{ my_role_config_dest }}"
    state: directory
    mode: "0755"

- name: Copy configuration
  ansible.builtin.copy:
    src: "{{ my_role_config_src_dir }}/"
    dest: "{{ my_role_config_dest }}/"
    mode: preserve
```

### Multiple Configuration Locations

If your software has multiple config locations:

```yaml
# defaults/main.yml
my_role_config_dest: "{{ xdg_config_home }}/my_app"
my_role_data_dest: "{{ xdg_data_home }}/my_app"

# tasks/main.yml
- name: Copy config files
  ansible.builtin.copy:
    src: "{{ config_files_root }}/my_app/config/"
    dest: "{{ my_role_config_dest }}/"
    mode: preserve

- name: Copy data files
  ansible.builtin.copy:
    src: "{{ config_files_root }}/my_app/data/"
    dest: "{{ my_role_data_dest }}/"
    mode: preserve
```

## Best Practices

1. **Variable naming**: Prefix all role variables with the role name to avoid conflicts
2. **Idempotency**: Ensure tasks can be run multiple times without issues
3. **Distribution support**: Test on all distributions you claim to support
4. **Error handling**: Use `.get()` with default values for graceful fallbacks
5. **Documentation**: Add inline comments explaining non-obvious configurations
6. **File modes**: Use explicit file modes for security
7. **Privilege escalation**: Only use `become: true` where necessary

## See Also

- [Roles Organization](../architecture/roles-organization.md): Architecture details
- [Adding Distribution Support](adding-distribution-support.md): Supporting new distributions
- [Neovim Role Documentation](../reference/roles/features/nvim.md): Complete role example
