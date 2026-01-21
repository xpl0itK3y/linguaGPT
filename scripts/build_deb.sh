#!/bin/bash
# Script to create .deb package for LinguaGPT

set -e

APP_NAME="linguagpt"
VERSION="1.0.0"
ARCH="amd64"
PACKAGE_NAME="${APP_NAME}_${VERSION}_${ARCH}"

echo "Creating .deb package for LinguaGPT..."

# Create package structure
mkdir -p "${PACKAGE_NAME}/DEBIAN"
mkdir -p "${PACKAGE_NAME}/usr/bin"
mkdir -p "${PACKAGE_NAME}/usr/share/applications"
mkdir -p "${PACKAGE_NAME}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}"

# Copy executable file
echo "Copying files..."
cp ../dist/LinguaGPT "${PACKAGE_NAME}/usr/bin/linguagpt"
chmod +x "${PACKAGE_NAME}/usr/bin/linguagpt"

# Copy .desktop file
cp ../resources/linguagpt.desktop "${PACKAGE_NAME}/usr/share/applications/"

# Create icon (if available)
# cp icon.png "${PACKAGE_NAME}/usr/share/icons/hicolor/256x256/apps/linguagpt.png"

# Copy documentation
cp ../README.md "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}/"
cp ../LICENSE "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}/" 2>/dev/null || echo "LICENSE file not found"

# Create control file
cat > "${PACKAGE_NAME}/DEBIAN/control" << EOF
Package: ${APP_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: libc6, libgcc-s1, libstdc++6
Maintainer: Your Name <your@email.com>
Description: AI-powered translator with GPT
 LinguaGPT is a modern translation application powered by OpenAI's GPT models.
 Features include:
  - Real-time streaming translation
  - Multiple language support
  - Alternative translation suggestions
  - System tray integration
  - Beautiful modern UI
Homepage: https://github.com/yourusername/linguagpt
EOF

# Create postinst script (post-installation)
cat > "${PACKAGE_NAME}/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Update icon cache
if [ -x "$(command -v gtk-update-icon-cache)" ]; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi

# Update .desktop files database
if [ -x "$(command -v update-desktop-database)" ]; then
    update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi

echo "LinguaGPT installed successfully!"
echo "Run: linguagpt or find in applications menu"

exit 0
EOF

chmod +x "${PACKAGE_NAME}/DEBIAN/postinst"

# Create prerm script (pre-removal)
cat > "${PACKAGE_NAME}/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

# Stop application if running
pkill -f linguagpt 2>/dev/null || true

exit 0
EOF

chmod +x "${PACKAGE_NAME}/DEBIAN/prerm"

# Create postrm script (post-removal)
cat > "${PACKAGE_NAME}/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e

# Remove user config (optional)
# rm -f ~/.gpt_translator_config.json 2>/dev/null || true

# Update icon cache
if [ -x "$(command -v gtk-update-icon-cache)" ]; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi

# Update .desktop files database
if [ -x "$(command -v update-desktop-database)" ]; then
    update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi

exit 0
EOF

chmod +x "${PACKAGE_NAME}/DEBIAN/postrm"

# Create copyright file
cat > "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}/copyright" << EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: LinguaGPT
Source: https://github.com/yourusername/linguagpt

Files: *
Copyright: $(date +%Y) Your Name
License: MIT
 [MIT license text]
EOF

# Create changelog
cat > "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}/changelog" << EOF
linguagpt (${VERSION}) unstable; urgency=medium

  * Initial release
  * AI-powered translation with GPT models
  * Multiple language support
  * Real-time streaming translation
  * System tray integration

 -- Your Name <your@email.com>  $(date -R)
EOF

gzip -9 "${PACKAGE_NAME}/usr/share/doc/${APP_NAME}/changelog"

# Set correct permissions
echo "Setting permissions..."
find "${PACKAGE_NAME}" -type f -exec chmod 644 {} \;
find "${PACKAGE_NAME}" -type d -exec chmod 755 {} \;
chmod +x "${PACKAGE_NAME}/usr/bin/linguagpt"
chmod +x "${PACKAGE_NAME}/DEBIAN/postinst"
chmod +x "${PACKAGE_NAME}/DEBIAN/prerm"
chmod +x "${PACKAGE_NAME}/DEBIAN/postrm"

# Build package
echo "Building package..."
dpkg-deb --build --root-owner-group "${PACKAGE_NAME}"

# Move to installers folder
mkdir -p ../installers
mv "${PACKAGE_NAME}.deb" ../installers/

# Cleanup
rm -rf "${PACKAGE_NAME}"

echo "Package created: ../installers/${PACKAGE_NAME}.deb"
echo ""
echo "Installation:"
echo "   sudo dpkg -i ../installers/${PACKAGE_NAME}.deb"
echo "   sudo apt-get install -f  # If dependencies needed"
echo ""
echo "Removal:"
echo "   sudo apt-get remove ${APP_NAME}"
echo ""
echo "Package verification:"
echo "   dpkg-deb -I ../installers/${PACKAGE_NAME}.deb"
echo "   dpkg-deb -c ../installers/${PACKAGE_NAME}.deb"
