# LinguaGPT 🌐

AI-powered translation tool using GPT models for high-quality translations between languages.

## ✨ Features

- 🤖 **GPT-powered translations** - High-quality translations using OpenAI's API
- 🌍 **Multi-language support** - Translate between 100+ languages
- 🎨 **Modern Dark UI** - Clean, user-friendly dark interface
- 📱 **Cross-platform** - Available for Windows, macOS, and Linux
- ⚡ **Fast & Lightweight** - Optimized for performance
- 🔒 **Secure** - API key stored locally

## 🚀 Quick Start

### Download

Get the latest release from [Releases](https://github.com/xpl0itK3y/linguaGPT/releases) page.

### Installation

#### Windows
1. Download `LinguaGPT-Setup-*.exe` (recommended) or `LinguaGPT.exe` (portable)
2. Run the installer or executable

#### macOS
1. Download `LinguaGPT-*.dmg`
2. Open DMG and drag LinguaGPT.app to Applications
3. Or download `LinguaGPT.app.zip` and extract

#### Linux
1. **Option 1 - DEB Package**: Download `linguagpt_*_amd64.deb` and install:
   ```bash
   sudo dpkg -i linguagpt_*_amd64.deb
   ```
2. **Option 2 - Executable**: Download `LinguaGPT` and run:
   ```bash
   chmod +x LinguaGPT
   ./LinguaGPT
   ```

## 🔧 Requirements

- OpenAI API key (get from [OpenAI Platform](https://platform.openai.com/))
- Internet connection
- For Linux: X11 display server

## 📝 Usage

1. Launch LinguaGPT
2. Enter your OpenAI API key in settings
3. Select source and target languages
4. Enter or paste text to translate
5. Click "Translate" or press Enter
6. Copy the translated result

## 🏗️ Build from Source

```bash
# Clone repository
git clone https://github.com/xpl0itK3y/linguaGPT.git
cd linguagpt

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build application
python build.py

# Run application
python main.py
```

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run application in development mode
python main.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [OpenAI](https://openai.com/) - GPT API for translations
- [PyInstaller](https://pyinstaller.org/) - Application bundling

## 📧 Support

If you have any questions or issues:

- 🐛 [Report Issues](https://github.com/xpl0itK3y/linguaGPT/issues)
- 💬 [Discussions](https://github.com/xpl0itK3y/linguaGPT/discussions)
- 📧 Email: support@linguagpt.com

---
