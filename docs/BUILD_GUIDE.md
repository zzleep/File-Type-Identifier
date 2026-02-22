# Building the GUI Executable

This guide explains how to build a standalone executable (.exe) for the File Type Identifier GUI application.

## Prerequisites

- Python 3.7 or higher installed
- All project files in the same directory

## Quick Start

### Option 1: Using the Build Script (Recommended)

Simply double-click one of these files:
- `build_exe.bat` - Batch file (works on all Windows versions)
- `build_exe.ps1` - PowerShell script (more modern)

The script will:
1. Check if PyInstaller is installed (and install it if needed)
2. Build the executable automatically
3. Place the `.exe` file in the `dist` folder

### Option 2: Manual Build

1. **Install PyInstaller:**
   ```powershell
   pip install pyinstaller
   ```

2. **Run the build command:**
   ```powershell
   pyinstaller --name=FileTypeIdentifier --onefile --windowed --add-data="default_signatures.json;." --add-data="src;src" --clean gui.py
   ```

3. **Find your executable:**
   - The executable will be created at: `.\dist\FileTypeIdentifier.exe`

## Running the Application

### GUI Application
- Double-click `gui.py` to run from source, OR
- Double-click `.\dist\FileTypeIdentifier.exe` to run the compiled version

### Command-Line Application
- Run `python main.py` for the CLI version

## Build Options Explained

- `--name=FileTypeIdentifier` - Names the output file
- `--onefile` - Creates a single executable file (not a folder)
- `--windowed` - Hides the console window (GUI only)
- `--add-data` - Includes necessary data files in the executable
- `--clean` - Cleans previous build files

## Advanced Options

### Adding a Custom Icon

1. Get an `.ico` file (e.g., `icon.ico`)
2. Modify the build command:
   ```powershell
   pyinstaller --name=FileTypeIdentifier --onefile --windowed --icon=icon.ico --add-data="default_signatures.json;." --add-data="src;src" gui.py
   ```

### Creating a Console Version

Remove the `--windowed` flag to show console output:
```powershell
pyinstaller --name=FileTypeIdentifier --onefile --add-data="default_signatures.json;." --add-data="src;src" gui.py
```

### Smaller Executable Size

Use UPX compression (requires UPX installed):
```powershell
pyinstaller --name=FileTypeIdentifier --onefile --windowed --upx-dir=C:\path\to\upx --add-data="default_signatures.json;." --add-data="src;src" gui.py
```

## Troubleshooting

### "PyInstaller is not recognized"
- Make sure Python's Scripts folder is in your PATH
- Or use: `python -m PyInstaller` instead of just `pyinstaller`

### "Failed to execute script"
- Check that `default_signatures.json` exists in the project root
- Check that the `src` folder exists with all Python files

### Antivirus False Positive
- PyInstaller executables sometimes trigger antivirus warnings
- This is a known false positive with packed executables
- You can whitelist the file or add a code signing certificate

### Missing Data Files
- Make sure `default_signatures.json` is in the same folder as `gui.py`
- The `--add-data` flag must use semicolon (`;`) on Windows, colon (`:`) on Linux/Mac

## Distribution

The compiled `.exe` file in the `dist` folder is standalone and can be:
- Copied to any Windows computer
- Run without Python installed
- Shared with others

**Note:** The first run might be slower as PyInstaller unpacks files to a temporary directory.

## File Structure After Build

```
FEI/
├── build/                  # Temporary build files (can be deleted)
├── dist/                   # Your executable is here!
│   └── FileTypeIdentifier.exe
├── gui.py                  # GUI source code
├── main.py                 # CLI source code
├── build_exe.bat          # Build script
├── build_exe.ps1          # PowerShell build script
├── FileTypeIdentifier.spec # PyInstaller spec file (can be edited)
└── ...
```

## GUI Features

The GUI application provides:

1. **Single File Analysis Tab**
   - Browse and select individual files
   - Analyze file type using magic numbers
   - Detect mismatches between extension and content

2. **Directory Analysis Tab**
   - Select entire folders to scan
   - Option for recursive subdirectory scanning
   - Comprehensive reports with statistics

3. **Database Info Tab**
   - View all supported file types
   - See database statistics
   - List of 50+ supported extensions

## Need Help?

- For CLI usage: `python main.py --help`
- For GUI: Just launch the application!
- Check `README.md` for more details about the detection system
