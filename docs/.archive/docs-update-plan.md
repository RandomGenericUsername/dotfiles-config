# Ansible Zsh Role Implementation Plan

## Overview

Add a zsh role to `playbooks/roles/base/zsh/` as a fundamental shell configuration. The existing template at `config-files/zsh/.zshrc.j2` will be rendered using Ansible's `template` module with distribution-specific plugin paths.

**Source of Truth:** Distribution-specific configurations from `/tmp/config/packages/{distro}/system.toml`

---

## Distribution-Specific Plugin Paths

| Plugin | Archlinux | Debian | Fedora |
|--------|-----------|--------|--------|
| syntax_highlighting | `/usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh` | `/usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh` | `/usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh` |
| autosuggestions | `/usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh` | `/usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh` | `/usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh` |
| history_substring_search | `/usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh` | *(unavailable)* | *(unavailable)* |
| fzf_key_bindings | `/usr/share/fzf/key-bindings.zsh` | `/usr/share/doc/fzf/examples/key-bindings.zsh` | `/usr/share/fzf/shell/key-bindings.zsh` |
| fzf_completion | `/usr/share/fzf/completion.zsh` | `/usr/share/doc/fzf/examples/completion.zsh` | *(unavailable)* |

---

## Files to Create

```
packages/ansible/playbooks/roles/base/zsh/
├── defaults/main.yml      # Default template variables
├── vars/main.yml          # Distribution package mappings & plugin paths
└── tasks/main.yml         # Installation and template rendering
```

---

## File Contents

### 1. `defaults/main.yml` - Template Variables with Defaults

```yaml
# Destination paths
zsh_config_dest: "{{ home_root }}/.zshrc"
zsh_template_src: "{{ config_files_root }}/zsh/.zshrc.j2"

# Whether to use distribution-specific plugin paths (set to false to use custom paths)
zsh_use_distro_paths: true

# Required template variables
STARSHIP_CONFIG: "{{ xdg_config_home }}/starship/starship.toml"
OH_MY_ZSH_DIR: "{{ home_root }}/.oh-my-zsh"
COLOR_SCHEME_SEQUENCES_FILE: "{{ xdg_data_home }}/themes/sequences"
NVM_DIR: "{{ home_root }}/.nvm"

# Optional plugin paths (overridden by distro-specific values when zsh_use_distro_paths is true)
ZSH_SYNTAX_HIGHLIGHTING: ""
ZSH_AUTOSUGGESTIONS: ""
ZSH_HISTORY_SUBSTRING_SEARCH: ""
FZF_KEY_BINDINGS: ""
FZF_COMPLETION: ""

# Pyenv configuration (disabled by default)
PYENV_CONFIGURED: false
PYENV_DIR: "{{ home_root }}/.pyenv"
```

### 2. `vars/main.yml` - Package Mappings & Distribution-Specific Paths

```yaml
# Distribution-specific package names
zsh_packages_map:
  Archlinux:
    - zsh
    - zsh-syntax-highlighting
    - zsh-autosuggestions
    - zsh-history-substring-search
    - fzf
    - exa
    - bat
  Debian:
    - zsh
    - zsh-syntax-highlighting
    - zsh-autosuggestions
    # Note: zsh-history-substring-search not in default repos
    - fzf
    - exa
    - bat
  Fedora:
    - zsh
    - zsh-syntax-highlighting
    - zsh-autosuggestions
    # Note: zsh-history-substring-search may need EPEL
    - fzf
    - exa
    - bat

# Distribution-specific plugin paths (from /tmp/config/packages/{distro}/system.toml)
zsh_plugin_paths_map:
  Archlinux:
    syntax_highlighting: "/usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
    autosuggestions: "/usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
    history_substring_search: "/usr/share/zsh/plugins/zsh-history-substring-search/zsh-history-substring-search.zsh"
    fzf_key_bindings: "/usr/share/fzf/key-bindings.zsh"
    fzf_completion: "/usr/share/fzf/completion.zsh"
  Debian:
    syntax_highlighting: "/usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
    autosuggestions: "/usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
    history_substring_search: ""  # Not available in default repos
    fzf_key_bindings: "/usr/share/doc/fzf/examples/key-bindings.zsh"
    fzf_completion: "/usr/share/doc/fzf/examples/completion.zsh"
  Fedora:
    syntax_highlighting: "/usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
    autosuggestions: "/usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
    history_substring_search: ""  # Not available in default repos
    fzf_key_bindings: "/usr/share/fzf/shell/key-bindings.zsh"
    fzf_completion: ""  # Not included in Fedora's fzf package
```

### 3. `tasks/main.yml` - Installation and Template Rendering

```yaml
- name: Install zsh and related packages
  become: true
  ansible.builtin.package:
    name: "{{ zsh_packages_map.get(ansible_facts['distribution'], []) }}"
    state: present

- name: Set distribution-specific plugin paths
  ansible.builtin.set_fact:
    ZSH_SYNTAX_HIGHLIGHTING: "{{ zsh_plugin_paths_map.get(ansible_facts['distribution'], {}).get('syntax_highlighting', '') }}"
    ZSH_AUTOSUGGESTIONS: "{{ zsh_plugin_paths_map.get(ansible_facts['distribution'], {}).get('autosuggestions', '') }}"
    ZSH_HISTORY_SUBSTRING_SEARCH: "{{ zsh_plugin_paths_map.get(ansible_facts['distribution'], {}).get('history_substring_search', '') }}"
    FZF_KEY_BINDINGS: "{{ zsh_plugin_paths_map.get(ansible_facts['distribution'], {}).get('fzf_key_bindings', '') }}"
    FZF_COMPLETION: "{{ zsh_plugin_paths_map.get(ansible_facts['distribution'], {}).get('fzf_completion', '') }}"
  when: zsh_use_distro_paths | default(true)

- name: Render .zshrc from template
  ansible.builtin.template:
    src: "{{ zsh_template_src }}"
    dest: "{{ zsh_config_dest }}"
    mode: "0644"
    backup: true
```

