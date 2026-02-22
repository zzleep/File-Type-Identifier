# Online Database Guide

## 📚 **Getting Magic Number Databases Online**

Yes! You can absolutely get magic number databases from online sources. This system now supports importing, exporting, and managing custom signature databases.

---

## 🌐 **Popular Online Sources**

### 1. **Gary Kessler's File Signatures Database**
- **URL:** https://www.garykessler.net/library/file_sigs.html
- **Format:** HTML table
- **Coverage:** 500+ file signatures
- **Quality:** ⭐⭐⭐⭐⭐ (Highly maintained, industry standard)

### 2. **Wikipedia - List of File Signatures**
- **URL:** https://en.wikipedia.org/wiki/List_of_file_signatures
- **Format:** HTML table
- **Coverage:** 200+ common signatures
- **Quality:** ⭐⭐⭐⭐ (Community maintained, well-documented)

### 3. **FileSignatures.net**
- **URL:** https://filesignatures.net/
- **Format:** HTML
- **Coverage:** 1000+ signatures
- **Quality:** ⭐⭐⭐⭐

### 4. **GitHub Repositories**
- **python-magic** - https://github.com/ahupp/python-magic
- **file-type** - https://github.com/sindresorhus/file-type
- **TrID** database - http://mark0.net/soft-trid-e.html

### 5. **Forensics Wikis**
- **ForensicsWiki** - https://forensicswiki.xyz/wiki/index.php?title=File_Formats
- **NIST NSRL** - https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl

---

## 🛠️ **Database Management Tool**

We've created a powerful tool to manage magic number databases:

### **Basic Commands**

```bash
# Export default database to JSON
python manage_database.py export my_signatures.json

# Create example custom database file
python manage_database.py example

# Import custom database
python manage_database.py import custom_signatures.json

# List all signatures in a database
python manage_database.py list
python manage_database.py list custom_signatures.json

# Merge two databases
python manage_database.py merge default.json custom.json merged.json

# Show available online sources
python manage_database.py sources
```

---

## 📝 **JSON Database Format**

Here's the format for custom signature databases:

```json
{
  "version": "1.0",
  "replace_defaults": false,
  "signatures": [
    {
      "signature": "FFD8FF",
      "extension": "jpg",
      "description": "JPEG Image",
      "offset": 0,
      "mime_type": "image/jpeg"
    },
    {
      "signature": "89504E470D0A1A0A",
      "extension": "png",
      "description": "PNG Image",
      "offset": 0,
      "mime_type": "image/png"
    }
  ]
}
```

### **Field Descriptions:**

- **signature**: Hex string of the magic number (no spaces, or space-separated)
- **extension**: File extension without the dot
- **description**: Human-readable description
- **offset**: Byte offset where signature appears (usually 0)
- **mime_type**: MIME type (optional)
- **replace_defaults**: If true, replaces built-in signatures

---

## 🔄 **Workflow for Adding Online Databases**

### **Method 1: Manual Conversion**

