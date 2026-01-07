# Wallpaper Effects Generator Role

The wallpaper-effects-generator role installs the wallpaper effects processing tool, which applies ImageMagick effects to wallpaper images using containerized execution.

## Tag

`wallpaper-effects-generator`

## Tasks Performed

The role executes the following tasks (from `playbooks/roles/features/wallpaper-effects-generator/tasks/main.yml`):

1. **Ensure installation directory exists**: Creates the installation directory if it doesn't exist
2. **Clone wallpaper-effects-generator repository**: Clones the repository from GitHub
3. **Install core dependencies**: Runs `uv sync` in the core directory
4. **Install orchestrator dependencies**: Runs `uv sync` in the orchestrator directory
5. **Build wallpaper-effects Docker image**: Builds the ImageMagick-based Docker image
6. **Verify wallpaper-effects CLI**: Verifies the CLI is working
7. **Report installation status**: Displays success message

## Variables

### Defaults

Defined in `playbooks/roles/features/wallpaper-effects-generator/defaults/main.yml`:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `wallpaper_effects_install_dest` | `{{ xdg_data_home }}/wallpaper-effects-generator` | Installation directory |
| `wallpaper_effects_repo_url` | `https://github.com/RandomGenericUsername/wallpaper-effects-generator` | Repository URL |
| `wallpaper_effects_repo_version` | `main` | Git branch/tag to clone |
| `wallpaper_effects_build_docker` | `true` | Whether to build Docker image |
| `wallpaper_effects_image` | `wallpaper-effects` | Docker image name |
| `WALLPAPER_EFFECTS_BIN_DIR` | `{{ wallpaper_effects_install_dest }}/orchestrator` | Path for zsh integration |

### Role Variables

Defined in `playbooks/roles/features/wallpaper-effects-generator/vars/main.yml`:

| Variable | Description |
|----------|-------------|
| `wallpaper_effects_core_dir` | Path to core component directory |
| `wallpaper_effects_orchestrator_dir` | Path to orchestrator component directory |

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

Install wallpaper-effects-generator with default settings:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml --tags wallpaper-effects-generator
```

### Custom Installation Path

Override the installation destination:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags wallpaper-effects-generator \
  -e wallpaper_effects_install_dest=/opt/tools/wallpaper-effects-generator
```

### Skip Docker Build

Install without building Docker image (useful if image already exists):

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags wallpaper-effects-generator \
  -e wallpaper_effects_build_docker=false
```

### Use Specific Branch/Tag

Clone a specific version:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags wallpaper-effects-generator \
  -e wallpaper_effects_repo_version=v1.0.0
```

## Post-Installation Usage

After installation, the tool can be used from the installation directory:

```bash
cd ~/.local/share/wallpaper-effects-generator/orchestrator
uv run wallpaper-effects --help
uv run wallpaper-effects process /path/to/wallpaper.png
```

### Zsh Integration

If installed alongside the zsh role, you can set up an alias by providing the `WALLPAPER_EFFECTS_BIN_DIR` variable:

```bash
ansible-playbook -i inventory/localhost.yml playbooks/bootstrap.yml \
  --tags wallpaper-effects-generator,zsh \
  -e WALLPAPER_EFFECTS_BIN_DIR=~/.local/share/wallpaper-effects-generator/orchestrator
```

This creates a `wallpaper-effects` alias in your shell.

## Architecture

The wallpaper-effects-generator follows a dual-component architecture:

```
wallpaper-effects-generator/
├── core/                    # Standalone Python library
│   ├── src/
│   └── pyproject.toml
└── orchestrator/            # Docker-based CLI tool
    ├── src/
    ├── docker/
    │   ├── Dockerfile.imagemagick
    │   └── Dockerfile.pil
    └── pyproject.toml
```

- **Core**: The standalone wallpaper processing library
- **Orchestrator**: CLI that runs ImageMagick in Docker containers

## Docker Images

The role builds the following Docker image:

| Image | Dockerfile | Purpose |
|-------|------------|---------|
| `wallpaper-effects:latest` | `Dockerfile.imagemagick` | ImageMagick-based effects processor |

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

### ImageMagick effects not working

The ImageMagick installation is inside the Docker container. Ensure the container is built:

```bash
docker images | grep wallpaper-effects
```

## See Also

- [Variables Reference](../../variables.md): Global variables documentation
- [Tags Reference](../../tags.md): All available tags
- [Color Scheme Generator](color-scheme-generator.md): Related tool for color palette extraction