---

## Playbook Updates

### Update `playbooks/bootstrap.yml`

Add the zsh role and update the help message:

```yaml
- name: Dotfiles engine (local)
  hosts: localhost
  gather_facts: true

  pre_tasks:
    - name: Show available tags
      ansible.builtin.debug:
        msg:
          - "No tags specified. Available tags:"
          - "  --tags zsh      : Install and configure Zsh shell"
          - "  --tags nvim     : Install and configure Neovim"
          - "  --tags debug    : Show debug information"
          - ""
          - "Example: ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass"

    - name: Debug paths
      ansible.builtin.debug:
        msg:
          - "playbook_dir={{ playbook_dir }}"
          - "dotfiles_root={{ dotfiles_root | default('UNDEFINED') }}"
          - "config_files_root={{ config_files_root | default('UNDEFINED') }}"
      tags: [debug]

  roles:
    - role: zsh
      tags: [zsh, never]
    - role: nvim
      tags: [nvim, never]
```

---

## Documentation Updates

### Files to Update

| File | Action |
|------|--------|
| `docs/reference/tags.md` | Add `zsh` tag entry |
| `docs/reference/roles/base/index.md` | Add zsh role reference |
| `docs/architecture/roles-organization.md` | Update to note zsh as first base role |

### New File: `docs/reference/roles/base/zsh.md`

```markdown
# Zsh Role

Installs and configures the Zsh shell with plugins and custom configuration.

## Tags

- `zsh`: Install and configure Zsh

## Variables

### Defaults (`defaults/main.yml`)

| Variable | Default | Description |
|----------|---------|-------------|
| `zsh_config_dest` | `{{ home_root }}/.zshrc` | Destination path for .zshrc |
| `zsh_template_src` | `{{ config_files_root }}/zsh/.zshrc.j2` | Source template path |
| `zsh_use_distro_paths` | `true` | Use distribution-specific plugin paths |
| `STARSHIP_CONFIG` | `{{ xdg_config_home }}/starship/starship.toml` | Starship config path |
| `OH_MY_ZSH_DIR` | `{{ home_root }}/.oh-my-zsh` | Oh My Zsh installation path |
| `COLOR_SCHEME_SEQUENCES_FILE` | `{{ xdg_data_home }}/themes/sequences` | Color scheme sequences file |
| `NVM_DIR` | `{{ home_root }}/.nvm` | NVM installation path |
| `PYENV_CONFIGURED` | `false` | Enable pyenv configuration |
| `PYENV_DIR` | `{{ home_root }}/.pyenv` | Pyenv installation path |

### Distribution Package Mappings

Packages installed per distribution:

- **Archlinux**: zsh, zsh-syntax-highlighting, zsh-autosuggestions, zsh-history-substring-search, fzf, exa, bat
- **Debian**: zsh, zsh-syntax-highlighting, zsh-autosuggestions, fzf, exa, bat
- **Fedora**: zsh, zsh-syntax-highlighting, zsh-autosuggestions, fzf, exa, bat

## Usage

```bash
# Basic installation
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass

# Override template variables
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass \
  -e "OH_MY_ZSH_DIR={{ home_root }}/.config/oh-my-zsh" \
  -e "PYENV_CONFIGURED=true"

# Use custom plugin paths
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass \
  -e "zsh_use_distro_paths=false" \
  -e "ZSH_SYNTAX_HIGHLIGHTING=/custom/path/syntax.zsh"
```

## Template

The role renders `config-files/zsh/.zshrc.j2` which includes:

- Starship prompt initialization
- Oh My Zsh sourcing
- Plugin loading (syntax highlighting, autosuggestions, history search, fzf)
- Aliases for exa and bat
- NVM and Pyenv configuration (optional)
```

---

## Usage Examples

```bash
# Install zsh with auto-detected distro paths
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass

# Override template variables
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass \
  -e "OH_MY_ZSH_DIR={{ home_root }}/.config/oh-my-zsh" \
  -e "PYENV_CONFIGURED=true"

# Use custom plugin paths instead of distro defaults
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh --ask-become-pass \
  -e "zsh_use_distro_paths=false" \
  -e "ZSH_SYNTAX_HIGHLIGHTING=/custom/path/syntax.zsh"

# Install both zsh and nvim
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags zsh,nvim --ask-become-pass
```

---

## Implementation Checklist

- [ ] Create `playbooks/roles/base/zsh/defaults/main.yml`
- [ ] Create `playbooks/roles/base/zsh/vars/main.yml`
- [ ] Create `playbooks/roles/base/zsh/tasks/main.yml`
- [ ] Update `playbooks/bootstrap.yml` with zsh role
- [ ] Update `docs/reference/tags.md`
- [ ] Create `docs/reference/roles/base/zsh.md`
- [ ] Update `docs/architecture/roles-organization.md`
- [ ] Test on Archlinux
- [ ] Test on Debian (if available)
- [ ] Test on Fedora (if available)
