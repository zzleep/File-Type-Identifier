"""
Main entry point for the File Type Identification System.
Provides a command-line interface for detecting file types and mismatches.
"""

import sys
import argparse
from pathlib import Path
from typing import List

from src.filemagic import FileTypeDetector, FileTypeDatabase


def analyze_single_file(file_path: str, detector: FileTypeDetector):
    """Analyze a single file and display results."""
    try:
        result = detector.detect_file(file_path)
        print(result)
        
        if result.is_mismatch:
            print("⚠️  WARNING: This file may be disguised or corrupted!")
            print("    The file extension doesn't match the actual content.")
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
    except PermissionError:
        print(f"❌ Error: Permission denied: {file_path}")
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")


def analyze_directory(dir_path: str, detector: FileTypeDetector, recursive: bool = False):
    """Analyze all files in a directory."""
    try:
        print(f"\n🔍 Scanning directory: {dir_path}")
        print(f"   Recursive: {'Yes' if recursive else 'No'}\n")
        
        results = detector.detect_directory(dir_path, recursive=recursive)
        
        if not results:
            print("No files found to analyze.")
            return
        
        # Generate and display report
        report = detector.generate_report(results)
        print(report)
        
        # Display individual results
        print("\nDETAILED RESULTS:")
        print("=" * 70)
        for result in results:
            status_icon = "⚠️" if result.is_mismatch else "✓"
            print(f"{status_icon} {result.file_path}")
            print(f"   Claimed: .{result.claimed_extension or 'NONE'} | "
                  f"Detected: .{result.detected_type or 'UNKNOWN'}")
            if result.is_mismatch:
                print("   🚨 MISMATCH DETECTED!")
            print()
        
    except FileNotFoundError:
        print(f"❌ Error: Directory not found: {dir_path}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error analyzing directory: {e}")


def list_supported_types(detector: FileTypeDetector):
    """Display all supported file types."""
    extensions = detector.database.get_supported_extensions()
    
    print("\n📋 SUPPORTED FILE TYPES")
    print("=" * 70)
    print(f"Total signatures in database: {len(detector.database)}")
    print(f"Unique file extensions: {len(extensions)}")
    print("\nExtensions:")
    
    # Display in columns
    col_width = 15
    cols = 4
    for i in range(0, len(extensions), cols):
        row = extensions[i:i+cols]
        print("  " + "".join(f".{ext:<{col_width}}" for ext in row))
    
    print("\n" + "=" * 70)


def interactive_mode(detector: FileTypeDetector):
    """Run in interactive mode."""
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("Commands:")
    print("  file <path>     - Analyze a single file")
    print("  dir <path>      - Analyze a directory")
    print("  dirr <path>     - Analyze a directory recursively")
    print("  list            - List supported file types")
    print("  quit            - Exit")
    print("=" * 70)
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            
            if cmd in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            
            elif cmd == 'list':
                list_supported_types(detector)
            
            elif cmd == 'file' and len(parts) > 1:
                analyze_single_file(parts[1], detector)
            
            elif cmd == 'dir' and len(parts) > 1:
                analyze_directory(parts[1], detector, recursive=False)
            
            elif cmd == 'dirr' and len(parts) > 1:
                analyze_directory(parts[1], detector, recursive=True)
            
            else:
                print("❌ Invalid command. Type 'quit' to exit.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="File Type Identification System using Magic Numbers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -f document.pdf              # Analyze single file
  python main.py -d ./downloads               # Analyze directory
  python main.py -d ./downloads -r            # Analyze directory recursively
  python main.py -l                           # List supported file types
  python main.py -i                           # Interactive mode
        """
    )
    
    parser.add_argument('-f', '--file', help='Analyze a single file')
    parser.add_argument('-d', '--directory', help='Analyze all files in a directory')
    parser.add_argument('-r', '--recursive', action='store_true', 
                       help='Recursively analyze subdirectories')
    parser.add_argument('-l', '--list', action='store_true', 
                       help='List all supported file types')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Display header
    print("\n" + "=" * 70)
    print("FILE TYPE IDENTIFICATION SYSTEM")
    print("Magic Number Based Detection")
    print("=" * 70)
    
    # Initialize detector
    detector = FileTypeDetector()
    
    # Process arguments
    if args.list:
        list_supported_types(detector)
    
    elif args.file:
        analyze_single_file(args.file, detector)
    
    elif args.directory:
        analyze_directory(args.directory, detector, args.recursive)
    
    elif args.interactive:
        interactive_mode(detector)
    
    else:
        # No arguments - show help and enter interactive mode
        parser.print_help()
        print("\nEntering interactive mode...\n")
        interactive_mode(detector)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
