# Installation

This guide covers installing Ansible and verifying your setup.

## Installing Ansible

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install ansible
```

### Fedora

```bash
sudo dnf install ansible
```

### Archlinux

```bash
sudo pacman -S ansible
```

### Using pip

For the latest version, install via pip:

```bash
pip install --user ansible
```

Or system-wide:

```bash
sudo pip install ansible
```

### Official Documentation

For other installation methods, refer to the official Ansible documentation:
https://docs.ansible.com/ansible/latest/installation_guide/index.html

## Verify Installation

After installation, verify Ansible is working:

```bash
ansible --version
```

Expected output should include:
- ansible-core 2.20+
- Python version 3.x
- Jinja2 and PyYAML versions

[VERIFIED] Example output:
```
ansible [core 2.20.1]
  config file = /home/inumaki/Development/newDev/v2.0/dotfiles/config/packages/ansible/ansible.cfg
  configured module search path = ['/home/inumaki/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.13/site-packages/ansible
  ansible collection location = /home/inumaki/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.13.11 (main, Dec  7 2025, 13:01:45) [GCC 15.2.1 20251112] (/usr/bin/python)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
```

## Verify Playbook Setup

Check that the playbook syntax is valid:

```bash
cd /path/to/dotfiles/config/packages/ansible
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --syntax-check
```

Expected output:
```
playbook: playbooks/bootstrap.yml
```

If the syntax check passes, your setup is ready.

## Test Connection

Verify Ansible can connect to localhost:

```bash
ansible localhost -m ping
```

Expected output:
```json
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

## Configuration Verification

List all tasks to verify the playbook is configured correctly:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tasks
```

List all available tags:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags
```

## Troubleshooting

### Ansible Not Found

If `ansible` command is not found after installation:

1. Check if it's installed in a non-standard location:
   ```bash
   which ansible
   ```

2. If installed via pip with `--user`, ensure `~/.local/bin` is in your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. Restart your shell or reload configuration

### Python Version Mismatch

If Ansible uses Python 2.x instead of Python 3:

1. Specify Python 3 explicitly when running playbooks:
   ```bash
   ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
     -e ansible_python_interpreter=/usr/bin/python3
   ```

2. Or update the inventory file `inventory/localhost.yml` with the correct path

### Permission Issues

If you can't install Ansible system-wide:

1. Use the `--user` flag with pip:
   ```bash
   pip install --user ansible
   ```

2. Or use a Python virtual environment

## Next Steps

Once Ansible is installed and verified:

1. Review [Prerequisites](prerequisites.md) to ensure all requirements are met
2. Follow the [Quick Start Guide](index.md) to run your first playbook
3. Check [Examples](../examples/index.md) for common usage patterns
