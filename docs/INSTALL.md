# LinguaGPT - Installation Guide

## For Users: Installing Pre-built Application

### Windows

**Option 1: Installer (Recommended)**
1. Download `LinguaGPT-Setup-1.0.0.exe`
2. Run installer
3. Follow installation wizard
4. Select options:
   - Create desktop shortcut
   - Launch at Windows startup (optional)
5. After installation, app appears in Start menu
6. Launch and enter API key in settings

**Option 2: Portable Version**
1. Download `LinguaGPT.exe`
2. Place in any folder
3. Double-click to run

**Removal:**
Control Panel → Programs → LinguaGPT → Uninstall

---

### macOS

**Installation:**
1. Download `LinguaGPT-1.0.0.dmg`
2. Open DMG file
3. Drag LinguaGPT.app to Applications folder
4. Launch from Launchpad or Applications

**First Launch:**
- If "cannot open because developer cannot be verified" appears:
  1. System Settings → Privacy & Security
  2. Click "Open Anyway"
- Or run in terminal:
  ```bash
  xattr -cr /Applications/LinguaGPT.app
  ```

**Removal:**
- Drag LinguaGPT.app to Trash from Applications folder

---

### Linux

**Ubuntu/Debian (.deb package):**
```bash
# Download package
wget https://github.com/yourusername/linguagpt/releases/download/v1.0.0/linguagpt_1.0.0_amd64.deb

# Install
sudo dpkg -i linguagpt_1.0.0_amd64.deb

# Fix dependencies if needed
sudo apt-get install -f

# Run
linguagpt
```

**AppImage (Universal):**
```bash
# Download
wget https://github.com/yourusername/linguagpt/releases/download/v1.0.0/LinguaGPT-1.0.0-x86_64.AppImage

# Make executable
chmod +x LinguaGPT-1.0.0-x86_64.AppImage

# Run
./LinguaGPT-1.0.0-x86_64.AppImage
```

**Arch Linux (AUR):**
```bash
yay -S linguagpt
```

**Removal:**
```bash
# Debian/Ubuntu
sudo apt-get remove linguagpt

# Arch
sudo pacman -R linguagpt
```

**Application appears in menu:**
- Applications → Utilities → LinguaGPT
- Or run via terminal: `linguagpt`

---

## For Developers: Building and Creating Installers

### Step 1: Preparation

```bash
# Clone repository
git clone https://github.com/yourusername/linguagpt.git
cd linguagpt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Build Executable

```bash
# Build application
python build.py

# Result in dist/ folder
# Windows: dist/LinguaGPT.exe
# macOS: dist/LinguaGPT.app
# Linux: dist/LinguaGPT
```

### Step 3: Create Installer

#### Windows - Inno Setup Installer

```bash
# 1. Install Inno Setup
# Download: https://jrsoftware.org/isdl.php

# 2. Build application
python build.py

# 3. Open installer.iss in Inno Setup Compiler

# 4. Click "Compile"

# Result: installers/LinguaGPT-Setup-1.0.0.exe
```

**Or via command line:**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

#### macOS - DMG Image

```bash
# Install create-dmg (optional, for styled DMG)
brew install create-dmg

# Build application
python build.py

# Create DMG
chmod +x build_dmg.sh
./build_dmg.sh

# Result: installers/LinguaGPT-1.0.0.dmg
```

**For app signing (requires Apple Developer Account):**
```bash
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAMID)" \
  dist/LinguaGPT.app

# Verify
codesign --verify --deep --verbose=2 dist/LinguaGPT.app

# Notarization (for distribution outside App Store)
xcrun notarytool submit LinguaGPT-1.0.0.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAMID"
```

#### Linux - .deb Package

```bash
# Build application
python build.py

# Create .deb package
chmod +x build_deb.sh
./build_deb.sh

# Result: installers/linguagpt_1.0.0_amd64.deb
```

**Package testing:**
```bash
# Check structure
dpkg-deb -c installers/linguagpt_1.0.0_amd64.deb

# Check metadata
dpkg-deb -I installers/linguagpt_1.0.0_amd64.deb

# Test install
sudo dpkg -i installers/linguagpt_1.0.0_amd64.deb
```

#### Linux - AppImage

```bash
# Install linuxdeploy
wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-x86_64.AppImage

# Create AppImage
./linuxdeploy-x86_64.AppImage \
  --appdir AppDir \
  --executable dist/LinguaGPT \
  --desktop-file linguagpt.desktop \
  --icon-file icon.png \
  --output appimage

# Result: LinguaGPT-1.0.0-x86_64.AppImage
```

---

## System Requirements

| Platform | Minimum | Recommended |
|----------|---------|-------------|
| **Windows** | Windows 10 (64-bit) | Windows 11 |
| **macOS** | macOS 10.14 Mojave | macOS 13 Ventura+ |
| **Linux** | Ubuntu 20.04, Debian 11 | Ubuntu 22.04+ |
| **RAM** | 4 GB | 8 GB |
| **Disk** | 200 MB free | 500 MB |
| **Internet** | Required for API | - |

---

## OpenAI API Configuration

1. **Registration:**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Create account or sign in

2. **Create API Key:**
   - Open [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy key (shown only once!)

3. **In LinguaGPT:**
   - Open settings
   - Paste API key
   - Select model (GPT-4o Mini recommended)
   - Click "Save"

---

## Troubleshooting

### Windows

**Application won't start:**
- Check antivirus (add to exclusions)
- Install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- Run as administrator

**Not appearing in tray:**
- Check taskbar settings
- Restart explorer.exe

### macOS

**"Damaged and cannot be opened":**
```bash
xattr -cr /Applications/LinguaGPT.app
```

**Won't start:**
- Ensure macOS 10.14+
- Allow in System Settings → Security

### Linux

**No icon in menu:**
```bash
sudo update-desktop-database
gtk-update-icon-cache -f -t /usr/share/icons/hicolor
```

**Dependency errors:**
```bash
sudo apt-get install -f
```

**AppImage won't start:**
```bash
# Install FUSE
sudo apt-get install fuse libfuse2
```

---

## Installation Structure

### Windows
```
C:\Program Files\LinguaGPT\
├── LinguaGPT.exe
├── README.md
└── LICENSE.txt

User data:
C:\Users\YourName\.gpt_translator_config.json
```

### macOS
```
/Applications/LinguaGPT.app/
└── Contents/
    ├── MacOS/
    │   └── LinguaGPT
    ├── Resources/
    └── Info.plist

User data:
~/.gpt_translator_config.json
```

### Linux
```
/usr/bin/linguagpt
/usr/share/applications/linguagpt.desktop
/usr/share/icons/hicolor/256x256/apps/linguagpt.png
/usr/share/doc/linguagpt/

User data:
~/.gpt_translator_config.json
```

---

## Autostart

### Windows
- Installer offers "Launch at startup" option
- Or: Win+R → `shell:startup` → create shortcut

### macOS
- System Settings → Users & Groups → Login Items
- Add LinguaGPT.app

### Linux
- Use your DE's autostart feature
- Or add to `~/.config/autostart/linguagpt.desktop`

---

## Support

- **Bugs**: [GitHub Issues](https://github.com/yourusername/linguagpt/issues)
- **Questions**: [Discussions](https://github.com/yourusername/linguagpt/discussions)
- **Email**: support@example.com

---

## License

MIT License - free use and distribution

Copyright (c) 2024 Your Name