1. Visit an online source (e.g., Gary Kessler's database)
2. Copy the signatures you need
3. Export default database:
   ```bash
   python manage_database.py export my_db.json
   ```
4. Edit the JSON file to add new signatures
5. Import updated database:
   ```bash
   python manage_database.py import my_db.json
   ```

### **Method 2: Create Custom Database**

1. Create example file:
   ```bash
   python manage_database.py example
   ```
2. Edit `custom_signatures.json`
3. Add your signatures in JSON format
4. Test import:
   ```bash
   python manage_database.py import custom_signatures.json
   ```

### **Method 3: Merge Databases**

1. Export default:
   ```bash
   python manage_database.py export default.json
   ```
2. Create custom additions:
   ```bash
   python manage_database.py example my_additions.json
   ```
3. Merge them:
   ```bash
   python manage_database.py merge default.json my_additions.json final.json
   ```

---

## 💻 **Using Custom Databases in Code**

### **Python API**

```python
from src.filemagic import FileTypeDetector
from src.filemagic.online_database import OnlineDatabaseFetcher

# Method 1: Load from JSON file
fetcher = OnlineDatabaseFetcher()
custom_db = fetcher.load_from_file('custom_signatures.json')

# Create detector with custom database
detector = FileTypeDetector(database=custom_db)

# Use normally
result = detector.detect_file('suspicious.exe')
print(result)

# Method 2: Merge with default
from src.filemagic import FileTypeDatabase

default_db = FileTypeDatabase()
custom_db = fetcher.load_from_file('additions.json')
merged_db = fetcher.merge_databases(default_db, custom_db)

detector = FileTypeDetector(database=merged_db)
```

---

## 🎯 **Common Use Cases**

### **Case 1: Add Rare File Types**

You encounter a specialized file format not in the default database:

```bash
# Export default database
python manage_database.py export base.json

# Edit base.json to add:
{
  "signature": "4D546864",
  "extension": "mid",
  "description": "MIDI Audio File",
  "offset": 0,
  "mime_type": "audio/midi"
}

# Import and test
python manage_database.py import base.json
python main.py -f myfile.mid
```

### **Case 2: Forensics Investigation**

You need comprehensive coverage for forensic analysis:

```bash
# Start with default
python manage_database.py export forensics_base.json

# Add specialized forensics signatures from:
# - NIST database
# - ForensicsWiki
# - Case-specific malware signatures

# Import comprehensive database
python manage_database.py import forensics_base.json

# Scan evidence directory
python main.py -d evidence_folder -r
```

### **Case 3: Security Scanning**

Focus on executable and potentially dangerous file types:

```json
{
  "version": "1.0",
  "replace_defaults": false,
  "signatures": [
    {
      "signature": "4D5A",
      "extension": "exe",
      "description": "Windows PE Executable",
      "offset": 0,
      "mime_type": "application/x-msdownload"
    },
    {
      "signature": "7F454C46",
      "extension": "elf",
      "description": "Linux ELF Executable",
      "offset": 0,
      "mime_type": "application/x-executable"
    },
    {
      "signature": "23212F",
      "extension": "sh",
      "description": "Shell Script",
      "offset": 0,
      "mime_type": "text/x-shellscript"
    }
  ]
}
```

---

## 📊 **Database Statistics**

The default database includes:

- **43 signatures**
- **33 unique file extensions**
- Categories:
  - Documents (5 types)
  - Images (8 types)
  - Archives (8 types)
  - Executables (5 types)
  - Audio (5 types)
  - Video (5 types)
  - Other (7 types)

---

## 🔒 **Security Considerations**

When using online databases:

1. **Verify Sources** - Only use trusted sources
2. **Test Signatures** - Validate with known files
3. **Avoid Duplicates** - Use merge tool to prevent conflicts
4. **Keep Updated** - Regularly update from sources
5. **Backup** - Keep copies of working databases

---

## 🧪 **Testing Custom Databases**

```bash
# Create test database
python manage_database.py example test_db.json

# Import with validation
python manage_database.py import test_db.json

# List signatures to verify
python manage_database.py list test_db.json

# Test with actual files
python main.py -f test_file.pdf
python main.py -d test_folder
```

---

## 📦 **Exporting for Distribution**

Share your custom database with others:

```bash
# Export your enhanced database
python manage_database.py export my_enhanced_db.json

# Share the JSON file
# Others can import it:
python manage_database.py import my_enhanced_db.json
```

---

## 🌟 **Pro Tips**

1. **Keep it Organized**: Group signatures by category in your JSON
2. **Document Sources**: Add comments (in description) about where you got signatures
3. **Test Everything**: Always test new signatures with real files
4. **Version Control**: Keep your custom databases in git
5. **Incremental Updates**: Use merge instead of replacing entire databases

---

## 📚 **Additional Resources**

### **Online Tools**
- **HexEd.it** - Online hex editor to examine files
- **File Signature Verifier** - Online signature checker

### **Research Papers**
- "File Type Identification using Magic Numbers" - NIST
- "Digital Forensics File Analysis" - SANS Institute

### **Community Resources**
- Stack Overflow - File signature questions
- Reddit r/computerforensics
- Digital Forensics Discord servers

---

## 🤝 **Contributing Your Signatures**

If you discover new or rare file signatures:

1. Document the signature thoroughly
2. Test with multiple file samples
3. Export to JSON format
4. Share with the community

---

## ⚡ **Quick Reference**

| Task | Command |
|------|---------|
| Export default | `python manage_database.py export db.json` |
| Create example | `python manage_database.py example` |
| Import custom | `python manage_database.py import db.json` |
| List signatures | `python manage_database.py list db.json` |
| Merge databases | `python manage_database.py merge db1.json db2.json out.json` |
| Show sources | `python manage_database.py sources` |

---

**Last Updated:** February 15, 2026  
**Version:** 1.0  
**Compatibility:** Python 3.7+
