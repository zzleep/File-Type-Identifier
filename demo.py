"""
Test script to demonstrate the File Type Identification System capabilities.
Run this to see all features in action.
"""

from src.filemagic import FileTypeDetector, FileTypeDatabase
from pathlib import Path


def scan_and_report(detector, test_dir):
    """Scan test directory and display comprehensive results."""
    results = detector.detect_directory(test_dir)
    
    print(f"\nScanned {len(results)} files:")
    for result in results:
        status = "⚠️ MISMATCH" if result.is_mismatch else "✓ Match"
        print(f"\n{status}: {Path(result.file_path).name}")
        print(f"  Claimed: .{result.claimed_extension or 'NONE'}")
        print(f"  Detected: .{result.detected_type or 'UNKNOWN'}")
        if result.description:
            print(f"  Description: {result.description}")
    
    print("\n3️⃣  MISMATCH SUMMARY")
    print("-" * 70)
    
    if (mismatches := detector.get_mismatches_only(results)):
        print(f"\n🚨 Found {len(mismatches)} suspicious file(s):\n")
        for m in mismatches:
            print(f"📁 {Path(m.file_path).name}")
            print(f"   Claims: .{m.claimed_extension}")
            print(f"   Actually: .{m.detected_type} ({m.description})")
            print()
    else:
        print("✅ No mismatches found - all files are legitimate!")
    
    print("\n4️⃣  DETAILED REPORT")
    print("-" * 70)
    report = detector.generate_report(results)
    print(report)


def main():
    print("=" * 70)
    print("FILE TYPE IDENTIFICATION SYSTEM - DEMONSTRATION")
    print("=" * 70)
    
    detector = FileTypeDetector()
    
    print("\n1️⃣  SUPPORTED FILE TYPES")
    print("-" * 70)
    print(f"Total signatures: {len(detector.database)}")
    extensions = detector.database.get_supported_extensions()
    print(f"Extensions: {', '.join(extensions[:15])}...")
    
    print("\n2️⃣  SCANNING TEST DIRECTORY")
    print("-" * 70)
    
    test_dir = "test_samples"
    if (test_path := Path(test_dir)).exists():
        scan_and_report(detector, test_dir)
    else:
        print(f"Test directory '{test_dir}' not found.")
        print("Run the main.py program first to create test files.")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nTry these commands:")
    print("  python main.py -l              # List all supported types")
    print("  python main.py -i              # Interactive mode")
    print("  python main.py -f <file>       # Analyze a file")
    print("  python main.py -d <directory>  # Scan directory")
    print("=" * 70)


if __name__ == "__main__":
    main()
