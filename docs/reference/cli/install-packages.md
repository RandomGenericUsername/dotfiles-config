# install-packages

[VERIFIED via CLI - 2026-01-03]

Install packages using Ansible playbook.

## Synopsis

```bash
config install-packages [OPTIONS]
```

## Description

Executes the Ansible bootstrap playbook located at `packages/ansible/playbooks/bootstrap.yml` to install and configure system packages.

The command runs Ansible from the `packages/ansible` directory and forwards all specified options and arguments to the underlying `ansible-playbook` command.

## Options

| Option | Type | Description |
|--------|------|-------------|
| `--tags TEXT` | Optional | Ansible tags to run (comma-separated for multiple tags) |
| `--help` | Flag | Show this message and exit |

## Additional Arguments

All additional command-line arguments are forwarded directly to `ansible-playbook`. This enables use of any standard Ansible options such as:

- `--ask-become-pass` - Prompt for privilege escalation password
- `-e KEY=VALUE` - Set Ansible variables
- `-v`, `-vv`, `-vvv` - Increase verbosity

## Examples

Run the entire playbook:

```bash
config install-packages --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

Run with specific tags:

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

Run with debug output:

```bash
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

Override Ansible variables:

```bash
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test
```

[VERIFIED via CLI - 2026-01-03]

## Available Tags

[VERIFIED via CLI - 2026-01-03]

- `debug` - Show debug information about paths and configuration
- `nvim` - Install and configure Neovim

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Ansible command not found or execution error |
| Other | Exit code from ansible-playbook |

## Source Code

- Implementation: [src/commands/install_packages.py](../../../src/commands/install_packages.py)
- Playbook: [packages/ansible/playbooks/bootstrap.yml](../../../packages/ansible/playbooks/bootstrap.yml)

## See Also

- [Ansible Package Documentation](../../../packages/ansible/README.md)
