# Feature Roles

Feature roles install and configure specific software packages and their configurations.

## Available Roles

The following feature roles are currently available:

| Role | Tag | Description | Documentation |
|------|-----|-------------|---------------|
| nvim | `nvim` | Neovim text editor installation and configuration | [nvim.md](nvim.md) |
| color-scheme-generator | `color-scheme-generator` | Color palette extraction from wallpapers | [color-scheme-generator.md](color-scheme-generator.md) |
| wallpaper-effects-generator | `wallpaper-effects-generator` | ImageMagick effects for wallpapers | [wallpaper-effects-generator.md](wallpaper-effects-generator.md) |

## Role Location

[VERIFIED] Feature roles are located in `playbooks/roles/features/`.

## Using Feature Roles

Execute a specific feature role using its tag:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags <role-tag>
```

For example:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags nvim
```

## Adding New Feature Roles

To add a new feature role:

1. Create the role directory under `playbooks/roles/features/`
2. Implement the standard role structure (defaults, vars, tasks)
3. Add the role to `playbooks/bootstrap.yml` with an appropriate tag
4. Test the role on supported distributions

See the [Adding a Role Guide](../../../guides/adding-a-role.md) for detailed instructions.

## See Also

- [Base Roles](../base/index.md): System-level roles
- [Tags Reference](../../tags.md): Complete tag listing
- [Roles Organization](../../../architecture/roles-organization.md): Architecture details
