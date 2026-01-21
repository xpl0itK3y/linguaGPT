#!/bin/bash
# Script to create DMG image for macOS

set -e

APP_NAME="LinguaGPT"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-${VERSION}.dmg"

echo "Creating DMG image for ${APP_NAME}..."

# Check if application exists
if [ ! -d "../dist/${APP_NAME}.app" ]; then
    echo "Error: dist/${APP_NAME}.app not found"
    echo "First run: python build.py"
    exit 1
fi

# Create temporary folder for DMG
TMP_DIR="dmg_temp"
rm -rf "${TMP_DIR}"
mkdir -p "${TMP_DIR}"

# Copy application
echo "Copying ${APP_NAME}.app..."
cp -R "../dist/${APP_NAME}.app" "${TMP_DIR}/"

# Create symbolic link to Applications
echo "Creating Applications symlink..."
ln -s /Applications "${TMP_DIR}/Applications"

# Copy README
if [ -f "../README.md" ]; then
    cp ../README.md "${TMP_DIR}/"
fi

# Create background image (optional)
# mkdir -p "${TMP_DIR}/.background"
# cp background.png "${TMP_DIR}/.background/"

# Create .DS_Store for nice layout (optional)
cat > "${TMP_DIR}/.DS_Store.info" << 'EOF'
# To create nice DMG use create-dmg
# brew install create-dmg
EOF

mkdir -p ../installers

# Check for create-dmg
if command -v create-dmg &> /dev/null; then
    echo "Creating styled DMG with create-dmg..."

    create-dmg \
        --volname "${APP_NAME}" \
        --volicon "icon.icns" \
        --window-pos 200 120 \
        --window-size 800 450 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 200 190 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 600 185 \
        --background "background.png" \
        --hdiutil-quiet \
        "../installers/${DMG_NAME}" \
        "${TMP_DIR}"
else
echo "Creating simple DMG..."
echo "For styled DMG install: brew install create-dmg"

# Create simple DMG
    hdiutil create -volname "${APP_NAME}" \
        -srcfolder "${TMP_DIR}" \
        -ov -format UDZO \
        "../installers/${DMG_NAME}"
fi

# Cleanup
rm -rf "${TMP_DIR}"

echo "DMG image created: ../installers/${DMG_NAME}"
echo ""
echo "User installation:"
echo "   1. Open ${DMG_NAME}"
echo "   2. Drag ${APP_NAME}.app to Applications folder"
echo "   3. Launch ${APP_NAME} from Launchpad or Applications"
echo ""
echo "Security warnings may appear on first launch:"
echo "   System Settings → Security → Allow launching"
echo ""
echo "For app signing (requires Apple Developer Account):"
echo "   codesign --deep --force --verify --verbose --sign 'Developer ID' dist/${APP_NAME}.app"
echo "   codesign --verify --deep --verbose=2 dist/${APP_NAME}.app"
