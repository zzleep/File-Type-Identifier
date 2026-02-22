# File Type Identifier

A Python tool for detecting file types using magic numbers (file signatures). Useful for security analysis, digital forensics, and verifying file authenticity.

## Features

## Features

- **Modern GUI Application** - User-friendly interface with drag-and-drop support
- **Command-Line Interface** - Perfect for scripting and automation
- **50+ File Types Supported** - Documents, images, archives, executables, media files
- **Mismatch Detection** - Identifies files with incorrect extensions
- **Zero Dependencies** - Uses only Python standard library
- **Cross-Platform** - Works on Windows, Linux, and macOS

## Installation

```bash
git clone https://github.com/yourusername/file-type-identifier.git
cd file-type-identifier
```

No additional dependencies required! Optionally install PyInstaller to build executables:

```bash
pip install -r requirements.txt
```

## Usage

### GUI Application

```bash
python gui.py
```

### CLI Application

```bash
# Analyze a single file
python main.py -f document.pdf

# Analyze a directory
python main.py -d ./downloads

# Recursive scan
python main.py -d ./downloads -r

# Interactive mode
python main.py -i
```

## Building Executable

```bash
pip install pyinstaller
pyinstaller --name=FileTypeIdentifier --onefile --windowed gui.py
```

## Supported File Types

Documents, images, archives, executables, media files, and more. Run `python main.py -l` to see the complete list.

## How It Works

The tool reads the first few bytes of a file (the "magic number" or file signature) and compares it against a database of known signatures. This is more reliable than checking file extensions, which can be easily changed.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.
