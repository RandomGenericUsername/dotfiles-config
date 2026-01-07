# Assets Reference

[VERIFIED via CLI - 2026-01-03]

Documentation for all asset files and their formats.

## Overview

The `assets/` directory contains binary assets such as wallpapers, icons, and other resources used in the dotfiles configuration.

## Directory Structure

```
assets/
├── screenshot-tool-icons/
│   └── default/               - Screenshot tool icons
├── status-bar-icons/
│   ├── battery-icons/
│   │   └── default/           - Battery status icons
│   ├── email-client-icon/
│   │   └── default/           - Email client icon
│   ├── network-icons/
│   │   ├── default/           - Network status icons
│   │   ├── rounded/           - Rounded variant
│   │   └── sharp/             - Sharp variant
│   ├── power-menu-icons/
│   │   ├── default/           - Power menu icons
│   │   └── modern/            - Modern variant
│   └── wallpaper-selector-icons/
│       └── default/           - Wallpaper selector icon
├── wallpapers/
│   ├── manage_wallpapers.sh   - Bash script for wallpaper management
│   ├── README.md              - Wallpaper documentation
│   └── wallpapers.tar.gz      - Wallpaper archive
└── wlogout-icons/
    └── templates/
        └── wlogout-icons/
            └── default/       - Wlogout icons (hibernate, lock, logout, reboot, shutdown, suspend)
```

[VERIFIED via CLI - 2026-01-03]

## Asset Categories

### [Wallpapers](wallpapers.md)

Collection of wallpapers stored in tar.gz archive format.

**Location:** `assets/wallpapers/`

**Management:**
- CLI: `config assets wallpapers`
- Bash script: `manage_wallpapers.sh`

[VERIFIED via CLI - 2026-01-03]

### [Icons](icons.md)

SVG icon sets for various tools and applications.

**Categories:**
- Screenshot tool icons
- Status bar icons (battery, network, email, power menu, wallpaper selector)
- Wlogout icons

[VERIFIED via CLI - 2026-01-03]

### [File Formats](file-formats.md)

Technical documentation for asset file formats and structures.

## Icon Variants

Several icon sets provide multiple style variants:

**Network Icons:**
- default
- rounded
- sharp

**Power Menu Icons:**
- default
- modern (with gradient and background variants)

[VERIFIED via CLI - 2026-01-03]

## File Count

Total asset files: 51

[VERIFIED via CLI - 2026-01-03]

Breakdown:
- Screenshot tool icons: 5 SVG files
- Battery icons: 11 SVG files
- Email client icon: 1 SVG file
- Network icons: 21 SVG files (3 variants × 7 icons each)
- Power menu icons: 3 SVG files
- Wallpaper selector icon: 1 SVG file
- Wlogout icons: 6 SVG files
- Wallpaper management: 3 files (script, README, archive)

[VERIFIED via CLI - 2026-01-03]

## See Also

- [Wallpapers CLI Reference](../cli/assets/wallpapers.md)
