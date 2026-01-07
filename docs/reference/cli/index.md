# CLI Reference

[VERIFIED via CLI - 2026-01-03]

Complete reference documentation for the `config` command-line interface.

## Main Command

```bash
config [OPTIONS] COMMAND [ARGS]...
```

**Description:** Dotfiles configuration management CLI

**Options:**

| Option | Description |
|--------|-------------|
| `--install-completion` | Install completion for the current shell |
| `--show-completion` | Show completion for the current shell, to copy it or customize the installation |
| `--help` | Show this message and exit |

**Source:** [src/main.py](../../../src/main.py)

## Available Commands

### Core Commands

- [install-packages](install-packages.md) - Install packages using Ansible playbook
- [dummy](dummy.md) - A dummy command that prints a message

### Command Groups

- [assets](assets/index.md) - Manage dotfiles assets
  - [wallpapers](assets/wallpapers.md) - Manage wallpaper assets

## Command Hierarchy

```
config
├── install-packages    (Install packages using Ansible)
├── dummy              (Example dummy command)
└── assets             (Asset management group)
    └── wallpapers     (Wallpaper management)
        ├── add        (Add wallpaper to archive)
        ├── list       (List wallpapers in archive)
        └── extract    (Extract wallpapers from archive)
```

## Shell Completion

The CLI supports shell completion. Install it with:

```bash
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]
