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

# Basic parameters
app_name = "LinguaGPT"
main_script = "main.py"

# PyInstaller parameters
pyinstaller_args = [
    main_script,
    f"--name={app_name}",
    "--onefile",  # Single executable file
    "--windowed",  # No console (GUI application)
    "--clean",
    "--noconfirm",
]

# Add icon if available (optional)
# if os.path.exists('resources/icon.ico'):
#     pyinstaller_args.append('--icon=resources/icon.ico')

# Additional data to include
pyinstaller_args.extend(
    [
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--collect-all=PyQt6",
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
