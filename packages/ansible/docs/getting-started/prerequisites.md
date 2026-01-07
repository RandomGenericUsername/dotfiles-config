# Prerequisites

This document lists the requirements for running the ansible package.

## System Requirements

### Operating System

[VERIFIED] Supported Linux distributions:
- Debian
- Fedora
- Archlinux

Other distributions may work but are not officially supported.

### Ansible

[VERIFIED] Ansible core 2.20+ is required.

Current tested version: **ansible-core 2.20.1**

To check your Ansible version:

```bash
ansible --version
```

### Python

[VERIFIED] Python 3 is required at `/usr/bin/python3` (as configured in `inventory/localhost.yml`).

To check your Python version:

```bash
python3 --version
```

The system has been tested with Python 3.13.

### Python Libraries

[VERIFIED] The following Python libraries are required (tested versions):
- Jinja2 3.1.6+
- PyYAML 6.0.3+ (with libyaml)

These are typically installed as dependencies when you install Ansible.

## Permissions

### Root/Sudo Access

[VERIFIED] Root privileges are required for:
- Installing packages (via `become: true` in tasks)

You will need to:
- Have sudo access on the system
- Use `--ask-become-pass` flag when running the playbook
- OR configure passwordless sudo

### File System Access

Standard user permissions are sufficient for:
- Creating directories in your home directory
- Copying configuration files to `~/.config/`
- Reading files from the dotfiles repository

## Directory Requirements

### Source Files

The dotfiles repository must contain:
- Configuration files in `config-files/` directory (or custom path)
- For the nvim role: `config-files/nvim/` must exist

### Destination Paths

[VERIFIED] Default destinations follow XDG Base Directory specification:
- `$XDG_CONFIG_HOME` (defaults to `~/.config`)
- `$XDG_DATA_HOME` (defaults to `~/.local/share`)
- `~/.local/bin` for binaries

These directories will be created automatically if they don't exist.

## Network Requirements

### Package Installation

Internet access is required to:
- Download packages from distribution repositories
- Install software via package managers (apt, dnf, pacman)

### Local Operation

[VERIFIED] The playbook operates locally only:
- Connection type: `local`
- No remote hosts
- No SSH required

## Optional Requirements

### Distribution-Specific

Different package managers may have different requirements:

**Debian/Ubuntu**:
- `apt` must be functional
- Package lists should be updated (`apt update`)

**Fedora**:
- `dnf` must be functional
- Repository configuration should be valid

**Archlinux**:
- `pacman` must be functional
- Package databases should be synced (`pacman -Sy`)

## Verification

Verify your system meets the requirements:

```bash
# Check Ansible version
ansible --version

# Check Python version
python3 --version

# Check sudo access
sudo -v

# Check playbook syntax
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check
```

All commands should complete without errors.

## Next Steps

If your system meets all prerequisites, proceed to [Installation](installation.md) or jump straight to the [Quick Start Guide](index.md).
