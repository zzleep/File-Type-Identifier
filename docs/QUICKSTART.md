# Quick Start Guide - File Type Identification System

## 🚀 Getting Started

### Installation
No installation required! This project uses only Python's standard library.

**Requirements:**
- Python 3.7 or higher

### Basic Usage

#### 1. Analyze a Single File
```bash
python main.py -f path/to/suspicious_file.exe
```

#### 2. Scan a Directory
```bash
python main.py -d path/to/directory
```

#### 3. Scan Recursively
```bash
python main.py -d path/to/directory -r
```

#### 4. List Supported File Types
```bash
python main.py -l
```

#### 5. Interactive Mode
```bash
python main.py -i
```

## 📊 Example Output

### Detecting a Mismatch
```
======================================================================
File: suspicious_document.pdf.exe
Status: ⚠️ MISMATCH
Claimed Extension: .exe
Detected Type: .pdf
Confidence: HIGH
Description: Portable Document Format
MIME Type: application/pdf
File Size: 245,760 bytes
======================================================================

⚠️  WARNING: This file may be disguised or corrupted!
    The file extension doesn't match the actual content.
```

### Directory Scan Report
```
======================================================================
FILE TYPE IDENTIFICATION REPORT
======================================================================

Total Files Analyzed: 15
Matches: 13 ✓
Mismatches: 2 ⚠️
Success Rate: 86.7%

======================================================================

MISMATCHED FILES (POTENTIAL SECURITY RISK):
[Details of mismatched files...]
```

## 💻 Using as a Python Library

```python
from src.filemagic import FileTypeDetector

# Initialize detector
detector = FileTypeDetector()

# Analyze a file
result = detector.detect_file("suspicious.exe")

# Check for mismatch
if result.is_mismatch:
    print(f"Warning: {result.file_path}")
    print(f"Claims to be: .{result.claimed_extension}")
    print(f"Actually is: .{result.detected_type}")
    # Take appropriate action...

# Scan directory
results = detector.detect_directory("./downloads", recursive=True)

# Filter mismatches
mismatches = detector.get_mismatches_only(results)
print(f"Found {len(mismatches)} suspicious files")

# Generate report
report = detector.generate_report(results)
print(report)
```

## 🔧 Advanced Usage

### Custom Magic Number Database

```python
from src.filemagic import FileTypeDatabase, FileTypeDetector

# Create custom database
db = FileTypeDatabase()

# Add your own signature
db.add_signature(
    signature=b'\x4D\x5A',  # 'MZ' - Windows executable
    extension='exe',
    description='Windows Executable',
    offset=0,
    mime_type='application/x-msdownload'
)

# Use with detector
detector = FileTypeDetector(database=db)
```

### Configuring Read Size

```python
# Read more bytes for complex signatures
detector = FileTypeDetector(max_read_bytes=16384)  # 16 KB
```

## 🔍 Security Use Cases

### 1. Email Attachment Scanning
```python
def scan_email_attachment(file_path):
    detector = FileTypeDetector()
    result = detector.detect_file(file_path)
    
    if result.is_mismatch:
        # Block suspicious attachment
        quarantine_file(file_path)
        alert_admin(result)
        return False
    return True
```

### 2. Upload Validation
```python
def validate_upload(uploaded_file, expected_type):
    detector = FileTypeDetector()
    result = detector.detect_file(uploaded_file)
    
    if result.detected_type != expected_type:
        raise SecurityException("File type mismatch detected")
    
    return result
```

### 3. Forensic Analysis
```python
def analyze_evidence_directory(evidence_path):
    detector = FileTypeDetector()
    results = detector.detect_directory(evidence_path, recursive=True)
    
    # Generate forensic report
    report = detector.generate_report(results)
    
    # Save report
    with open("forensic_report.txt", "w") as f:
        f.write(report)
    
    return results
```

### 4. Automated Malware Detection
```python
def detect_disguised_malware(directory):
    detector = FileTypeDetector()
    results = detector.detect_directory(directory, recursive=True)
    mismatches = detector.get_mismatches_only(results)
    
    for result in mismatches:
        if result.detected_type == 'exe':
            print(f"⚠️  Potential malware: {result.file_path}")
            print(f"   Disguised as: .{result.claimed_extension}")
            # Quarantine and analyze further
```

## 🎯 Supported File Types

### Documents
- PDF, DOC, DOCX, XLSX, PPTX

### Images
- JPEG/JPG, PNG, GIF, BMP, TIFF, WebP

### Archives
- ZIP, RAR, GZIP, 7Z, BZIP2

### Executables
- EXE (Windows), ELF (Linux), Class (Java), Mach-O (macOS)

### Audio
- MP3, WAV, FLAC, OGG

### Video
- MP4, AVI, MKV, FLV

### Database
- SQLite

### Other
- HTML, XML, JSON

## 🛡️ Best Practices

1. **Regular Scanning**: Schedule periodic scans of critical directories
2. **Upload Validation**: Always validate file types on upload
3. **Quarantine Mismatches**: Isolate suspicious files for further analysis
4. **Logging**: Keep logs of all detections for audit trails
5. **Whitelist Known Files**: Maintain a database of verified files
6. **Update Signatures**: Regularly update the magic number database

## 🐛 Troubleshooting

### File Not Detected
- Check if file type is in supported list (`python main.py -l`)
- Ensure file has enough bytes (minimum 8 bytes typically)
- Add custom signature if needed

### Permission Errors
- Run with appropriate permissions
- Check file/directory access rights

### False Positives
- Some formats share signatures (e.g., ZIP-based formats: DOCX, XLSX, PPTX)
- The system handles common aliases (jpg/jpeg) automatically
- Add custom logic for specific cases

## 📈 Performance Tips

1. **Limit Read Size**: Use smaller `max_read_bytes` for faster scans
2. **Non-Recursive Scans**: Avoid recursive scanning for large directories
3. **Batch Processing**: Process files in batches for large datasets
4. **Filter by Extension**: Pre-filter files before scanning

## 🔗 Resources

- See `examples/example_usage.py` for more detailed examples
- See `README.md` for complete documentation
- Source code is fully commented and self-documenting

## 📞 Support

For issues or questions:
1. Check the examples directory
2. Review the source code documentation
3. Test with the provided sample files

---

**Version:** 1.0.0
**Author:** Cybersec FEI Team
**License:** Educational/Cybersecurity Use
