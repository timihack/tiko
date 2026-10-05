# Tiko

A minimalist, fully offline desktop clock, countdown timer, and stopwatch — inspired by the simplicity of Fliclo, built as a real desktop application rather than a script with a GUI attached.

## Features

- Large, minimalist clock display — 12-hour or 24-hour format, optional seconds, optional date
- Countdown timer — duration presets (1/5/10/25/30/45/60 minutes) plus a custom duration, with Start/Pause/Resume/Reset
- Stopwatch — Start/Pause/Reset
- Fullscreen / desk mode
- Appearance customization — Dark and Light themes, four font choices (Inter, JetBrains Mono, IBM Plex Mono, Roboto Mono), adjustable font size, and accent color presets (Teal, Amber, Coral) independent of theme
- Persistent settings — every preference survives a restart
- Keyboard shortcuts for every core action
- Sound and desktop notification when a timer finishes
- System tray menu (Open / Start timer / Pause timer / Quit)
- Fully offline: no accounts, no cloud sync, no analytics, no telemetry

## Requirements

- Python 3.12 or later
- PySide6
- Linux, Windows, or macOS

## Installation

Tiko isn't published as a downloadable release yet. For now, getting a working copy means building it yourself:

- To run it from source, see **Development Setup** below.
- To produce a standalone Linux AppImage/`.deb`, Windows `.exe`, or macOS `.app`, see **Packaging** below.

## Development Setup

```bash
git clone <this-repo-url>
cd tiko
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

If you have Anaconda/conda installed, make sure it's fully deactivated (`conda deactivate`, check your prompt has no `(base)`) before creating the virtual environment — mixing conda and venv Python installations causes hard-to-diagnose library conflicts, particularly when building with PyInstaller.

## Running the Application

```bash
python -m app.main
```

## Testing

```bash
pytest
```

77 tests cover clock formatting, countdown timer and stopwatch logic, duration formatting, appearance (including WCAG contrast ratios for every theme/accent combination), and settings persistence — including recovery from a corrupted settings file.

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `C` | Switch to Clock |
| `T` | Switch to Timer |
| `S` | Switch to Stopwatch |
| `Space` | Start/Pause the active timer or stopwatch |
| `R` | Reset the active timer or stopwatch |
| `F` | Toggle fullscreen |
| `Esc` | Exit fullscreen, or close the Settings panel |

The gear icon (top-right corner) opens and closes the Settings panel with the mouse.

## Building

Tiko is packaged with PyInstaller, using the included `tiko.spec`:

```bash
pip install -e ".[dev]" pyinstaller
pyinstaller tiko.spec --noconfirm
```

This must be run separately on each target operating system — PyInstaller does not cross-compile. It produces:

- Linux: `dist/tiko`
- Windows: `dist/tiko.exe`
- macOS: `dist/Tiko.app`

## Packaging

### Linux — AppImage

```bash
mkdir -p Tiko.AppDir/usr/bin
cp dist/tiko Tiko.AppDir/usr/bin/
cp packaging/icon_256.png Tiko.AppDir/tiko.png
printf '[Desktop Entry]\nType=Application\nName=Tiko\nComment=A minimalist desktop clock, timer, and stopwatch\nExec=tiko\nIcon=tiko\nCategories=Utility;Clock;\nTerminal=false\n' > Tiko.AppDir/tiko.desktop
printf '#!/bin/bash\nHERE="$(dirname "$(readlink -f "${0}")")"\nexec "${HERE}/usr/bin/tiko" "$@"\n' > Tiko.AppDir/AppRun
chmod +x Tiko.AppDir/AppRun

wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage Tiko.AppDir Tiko-x86_64.AppImage
```

Running the resulting AppImage requires `libfuse2` on the host system (`sudo apt install libfuse2t64` on Ubuntu 24.04+). If `appimagetool` itself fails to run with a FUSE error, extract and run it instead: `./appimagetool-x86_64.AppImage --appimage-extract`, then use `./squashfs-root/AppRun` in place of the tool.

### Linux — `.deb`

```bash
mkdir -p deb/tiko_0.1.0/DEBIAN deb/tiko_0.1.0/usr/bin deb/tiko_0.1.0/usr/share/applications deb/tiko_0.1.0/usr/share/icons/hicolor/256x256/apps
cp dist/tiko deb/tiko_0.1.0/usr/bin/tiko
cp packaging/icon_256.png deb/tiko_0.1.0/usr/share/icons/hicolor/256x256/apps/tiko.png
printf '[Desktop Entry]\nType=Application\nName=Tiko\nComment=A minimalist desktop clock, timer, and stopwatch\nExec=tiko\nIcon=tiko\nCategories=Utility;Clock;\nTerminal=false\n' > deb/tiko_0.1.0/usr/share/applications/tiko.desktop

INSTALLED_SIZE=$(du -sk dist/tiko | cut -f1)
printf 'Package: tiko\nVersion: 0.1.0\nSection: utils\nPriority: optional\nArchitecture: amd64\nInstalled-Size: %s\nMaintainer: Tiko <noreply@example.com>\nDescription: A minimalist desktop clock, timer, and stopwatch\n A minimalist, fully offline desktop clock with a built-in\n countdown timer and stopwatch.\n' "$INSTALLED_SIZE" > deb/tiko_0.1.0/DEBIAN/control

chmod 755 deb/tiko_0.1.0/usr/bin/tiko
dpkg-deb --build --root-owner-group deb/tiko_0.1.0 Tiko_0.1.0_amd64.deb
sudo dpkg -i Tiko_0.1.0_amd64.deb
```

### macOS

`dist/Tiko.app` is unsigned. On first launch, Gatekeeper will warn that the developer cannot be verified — right-click → Open to bypass it once. Distributing the app without that warning requires an Apple Developer account to code-sign and notarize it, which is not set up for this project.

### Windows

`dist\tiko.exe` runs standalone — no additional packaging step is required.

## License

All rights reserved. This code is public for viewing only — no permission is granted for reuse, modification, or redistribution. See `LICENSE` for the full notice.