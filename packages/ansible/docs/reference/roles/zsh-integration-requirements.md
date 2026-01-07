# Complete Zsh Integration Requirements

This document outlines all the missing components needed for a complete and fully-functional zsh shell integration using Ansible. The current `zsh` role provides the shell installation and basic configuration, but depends on several external components for a complete development environment.

## Overview

The current zsh role (`playbooks/roles/base/zsh/`) requires the following components to be fully functional:

| Component | Status | Priority | Purpose |
|-----------|--------|----------|---------|
| Oh My Zsh | ❌ Missing | REQUIRED | Zsh framework and plugin management |
| Starship | ❌ Missing | REQUIRED | Modern shell prompt |
| NVM (Node Version Manager) | ❌ Missing | REQUIRED | Node.js version management |
| Pyenv | ❌ Missing | OPTIONAL | Python version management (conditional) |
| Themes/Color Sequences | ❌ Missing | REQUIRED | Dynamic terminal color theme integration |
| Color Scheme Generator | ✅ Implemented | OPTIONAL | Generate color schemes (wallust/pywal) |
| Wallpaper Effects Generator | ✅ Implemented | OPTIONAL | Generate wallpaper with color effects |

## Dependency Analysis

### Required for Core Functionality

#### 1. Oh My Zsh (Required)
**Current Status:** Referenced in `.zshrc.j2` template but role doesn't exist

**Template Reference:**
- Line 4: `export ZSH="{{OH_MY_ZSH_DIR}}"`
- Line 7: `source $ZSH/oh-my-zsh.sh`
- Default location: `~/.oh-my-zsh`

**What it does:**
- Provides zsh framework with plugin system
- Manages zsh themes and configurations
- Enables plugin loading (syntax-highlighting, autosuggestions, etc.)

**Required Role Functionality:**
- Clone Oh My Zsh repository from GitHub
- Set proper permissions
- Support custom installation directory via `OH_MY_ZSH_DIR`
- Handle distribution-specific dependencies

**Proposed Variables:**
```yaml
# defaults/main.yml
oh_my_zsh_install_dest: "{{ home_root }}/.oh-my-zsh"
oh_my_zsh_repo_url: "https://github.com/ohmyzsh/ohmyzsh"
oh_my_zsh_repo_version: "master"
OH_MY_ZSH_DIR: "{{ oh_my_zsh_install_dest }}"
```

---

#### 2. Starship (Required)
**Current Status:** Referenced in `.zshrc.j2` template but role doesn't exist

**Template Reference:**
- Line 2: `export STARSHIP_CONFIG="{{STARSHIP_CONFIG}}"`
- Line 10: `eval "$(starship init zsh)"`
- Config location: `${XDG_CONFIG_HOME}/starship/starship.toml` (e.g., `~/.config/starship/starship.toml`)

**What it does:**
- Modern, customizable shell prompt
- Shows git status, context, execution time
- Highly configurable via TOML config file
- Replaces traditional PS1 prompts

**Required Role Functionality:**
- Install starship binary (via package manager or pre-built binary)
- Create config directory structure
- Provide default starship configuration template
- Support distribution-specific installation methods:
  - Fedora/Arch: package manager
  - Debian: pre-built binary or cargo
- Initialize starship in zsh rc file

**Proposed Variables:**
```yaml
# defaults/main.yml
starship_install_method: "package"  # or "binary" for pre-built
starship_config_dest: "{{ xdg_config_home }}/starship/starship.toml"
starship_config_src: "{{ config_files_root }}/starship/starship.toml"
STARSHIP_CONFIG: "{{ starship_config_dest }}"
```

---

#### 3. NVM - Node Version Manager (Required)
**Current Status:** Referenced in `.zshrc.j2` template but role doesn't exist

**Template Reference:**
- Lines 57-64: NVM initialization
- Default installation: `~/.nvm`
- Sources `$NVM_DIR/nvm.sh` and bash completion

**What it does:**
- Manages multiple Node.js versions
- Allows switching between versions per-project
- Essential for modern JavaScript development
- Provides npm and Node.js command availability

**Required Role Functionality:**
- Clone NVM repository from GitHub
- Install NVM initialization script
- Set proper directory permissions
- Handle shell integration (sourcing nvm.sh)
- Support custom NVM directory via environment variable

**Proposed Variables:**
```yaml
# defaults/main.yml
nvm_install_dest: "{{ home_root }}/.nvm"
nvm_repo_url: "https://github.com/nvm-sh/nvm"
nvm_repo_version: "v0.39.0"  # or latest tag
NVM_DIR: "{{ nvm_install_dest }}"
```

