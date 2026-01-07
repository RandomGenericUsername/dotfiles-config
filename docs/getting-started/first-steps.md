# First Steps

[VERIFIED via CLI - 2026-01-03]

Getting started with basic usage of the dotfiles-config CLI.

## Overview

The `config` CLI provides commands for:
- Installing and configuring system packages
- Managing wallpaper assets
- Testing functionality

## Command Structure

```bash
config [OPTIONS] COMMAND [ARGS]...
```

[VERIFIED via CLI - 2026-01-03]

## Basic Commands

### Get Help

View all available commands:

```bash
config --help
```

[VERIFIED via CLI - 2026-01-03]

View help for a specific command:

```bash
config install-packages --help
config assets wallpapers --help
config assets wallpapers add --help
```

[VERIFIED via CLI - 2026-01-03]

### Test the CLI

Run the dummy command to verify installation:

```bash
config dummy
```

[VERIFIED via CLI - 2026-01-03]

Output: `This is a dummy command! It doesn't do much, but it works!`

## Working with Wallpapers

### List Wallpapers

View all wallpapers in the archive:

```bash
config assets wallpapers list
```

[VERIFIED via CLI - 2026-01-03]

Example output:
```
Wallpapers in archive (3):
  - mountain.jpg
  - ocean.png
  - sunset.webp
```

### Add a Wallpaper

Add a new wallpaper to the archive:

```bash
config assets wallpapers add ~/Pictures/my-wallpaper.jpg
```

[VERIFIED via CLI - 2026-01-03]

Add with force overwrite if wallpaper exists:

```bash
config assets wallpapers add --force ~/Pictures/my-wallpaper.jpg
```

[VERIFIED via CLI - 2026-01-03]

Add without validating file extension:

```bash
config assets wallpapers add --no-validate /path/to/file.txt
```

[VERIFIED via CLI - 2026-01-03]

### Extract Wallpapers

Extract all wallpapers to a directory:

```bash
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

This creates `~/Pictures/wallpapers/` and extracts all wallpapers there.

Example output:
```
Extracted 3 wallpaper(s) to /home/user/Pictures/wallpapers
```

## Installing Packages

### Install with Ansible

Install all packages and configurations:

```bash
config install-packages --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

The `--ask-become-pass` flag prompts for your sudo password.

### Install Specific Packages

Install only Neovim:

```bash
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

### Debug Mode

View debug information:

```bash
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

This shows:
- Playbook directory
- Dotfiles root path
- Config files root path

### Additional Ansible Options

Forward any Ansible options:

```bash
# Increase verbosity
config install-packages --tags nvim -v

# Set custom variables
config install-packages --tags nvim -e nvim_config_dest=/tmp/nvim-test

# Multiple tags
config install-packages --tags nvim,debug --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

## Shell Completion

### Install Completion

Install shell completion for your shell:

```bash
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

### Use Completion

After installation, you can use tab completion:

```bash
config <TAB>              # Shows: assets, dummy, install-packages
config assets <TAB>       # Shows: wallpapers
config assets wallpapers <TAB>  # Shows: add, extract, list
```

## Common Workflows

### Workflow 1: Setting Up a New System

```bash
# 1. Install the CLI
make install-dev
source .venv/bin/activate

# 2. Install packages and configurations
config install-packages --tags nvim --ask-become-pass

# 3. Extract wallpapers
config assets wallpapers extract ~/Pictures

# 4. Enable shell completion
config --install-completion
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 2: Adding New Wallpapers

```bash
# 1. Add wallpaper
config assets wallpapers add ~/Downloads/new-wallpaper.png

# 2. Verify it was added
config assets wallpapers list

# 3. Optionally extract to use
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

### Workflow 3: Testing Changes

```bash
# 1. Make code changes

# 2. Run tests
make test-cov

# 3. Test CLI manually
config dummy
config assets wallpapers list

# 4. Check specific functionality
config install-packages --tags debug
```

[VERIFIED via CLI - 2026-01-03]

## Understanding Exit Codes

All commands use standard exit codes:

**Exit 0:** Success

```bash
config dummy
echo $?  # Output: 0
```

[VERIFIED via CLI - 2026-01-03]

**Exit 1:** Error

```bash
config assets wallpapers add /nonexistent/file.jpg
echo $?  # Output: 1
```

[VERIFIED via source - 2026-01-03]

## Error Messages

The CLI provides clear error messages:

**File not found:**
```
Error: Wallpaper file not found: /path/to/file.jpg
```

**Invalid image extension:**
```
Error: File does not have a valid image extension: document.txt
```

**Duplicate wallpaper:**
```
Error: Wallpaper 'image.png' already exists in archive. Use --force to overwrite.
```

**Archive not found:**
```
Error: Archive not found: /path/to/wallpapers.tar.gz
```

[VERIFIED via source - 2026-01-03]

## Tips and Best Practices

### 1. Use Tab Completion

Install shell completion to discover commands faster:

```bash
config --install-completion
```

### 2. Check Help First

Always check command help for available options:

```bash
config <command> --help
```

### 3. Use Make Targets

Use Make targets for common tasks:

```bash
make test       # Run tests
make shell      # Activate venv
make clean      # Clean up
```

[VERIFIED via source - 2026-01-03]

### 4. Verify After Operations

Always verify operations completed successfully:

```bash
config assets wallpapers add wallpaper.jpg
config assets wallpapers list  # Verify it's there
```

### 5. Use Force Flag Carefully

The `--force` flag overwrites without warning:

```bash
config assets wallpapers add --force wallpaper.jpg  # Overwrites existing
```

## Next Steps

- **Learn Architecture:** Read [Architecture Overview](../architecture/index.md)
- **Explore All Commands:** Browse [CLI Reference](../reference/cli/index.md)
- **Advanced Usage:** Read [Usage Guides](../guides/usage/index.md)
- **Development:** See [Development Guide](../guides/development/index.md)

## See Also

- [Installation](installation.md) - Installation instructions
- [Project Structure](project-structure.md) - Understanding the repository
- [CLI Reference](../reference/cli/index.md) - Complete command reference
