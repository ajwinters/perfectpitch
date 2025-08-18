"""
Setup script for building Perfect Pitch Trainer executable.
"""

import os
import sys
from pathlib import Path

# PyInstaller spec file content
SPEC_CONTENT = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
    ],
    hiddenimports=[
        'pygame',
        'pygame.midi',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'pandas',
        'numpy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyi_splash = Splash(
    'resources/splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

pyi = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyi,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    pyi_splash.binaries,
    [],
    name='PerfectPitchTrainer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico'
)
"""

def create_build_structure():
    """Create necessary directories for building."""
    directories = [
        'build',
        'dist',
        'resources'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def create_spec_file():
    """Create PyInstaller spec file."""
    with open('PerfectPitchTrainer.spec', 'w', encoding='utf-8') as f:
        f.write(SPEC_CONTENT)
    print("Created PyInstaller spec file")

def create_build_script():
    """Create build script."""
    if sys.platform == "win32":
        script_content = """@echo off
echo Building Perfect Pitch Trainer executable...
echo.

echo Installing/updating dependencies...
pip install -r requirements_new.txt
echo.

echo Building executable with PyInstaller...
pyinstaller PerfectPitchTrainer.spec --clean
echo.

echo Build complete! Check the dist folder for the executable.
pause
"""
        script_name = "build.bat"
    else:
        script_content = """#!/bin/bash
echo "Building Perfect Pitch Trainer executable..."
echo

echo "Installing/updating dependencies..."
pip install -r requirements_new.txt
echo

echo "Building executable with PyInstaller..."
pyinstaller PerfectPitchTrainer.spec --clean
echo

echo "Build complete! Check the dist folder for the executable."
"""
        script_name = "build.sh"
    
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    if sys.platform != "win32":
        os.chmod(script_name, 0o755)
    
    print(f"Created build script: {script_name}")

def create_readme():
    """Create README for the project."""
    readme_content = """# Perfect Pitch Trainer

A comprehensive application for training perfect pitch recognition with advanced note and octave identification.

## Features

- **Configurable Training**: Choose from various note groups (All notes, C Major, Guitar tuning, etc.) or create custom selections
- **Full Octave Training**: Identify both note names and octaves, not just note names
- **Practice Keyboard**: Play any note to familiarize yourself with different octaves
- **Data Tracking**: Automatic recording of all training attempts with detailed analytics
- **Progress Monitoring**: Real-time statistics and session tracking
- **Export Capabilities**: Export training data for external analysis

## Installation

### From Source
1. Install Python 3.7 or higher
2. Install dependencies:
   ```
   pip install -r requirements_new.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

### Pre-built Executable
1. Download the latest release from the releases page
2. Extract the files
3. Run `PerfectPitchTrainer.exe` (Windows) or equivalent for your platform

## Building Executable

To build your own executable:

1. Install build dependencies:
   ```
   pip install pyinstaller
   ```

2. Run the build script:
   - Windows: `build.bat`
   - macOS/Linux: `./build.sh`

3. Find the executable in the `dist` folder

## Usage

1. **Configure Training**: Go to Settings > Training Configuration to select:
   - Note groups (All, C Major, Guitar tuning, etc.)
   - Octave range (2-7 by default)
   - MIDI instrument for playback

2. **Training Process**:
   - Listen to the played note
   - Select the correct note name and octave from the grid
   - Get immediate feedback
   - Track your progress in the status bar

3. **Practice Mode**: Use the practice keyboard to play any note and familiarize yourself with different octaves

4. **Analytics**: 
   - View real-time statistics in the status bar
   - Export session data via File > Export Session Data
   - Use the analytics tools in the `analytics` folder for detailed analysis

## Project Structure

```
perfectpitch/
├── app.py                 # Main application entry point
├── src/
│   ├── config.py         # Configuration and constants
│   ├── audio/
│   │   └── player.py     # MIDI audio playback
│   ├── data/
│   │   └── manager.py    # Data recording and management
│   └── ui/
│       ├── main_window.py      # Main application window
│       └── settings_dialog.py  # Settings configuration
├── analytics/
│   └── analyzer.py       # Data analysis and visualization tools
├── data/                 # Training data storage
└── build/               # Build artifacts and resources
```

## Requirements

- Python 3.7+
- PyQt5 (GUI framework)
- pygame (MIDI playback)
- pandas (data management)
- matplotlib & seaborn (analytics - optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Troubleshooting

**MIDI Issues**: 
- Ensure you have a working MIDI synthesizer
- On Windows, the built-in Windows MIDI synthesizer should work
- On macOS/Linux, you may need to install additional MIDI software

**Audio Not Playing**:
- Check your system's audio settings
- Ensure pygame can access MIDI output devices
- Try different MIDI instruments in the settings

**Performance Issues**:
- Close other audio applications
- Reduce the octave range in settings
- Use simpler note groups for training
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("Created README.md")

def main():
    """Main setup function."""
    print("Setting up Perfect Pitch Trainer build environment...")
    
    create_build_structure()
    create_spec_file() 
    create_build_script()
    create_readme()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements_new.txt")
    print("2. Test the application: python app.py")
    print("3. Build executable: run build.bat (Windows) or ./build.sh (Unix)")

if __name__ == "__main__":
    main()