---

### Optional Components

#### 4. Pyenv (Optional)
**Current Status:** Partially integrated, conditional support exists

**Template Reference:**
- Lines 67-79: Conditional pyenv initialization
- Enabled when `PYENV_CONFIGURED: true`
- Default location: `~/.pyenv`

**What it does:**
- Manages multiple Python versions
- Per-project Python version switching
- Essential for Python development
- Provides pyenv shim commands

**Current Integration:**
- Already has template support with conditional block
- Already has defaults in zsh role
- Just needs a dedicated role to install

**Proposed Variables:**
```yaml
# defaults/main.yml
pyenv_install_dest: "{{ home_root }}/.pyenv"
pyenv_repo_url: "https://github.com/pyenv/pyenv"
pyenv_repo_version: "master"
pyenv_build_dependencies: true  # Install build tools
PYENV_CONFIGURED: true  # Enable in zsh template
PYENV_DIR: "{{ pyenv_install_dest }}"
```

---

### Integration Components

#### 5. Themes/Color Sequences (Required)
**Current Status:** Referenced in `.zshrc.j2` template but no role to generate it

**Template Reference:**
- Line 19: `(cat "{{COLOR_SCHEME_SEQUENCES_FILE}}" &)`
- Expected location: `${XDG_DATA_HOME}/themes/sequences` (e.g., `~/.local/share/themes/sequences`)
- File format: Shell color escape sequences (ANSI codes)

**What it does:**
- Dynamically applies terminal color schemes at shell startup
- Integrates with color-scheme-generator for consistent theming
- Applies to all terminal windows

**Current Status:**
- Color scheme generator can CREATE these sequences
- But we need a base/default themes role to initialize the directory and provide defaults
- Then color-scheme-generator can update it dynamically

**Proposed Variables:**
```yaml
# defaults/main.yml
themes_install_dest: "{{ xdg_data_home }}/themes"
themes_sequences_file: "{{ themes_install_dest }}/sequences"
COLOR_SCHEME_SEQUENCES_FILE: "{{ themes_sequences_file }}"
```

**Proposed Role Functionality:**
- Create themes directory structure
- Generate default color sequences file
- Can use a default color scheme (e.g., system colors)
- color-scheme-generator role can override this later

---

## Implementation Order

### Phase 1: Core Shell Foundation (Must complete first)
1. **Oh My Zsh Role** - Required for plugin system
   - Dependency for: zsh plugins, theme system
2. **Starship Role** - Required for prompt
   - Dependency for: shell prompt display
3. **NVM Role** - Required for Node development
   - Independent of others

### Phase 2: Python & Themes (Can run parallel to Phase 1 Part B)
4. **Pyenv Role** - Optional for Python development
   - Independent, conditional
5. **Themes Role** - Required for color scheme integration
   - Must complete before color-scheme-generator can work properly

### Phase 3: Already Implemented
6. **Color Scheme Generator** - ✅ Done
   - Updates color schemes (requires Themes role from Phase 2)
7. **Wallpaper Effects Generator** - ✅ Done
   - Generates wallpapers with color effects

## Proposed Role Implementations

### Role: `oh-my-zsh`
**Location:** `playbooks/roles/base/oh-my-zsh/`

**Files:**
- `defaults/main.yml` - Configuration defaults
- `tasks/main.yml` - Installation and setup
- No vars needed (simple installation)

**Tasks:**
1. Clone Oh My Zsh repository
2. Set directory permissions (755)
3. Create necessary subdirectories
4. Report installation status

---

### Role: `starship`
**Location:** `playbooks/roles/base/starship/`

**Files:**
- `defaults/main.yml` - Configuration defaults
- `tasks/main.yml` - Installation and setup
- `templates/starship.toml.j2` - Default starship config template
- `vars/main.yml` - Distribution-specific install methods

**Tasks:**
1. Install starship binary (distro-specific method)
2. Create config directory
3. Render starship.toml template
4. Verify installation with `starship --version`

**Distribution-specific Installation:**
```yaml
# Arch Linux: pacman -S starship
# Fedora: dnf install starship
# Debian/Ubuntu: cargo install starship (or pre-built binary)
```

---

### Role: `nvm`
**Location:** `playbooks/roles/base/nvm/`

**Files:**
- `defaults/main.yml` - Configuration defaults
- `tasks/main.yml` - Installation and setup

