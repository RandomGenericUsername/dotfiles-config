# Available Tags

Reference documentation for Ansible tags used in the dotfiles configuration.

## Base Tags

Tags for foundational system components.

### zsh

Install and configure the Zsh shell with plugins and custom configuration.

**Command:**
```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass
```

**What it does:**
- Installs zsh and related packages (distribution-specific)
- Configures distribution-specific plugin paths
- Renders `.zshrc` from template

**See:** [Zsh Role](roles/base/zsh.md)

## Feature Tags

Tags for optional features and configurations.

### nvim

Install and configure Neovim.

**Command:**
```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim --ask-become-pass
```

**See:** Neovim role documentation (coming soon)

## Utility Tags

Tags for debugging and development.

### debug

Show debug information about paths and configuration.

**Command:**
```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug
```

## Combining Tags

You can combine multiple tags to install multiple components:

```bash
# Install both zsh and nvim
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh,nvim --ask-become-pass
```

## Tag Behavior

- Tags with `never` modifier require explicit selection (they won't run with `--tags`)
- All base and feature tags use the `never` modifier to prevent accidental execution
- Use `--ask-become-pass` when tags require elevated privileges
