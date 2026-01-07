# Tags Reference

This document lists all available tags for selective playbook execution.

## Available Tags

[VERIFIED] The following tags are available in the playbook (verified via `ansible-playbook --list-tags`):

| Tag | Description | Associated Roles/Tasks |
|-----|-------------|------------------------|
| `debug` | Debug information tasks | Pre-task that displays path variables |
| `nvim` | Neovim installation and configuration | All tasks in the nvim role (requires explicit tag) |
| `never` | Special tag to skip by default | Tasks tagged with `never` only run when explicitly requested |

## Using Tags

Tags allow you to run specific parts of the playbook without executing everything.

### Run Specific Tags

Execute only tasks tagged with `nvim`:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

Execute only debug tasks:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug
```

### Run Multiple Tags

Execute multiple tags by separating them with commas:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags debug,nvim
```

### Skip Tags

Skip specific tags using `--skip-tags`:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --skip-tags debug
```

### List All Tags

To see all available tags without running the playbook:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --list-tags
```

## Tag Details

### `debug` Tag

[VERIFIED] Applied to the "Debug paths" pre-task in `playbooks/bootstrap.yml`.

Displays:
- `playbook_dir`: Directory containing the playbook
- `dotfiles_root`: Root of the dotfiles repository
- `config_files_root`: Configuration files directory

Useful for troubleshooting path-related issues.

### `nvim` Tag

[VERIFIED] Applied to the nvim role in `playbooks/bootstrap.yml`.

**Note**: This role is tagged with `[nvim, never]`, meaning it will **only** run when explicitly requested with `--tags nvim`. It will not run when no tags are specified.

Executes all tasks in the nvim role:
1. Install neovim package
2. Ensure destination directory exists
3. Copy Neovim config directory

### `never` Tag

Special Ansible tag that prevents tasks from running by default. Tasks tagged with `never` only execute when:
- Their specific tag is requested (e.g., `--tags nvim`)
- The `--tags never` is explicitly used (not recommended)

This is used for optional features that should opt-in rather than opt-out.

## Best Practices

1. **Selective Installation**: Use tags to install only the software you need
2. **Debugging**: Use the `debug` tag to verify paths before running installation tasks
3. **Testing**: Test individual roles using their specific tags before running the full playbook
4. **CI/CD**: Use tags in automated environments to control which roles execute

## Examples

See [Selective Install Examples](../examples/selective-install.md) for more usage examples.