**Tasks:**
1. Create NVM directory
2. Clone NVM repository
3. Set proper permissions
4. Source nvm.sh in zsh rc (already integrated in .zshrc.j2)
5. Verify installation

---

### Role: `pyenv`
**Location:** `playbooks/roles/base/pyenv/`

**Files:**
- `defaults/main.yml` - Configuration defaults
- `tasks/main.yml` - Installation and setup
- `vars/main.yml` - Distribution-specific build dependencies

**Tasks:**
1. Install build dependencies (distro-specific)
2. Create pyenv directory
3. Clone pyenv repository
4. Clone pyenv-virtualenv plugin
5. Set proper permissions
6. Source pyenv init in zsh rc (already integrated in .zshrc.j2)
7. Verify installation

---

### Role: `themes`
**Location:** `playbooks/roles/base/themes/`

**Files:**
- `defaults/main.yml` - Configuration defaults
- `tasks/main.yml` - Installation and setup
- `templates/sequences.j2` - Default color sequences template

**Tasks:**
1. Create themes directory structure
2. Generate default color sequences file
3. Set proper permissions
4. Provide hook for color-scheme-generator to update

---

## Integration Points

### With Existing zsh Role
The `zsh` role already has template variables for all these components. Update `defaults/main.yml`:

```yaml
# These are set by each component role
OH_MY_ZSH_DIR: "{{ home_root }}/.oh-my-zsh"
STARSHIP_CONFIG: "{{ xdg_config_home }}/starship/starship.toml"
NVM_DIR: "{{ home_root }}/.nvm"
PYENV_CONFIGURED: false  # Enable when pyenv role is included
PYENV_DIR: "{{ home_root }}/.pyenv"
COLOR_SCHEME_SEQUENCES_FILE: "{{ xdg_data_home }}/themes/sequences"
COLOR_SCHEME_BIN_DIR: ""  # Set by color-scheme-generator role
WALLPAPER_EFFECTS_BIN_DIR: ""  # Set by wallpaper-effects-generator role
```

### With bootstrap.yml
Add tags for each role:

```yaml
- name: Install and configure Oh My Zsh
  ansible.builtin.include_role:
    name: oh-my-zsh
  tags: [oh-my-zsh, never]

- name: Install and configure Starship
  ansible.builtin.include_role:
    name: starship
  tags: [starship, never]

- name: Install and configure NVM
  ansible.builtin.include_role:
    name: nvm
  tags: [nvm, never]

- name: Install and configure Pyenv
  ansible.builtin.include_role:
    name: pyenv
  tags: [pyenv, never]

- name: Install and configure Themes
  ansible.builtin.include_role:
    name: themes
  tags: [themes, never]
```

---

## Installation Command

Once all roles are implemented, the complete zsh environment can be installed with:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
ansible-playbook \
  -i ./inventory/localhost.yml \
  ./playbooks/bootstrap.yml \
  --tags zsh,oh-my-zsh,starship,nvm,pyenv,themes,color-scheme-generator,wallpaper-effects-generator \
  --ask-become-pass
```

Or to install without optional components:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
ansible-playbook \
  -i ./inventory/localhost.yml \
  ./playbooks/bootstrap.yml \
  --tags zsh,oh-my-zsh,starship,nvm,themes,color-scheme-generator \
  --ask-become-pass
```

---

## Dependencies Graph

```
zsh (base)
├── oh-my-zsh (required)
│   └── plugins system
├── starship (required)
│   └── prompt display
├── nvm (required)
│   └── node version management
├── pyenv (optional)
│   └── python version management
├── themes (required)
│   ├── color-scheme-generator (optional)
│   │   └── dynamically generate color schemes
│   └── wallpaper-effects-generator (optional)
│       └── generate wallpapers with themes
└── xdg directories (required base)
    └── config, data, cache directories
```

---

## Summary

**Total new roles needed:** 5
- 3 REQUIRED for functional zsh: oh-my-zsh, starship, nvm, themes
- 1 OPTIONAL: pyenv (for Python development)
- 2 ALREADY IMPLEMENTED: color-scheme-generator, wallpaper-effects-generator

**Complexity:** Low to Medium
- Simple git clones and directory setup
- Mostly template rendering and permission handling
- No complex orchestration like color-scheme-generator or wallpaper-effects-generator

**Estimated scope:** Each role is ~50-100 lines of YAML, similar to what we've already done with the two generator roles
