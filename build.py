"""
Script for building LinguaGPT into an executable file
"""

import os
import sys
import subprocess

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

def check_qt6_libraries():
    """Check if Qt6 libraries are available on Linux"""
    if not is_linux:
        return True
    
    required_libs = [
        'libQt6Core.so.6',
        'libQt6Gui.so.6', 
        'libQt6Widgets.so.6'
    ]
    
    for lib in required_libs:
        result = subprocess.run(['ldconfig', '-p'], capture_output=True, text=True)
        if lib not in result.stdout:
            try:
                print(f"[ERROR] Missing Qt6 library: {lib}")
            except UnicodeEncodeError:
                print(f"[ERROR] Missing Qt6 library: {lib}")
            return False
    
    try:
        print("[INFO] Qt6 libraries found")
    except UnicodeEncodeError:
        print("[INFO] Qt6 libraries found")
    return True

# PyInstaller parameters - simplified and more reliable
pyinstaller_args = [
    main_script,
    f"--name={app_name}",
    "--onefile",
    "--windowed",
    "--clean",
    "--noconfirm",
    # Only exclude modules that are definitely not needed
    "--exclude-module=PyQt6.QtMultimedia",
    "--exclude-module=PyQt6.QtWebEngine",
    "--exclude-module=PyQt6.Qt3D",
    "--exclude-module=PyQt6.QtQuick3D",
    "--exclude-module=PyQt6.QtBluetooth",
    "--exclude-module=PyQt6.QtPositioning",
    "--exclude-module=PyQt6.QtSensors",
    "--exclude-module=PyQt6.QtSerialPort",
    "--exclude-module=PyQt6.QtWebChannel",
    "--exclude-module=PyQt6.QtWebSockets",
    "--exclude-module=PyQt6.QtTextToSpeech",
    "--exclude-module=PyQt6.QtNfc",
    "--exclude-module=PyQt6.QtSpatialAudio",
]

# Essential hidden imports
pyinstaller_args.extend([
    "--hidden-import=PyQt6.QtCore",
    "--hidden-import=PyQt6.QtGui",
    "--hidden-import=PyQt6.QtWidgets",
    "--hidden-import=PyQt6.QtNetwork",
    "--hidden-import=PyQt6.QtPrintSupport",
    "--hidden-import=PyQt6.QtSvg",
])

# Add platform-specific configurations
if is_linux:
    if is_github_actions:
        try:
            print("[CONFIG] Configuring for GitHub Actions Linux environment")
        except UnicodeEncodeError:
            print("[CONFIG] Configuring for GitHub Actions Linux environment")
        
        # Add Qt6 runtime path for GitHub Actions
        qt6_path = "/usr/lib/x86_64-linux-gnu"
        if os.path.exists(qt6_path):
            # Try to find Qt6 libraries with different naming conventions
            qt_libs = [
                "libQt6Core.so.6", "libQt6Gui.so.6", "libQt6Widgets.so.6",
                "libQt6Network.so.6", "libQt6PrintSupport.so.6", "libQt6Svg.so.6"
            ]
            
            for lib in qt_libs:
                lib_path = f"{qt6_path}/{lib}"
                if os.path.exists(lib_path):
                    pyinstaller_args.append(f"--add-binary={lib_path}:.")
                else:
                    try:
                        print(f"[WARNING] Library not found: {lib_path}")
                    except UnicodeEncodeError:
                        print(f"[WARNING] Library not found: {lib_path}")
    
    # Add essential Qt6 plugins for Linux
    pyinstaller_args.extend([
        "--collect-binaries=PyQt6.Qt6.plugins.platforms",
        "--collect-binaries=PyQt6.Qt6.plugins.platformthemes",
        "--collect-binaries=PyQt6.Qt6.plugins.styles",
        "--collect-binaries=PyQt6.Qt6.plugins.iconengines",
        "--collect-binaries=PyQt6.Qt6.plugins.imageformats",
    ])

elif is_windows:
    pyinstaller_args.extend([
        "--collect-binaries=PyQt6.Qt6.plugins.platforms",
        "--collect-binaries=PyQt6.Qt6.plugins.styles",
        "--collect-binaries=PyQt6.Qt6.plugins.iconengines",
        "--collect-binaries=PyQt6.Qt6.plugins.imageformats",
    ])

elif is_mac:
    pyinstaller_args.extend([
        "--collect-binaries=PyQt6.Qt6.plugins.platforms",
        "--collect-binaries=PyQt6.Qt6.plugins.styles",
        "--collect-binaries=PyQt6.Qt6.plugins.iconengines",
        "--collect-binaries=PyQt6.Qt6.plugins.imageformats",
    ])

# Start build
try:
    print(f"[BUILD] Building {app_name} for {sys.platform}...")
    print(f"[BUILD] Parameters: {' '.join(pyinstaller_args)}")
except UnicodeEncodeError:
    # Fallback for Windows consoles without Unicode support
    print(f"[BUILD] Building {app_name} for {sys.platform}...")
    print("[BUILD] Parameters configured successfully")

# Check Qt6 libraries on Linux
if is_linux and not check_qt6_libraries():
    print("[WARNING] Some Qt6 libraries are missing. Build may fail.")

try:
    PyInstaller.__main__.run(pyinstaller_args)
    
    try:
        print(f"\n[SUCCESS] Build completed successfully!")
    except UnicodeEncodeError:
        print("\n[SUCCESS] Build completed successfully!")

    if is_windows:
        try:
            print(f"[INFO] Executable file: dist/{app_name}.exe")
        except UnicodeEncodeError:
            print(f"[INFO] Executable file: dist/{app_name}.exe")
    elif is_mac:
        try:
            print(f"[INFO] Application: dist/{app_name}.app")
        except UnicodeEncodeError:
            print(f"[INFO] Application: dist/{app_name}.app")
    else:
        try:
            print(f"[INFO] Executable file: dist/{app_name}")
        except UnicodeEncodeError:
            print(f"[INFO] Executable file: dist/{app_name}")

    try:
        print("\n[INFO] You can now distribute application!")
    except UnicodeEncodeError:
        print("\n[INFO] You can now distribute application!")

except Exception as e:
    try:
        print(f"\n[ERROR] Build error: {e}")
    except UnicodeEncodeError:
        print(f"\n[ERROR] Build error occurred")
    
    if is_github_actions:
        print("[INFO] This is a known issue with GitHub Actions Qt6 environment.")
        print("[INFO] The build artifacts may still work despite warnings.")
    sys.exit(1)