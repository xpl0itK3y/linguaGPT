"""
Script for building LinguaGPT into an executable file
"""

import os
import sys

import PyInstaller.__main__

# Detect operating system
is_windows = sys.platform.startswith("win")
is_mac = sys.platform == "darwin"
is_linux = sys.platform.startswith("linux")

# Check if running on GitHub Actions
is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'

# Basic parameters
app_name = "LinguaGPT"
main_script = "main.py"

# PyInstaller parameters - optimized for GitHub Actions
pyinstaller_args = [
    main_script,
    f"--name={app_name}",
    "--onefile",  # Single executable file
    "--windowed",  # No console (GUI application)
    "--clean",
    "--noconfirm",
    # Exclude problematic Qt6 modules that cause dependency issues
    "--exclude-module=PyQt6.QtMultimedia",
    "--exclude-module=PyQt6.QtWebEngine",
    "--exclude-module=PyQt6.Qt3D",
    "--exclude-module=PyQt6.QtSpatialAudio",
    "--exclude-module=PyQt6.QtNfc",
    "--exclude-module=PyQt6.QtTextToSpeech",
    "--exclude-module=PyQt6.QtQuick3D",
    "--exclude-module=PyQt6.QtQuick3DHelpers",
    "--exclude-module=PyQt6.QtQuick3DAssetUtils",
    "--exclude-module=PyQt6.QtQuick3DEffects",
    "--exclude-module=PyQt6.QtQuick3DParticleEffects",
    "--exclude-module=PyQt6.QtQuick3DRuntimeRender",
    "--exclude-module=PyQt6.QtQuick3DUtils",
    # Additional exclusions for GitHub Actions compatibility
    "--exclude-module=PyQt6.QtSql",
    "--exclude-module=PyQt6.QtNetwork",
    "--exclude-module=PyQt6.QtBluetooth",
    "--exclude-module=PyQt6.QtPositioning",
    "--exclude-module=PyQt6.QtSensors",
    "--exclude-module=PyQt6.QtSerialPort",
    "--exclude-module=PyQt6.QtWebChannel",
    "--exclude-module=PyQt6.QtWebSockets",
]

# Add icon if available (optional)
# if os.path.exists('resources/icon.ico'):
#     pyinstaller_args.append('--icon=resources/icon.ico')

# Additional data to include - focus only on essential modules
pyinstaller_args.extend(
    [
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--collect-data=PyQt6",
        "--collect-submodules=PyQt6",
        # Add specific plugins needed for basic GUI functionality
        # Only essential plugins to avoid missing dependencies
        "--collect-binaries=PyQt6.Qt6.plugins.platforms",
        "--collect-binaries=PyQt6.Qt6.plugins.styles",
        "--collect-binaries=PyQt6.Qt6.plugins.iconengines",
        "--collect-binaries=PyQt6.Qt6.plugins.imageformats",
        # Add plugin exclusion NOTES: This parameter does not exist in PyInstaller 6.3.0
        # "--exclude-unused-plugins",
    ]
)

# Start build
print(f"🚀 Building {app_name} for {sys.platform}...")
print(f"📦 Parameters: {' '.join(pyinstaller_args)}")

try:
    PyInstaller.__main__.run(pyinstaller_args)
    print(f"\n✅ Build completed successfully!")

    if is_windows:
        print(f"📁 Executable file: dist/{app_name}.exe")
    elif is_mac:
        print(f"📁 Application: dist/{app_name}.app")
    else:
        print(f"📁 Executable file: dist/{app_name}")

    print("\n💡 You can now distribute the application!")

except Exception as e:
    print(f"\n❌ Build error: {e}")
    sys.exit(1)
