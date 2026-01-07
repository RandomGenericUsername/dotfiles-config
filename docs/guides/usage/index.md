# Usage Guides

[VERIFIED via CLI - 2026-01-03]

Practical guides for using the dotfiles-config system.

## Contents

- [Managing Wallpapers](wallpapers.md) - How to work with wallpaper assets
- [Installing Packages](packages.md) - Using Ansible to install packages

## Quick Reference

### Wallpapers

```bash
# List wallpapers
config assets wallpapers list

# Add wallpaper
config assets wallpapers add ~/Pictures/my-wallpaper.jpg

# Extract wallpapers
config assets wallpapers extract ~/Pictures
```

[VERIFIED via CLI - 2026-01-03]

### Package Installation

```bash
# Install all packages
config install-packages --ask-become-pass

# Install specific packages
config install-packages --tags nvim --ask-become-pass
```

[VERIFIED via CLI - 2026-01-03]

## See Also

- [CLI Reference](../../reference/cli/index.md)
- [First Steps](../../getting-started/first-steps.md)
