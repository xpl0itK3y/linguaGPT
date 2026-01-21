# LinguaGPT

Modern desktop translator powered by OpenAI GPT with multi-language support.

## Features

- **Streaming Translation** - Real-time translation display
- **Alternative Variants** - Up to 3 translation alternatives
- **Multi-Language Support** - 10+ languages supported
- **Modern Interface** - Dark theme with gradients
- **System Tray** - Background operation
- **Flexible Settings** - GPT model selection, interface language

## Installation

### Windows
1. Download `LinguaGPT-Setup-*.exe` from [Releases](https://github.com/yourusername/linguagpt/releases)
2. Run installer and follow instructions

### macOS
1. Download `LinguaGPT-*.dmg` from [Releases](https://github.com/yourusername/linguagpt/releases)
2. Open DMG and drag app to Applications

### Linux
```bash
# Ubuntu/Debian
sudo dpkg -i linguagpt_*_amd64.deb
sudo apt-get install -f
```

See [docs/INSTALL.md](docs/INSTALL.md) for detailed instructions

## Configuration

1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Open app settings
3. Enter API key
4. Select GPT model (GPT-4o Mini recommended)

## Development

### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Run

```bash
python main.py
```

### Build

```bash
python build.py
```

## Automatic Releases

Application automatically builds for all platforms when creating a tag:

```bash
# Create new release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

GitHub Actions automatically:
- Builds app for Windows, macOS, and Linux
- Creates installers (.exe, .dmg, .deb)
- Publishes release with artifacts

## Project Structure

```
linguaGPT/
├── app/                    # Application code
│   ├── config.py          # Configuration
│   ├── main_window.py     # Main window
│   ├── settings_dialog.py # Settings
│   └── ...
├── scripts/               # Build scripts
├── resources/             # Resources
├── docs/                  # Documentation
└── .github/workflows/     # GitHub Actions
```

## License

MIT License

## Contributing

Pull requests welcome! For major changes, please open an issue first.
