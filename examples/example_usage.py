"""
Example usage demonstrations for the File Type Identification System.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.filemagic import FileTypeDetector, FileTypeDatabase, MagicNumber


def example_1_basic_detection():
    """Example 1: Basic file type detection."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic File Type Detection")
    print("="*70)
    
    detector = FileTypeDetector()
    
    # Replace with an actual file path on your system
    test_file = input("Enter a file path to analyze: ")
    
    try:
        result = detector.detect_file(test_file)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


def example_2_directory_scan():
    """Example 2: Scanning a directory for mismatches."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Directory Scanning")
    print("="*70)
    
    detector = FileTypeDetector()
    
    # Replace with an actual directory path
    test_dir = input("Enter a directory path to scan: ")
    
    try:
        results = detector.detect_directory(test_dir, recursive=False)
        
        # Filter mismatches
        mismatches = detector.get_mismatches_only(results)
        
        print(f"\nScanned {len(results)} files")
        print(f"Found {len(mismatches)} mismatches\n")
        
        if mismatches:
            print("⚠️  FILES WITH MISMATCHES:")
            for result in mismatches:
                print(f"  - {Path(result.file_path).name}")
                print(f"    Claimed: .{result.claimed_extension}")
                print(f"    Detected: .{result.detected_type}\n")
    except Exception as e:
        print(f"Error: {e}")


def example_3_custom_database():
    """Example 3: Creating a custom signature database."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Signature Database")
    print("="*70)
    
    # Create custom database
    db = FileTypeDatabase()
    
    # Add a custom signature (example: custom file format)
    db.add_signature(
        signature=b'CUSTOM\x00\x01',
        extension='cst',
        description='Custom File Format',
        offset=0,
        mime_type='application/x-custom'
    )
    
    print(f"Database has {len(db)} signatures")
    print(f"Supported extensions: {', '.join(db.get_supported_extensions()[:20])}...")
    
    # Use custom database with detector
    detector = FileTypeDetector(database=db)
    print("\nCustom detector ready!")


def example_4_report_generation():
    """Example 4: Generating analysis reports."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Report Generation")
    print("="*70)
    
    detector = FileTypeDetector()
    
    test_dir = input("Enter a directory path to generate report: ")
    
    try:
        results = detector.detect_directory(test_dir, recursive=True)
        report = detector.generate_report(results)
        print(report)
        
        # Optionally save report to file
        save = input("\nSave report to file? (y/n): ")
        if save.lower() == 'y':
            output_file = "file_analysis_report.txt"
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")


def example_5_programmatic_usage():
    """Example 5: Programmatic usage in your own code."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Programmatic Usage")
    print("="*70)
    
    detector = FileTypeDetector()
    
    test_file = input("Enter a file path: ")
    
    try:
        result = detector.detect_file(test_file)
        
        # Use the result in your code
        if result.is_mismatch:
            print(f"\n🚨 SECURITY ALERT!")
            print(f"File: {result.file_path}")
            print(f"Extension claims: .{result.claimed_extension}")
            print(f"Actually contains: .{result.detected_type}")
            print(f"Description: {result.description}")
            
            # Take action
            action = input("\nQuarantine this file? (y/n): ")
            if action.lower() == 'y':
                print("File would be moved to quarantine...")
                # quarantine_file(result.file_path)
        else:
            print(f"\n✅ File is legitimate")
            print(f"Type: {result.detected_type}")
            print(f"Confidence: {result.confidence}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run example demonstrations."""
    examples = {
        '1': ('Basic Detection', example_1_basic_detection),
        '2': ('Directory Scan', example_2_directory_scan),
        '3': ('Custom Database', example_3_custom_database),
        '4': ('Report Generation', example_4_report_generation),
        '5': ('Programmatic Usage', example_5_programmatic_usage),
    }
    
    print("\n" + "="*70)
    print("FILE TYPE IDENTIFICATION SYSTEM - EXAMPLES")
    print("="*70)
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. Quit")
    
    while True:
        choice = input("\nSelect an example (1-5, q to quit): ").strip()
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        
        if choice in examples:
            _, func = examples[choice]
            func()
            input("\nPress Enter to continue...")
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
