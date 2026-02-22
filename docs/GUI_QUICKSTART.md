# Quick Start - GUI Application

## Running the GUI (Without Building)

Just run:
```powershell
python gui.py
```

## Building the Executable

### Easy Method (Double-click):
1. Double-click `build_exe.bat`
2. Wait for the build to complete
3. Find your executable at `dist\FileTypeIdentifier.exe`

### Command Line Method:
```powershell
# Install PyInstaller
pip install pyinstaller

# Build the executable
pyinstaller --name=FileTypeIdentifier --onefile --windowed --add-data="default_signatures.json;." --add-data="src;src" --clean gui.py
```

## Using the GUI

### Tab 1: Single File Analysis
1. Click "Browse..." to select a file
2. Click "🔍 Analyze File"
3. View results in the text area below
4. If there's a mismatch, you'll see a warning ⚠️

### Tab 2: Directory Analysis
1. Click "Browse..." to select a folder
2. Check "Include subdirectories" for recursive scan (optional)
3. Click "🔍 Analyze Directory"
4. View comprehensive results with statistics

### Tab 3: Database Info
- See all 50+ supported file types
- View database statistics
- Check which extensions are supported

## Features

✅ User-friendly graphical interface
✅ Drag-and-drop file selection (via Browse button)
✅ Recursive directory scanning
✅ Real-time analysis with progress updates
✅ Mismatch detection warnings
✅ Detailed reports and statistics
✅ No installation required (once built as .exe)

## Distribution

After building, you can:
- Share `dist\FileTypeIdentifier.exe` with anyone
- It works on any Windows PC (no Python needed!)
- Single file, easy to distribute
