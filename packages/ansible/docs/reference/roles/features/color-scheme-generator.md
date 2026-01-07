# Color Scheme Generator Role

The color-scheme-generator role installs the color scheme extraction tool, which generates color palettes from wallpaper images using containerized backends (pywal, wallust).

## Tag

`color-scheme-generator`

## Tasks Performed

The role executes the following tasks (from `playbooks/roles/features/color-scheme-generator/tasks/main.yml`):

1. **Ensure installation directory exists**: Creates the installation directory if it doesn't exist
2. **Clone color-scheme-generator repository**: Clones the repository from GitHub
3. **Install core dependencies**: Runs `uv sync` in the core directory
4. **Install orchestrator dependencies**: Runs `uv sync` in the orchestrator directory
5. **Build pywal Docker image**: Builds the pywal backend Docker image
6. **Build wallust Docker image**: Builds the wallust backend Docker image
7. **Verify color-scheme CLI**: Verifies the CLI is working
8. **Report installation status**: Displays success message

## Variables

### Defaults

Defined in `playbooks/roles/features/color-scheme-generator/defaults/main.yml`:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `color_scheme_install_dest` | `{{ xdg_data_home }}/color-scheme-generator` | Installation directory |
| `color_scheme_repo_url` | `https://github.com/RandomGenericUsername/color-scheme-generator` | Repository URL |
| `color_scheme_repo_version` | `main` | Git branch/tag to clone |
| `color_scheme_build_docker` | `true` | Whether to build Docker images |
| `color_scheme_image_pywal` | `color-scheme-pywal` | Pywal Docker image name |
| `color_scheme_image_wallust` | `color-scheme-wallust` | Wallust Docker image name |
| `COLOR_SCHEME_BIN_DIR` | `{{ color_scheme_install_dest }}/orchestrator` | Path for zsh integration |

### Role Variables

Defined in `playbooks/roles/features/color-scheme-generator/vars/main.yml`:

| Variable | Description |
|----------|-------------|
| `color_scheme_core_dir` | Path to core component directory |
| `color_scheme_orchestrator_dir` | Path to orchestrator component directory |

## Prerequisites

This role requires the following to be installed (not managed by Ansible):

| Requirement | Purpose | Verification |
|-------------|---------|--------------|
| `uv` | Python package manager | `uv --version` |
| Docker or Podman | Container runtime | `docker --version` |
| Git | Repository cloning | `git --version` |
| Python 3.12+ | Runtime | `python3 --version` |

## Usage

### Basic Installation

Install color-scheme-generator with default settings:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags color-scheme-generator
```

### Custom Installation Path

Override the installation destination:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags color-scheme-generator \
  -e color_scheme_install_dest=/opt/tools/color-scheme-generator
```

### Skip Docker Build

Install without building Docker images (useful if images already exist):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags color-scheme-generator \
  -e color_scheme_build_docker=false
```

### Use Specific Branch/Tag

Clone a specific version:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags color-scheme-generator \
  -e color_scheme_repo_version=v1.0.0
```

## Post-Installation Usage

After installation, the tool can be used from the installation directory:

```bash
cd ~/.local/share/color-scheme-generator/orchestrator
uv run color-scheme --help
uv run color-scheme generate /path/to/wallpaper.png
```

### Zsh Integration

If installed alongside the zsh role, you can set up an alias by providing the `COLOR_SCHEME_BIN_DIR` variable:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags color-scheme-generator,zsh \
  -e COLOR_SCHEME_BIN_DIR=~/.local/share/color-scheme-generator/orchestrator
```

This creates a `color-scheme` alias in your shell.

## Architecture

The color-scheme-generator follows a dual-component architecture:

```
color-scheme-generator/
├── core/                    # Standalone Python library
│   ├── src/
│   └── pyproject.toml
└── orchestrator/            # Docker-based CLI tool
    ├── src/
    ├── docker/
    │   ├── Dockerfile.pywal
    │   └── Dockerfile.wallust
    └── pyproject.toml
```

- **Core**: The standalone color extraction library
- **Orchestrator**: CLI that runs backends in Docker containers

## Docker Images

The role builds the following Docker images:

| Image | Dockerfile | Purpose |
|-------|------------|---------|
| `color-scheme-pywal:latest` | `Dockerfile.pywal` | Pywal backend |
| `color-scheme-wallust:latest` | `Dockerfile.wallust` | Wallust backend |

## Troubleshooting

### uv sync fails

Ensure `uv` is installed and in your PATH:

```bash
uv --version
```

### Docker build fails

Ensure Docker/Podman is running:

```bash
docker ps
# or
podman ps
```

### Permission denied

The role does not require root privileges. Ensure your user can run Docker commands:

```bash
docker run hello-world
```

## See Also

- [Variables Reference](../../variables.md): Global variables documentation
- [Tags Reference](../../tags.md): All available tags
- [Wallpaper Effects Generator](wallpaper-effects-generator.md): Related tool for wallpaper processing
