# LinguaGPT Build Scripts

This folder contains scripts for building and creating application installers.

## Structure

- `build_deb.sh` - creates .deb package for Linux (Debian/Ubuntu)
- `build_dmg.sh` - creates DMG image for macOS
- `installer.iss` - Inno Setup configuration for Windows installer
- `LinguaGPT.spec` - PyInstaller specification

## Usage

**Important:** All scripts must be run from project root!

### Build Executable

```bash
# From project root
python build.py
```

### Create Installers

#### Linux (.deb package)

```bash
# From project root
bash scripts/build_deb.sh
```

Result: `installers/linguagpt_1.0.0_amd64.deb`

#### macOS (DMG)

```bash
# From project root
bash scripts/build_dmg.sh
```

Result: `installers/LinguaGPT-1.0.0.dmg`

#### Windows (Inno Setup)

1. Install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Open `scripts/installer.iss` in Inno Setup Compiler
3. Click "Compile"

Or via command line:
```bash
# From project root
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" scripts\installer.iss
```

Result: `installers/LinguaGPT-Setup-1.0.0.exe`

## Dependencies

Before running scripts, ensure:
1. Application is built (`python build.py`)
2. Build output is in `dist/`
3. You're running scripts from project root

