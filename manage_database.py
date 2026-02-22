"""
Database Management Tool for File Type Identification System.
Manage, import, export, and update magic number databases.
"""

import argparse
import sys
from pathlib import Path

from src.filemagic import FileTypeDatabase, FileTypeDetector
from src.filemagic.online_database import OnlineDatabaseFetcher, create_example_database_file


def export_default_database(output_file: str):
    """Export the default database to a JSON file."""
    print(f"\n📤 Exporting default database to: {output_file}")
    
    fetcher = OnlineDatabaseFetcher()
    
    if fetcher.export_default_database(output_file):
        print(f"✅ Successfully exported {len(FileTypeDatabase())} signatures")
    else:
        print("❌ Export failed")


def import_custom_database(input_file: str, test: bool = True):
    """Import a custom database from JSON file."""
    print(f"\n📥 Importing custom database from: {input_file}")
    
    fetcher = OnlineDatabaseFetcher()
    db = fetcher.load_from_file(input_file)
    
    if db:
        print(f"✅ Successfully loaded {len(db)} signatures")
        print(f"   Supported extensions: {len(db.get_supported_extensions())}")
        
        if test:
            print("\n🧪 Testing database...")
            detector = FileTypeDetector(database=db)
            print(f"   Detector ready with {len(detector.database)} signatures")
            print("   Database is valid and ready to use!")
    else:
        print("❌ Import failed")


def merge_databases(file1: str, file2: str, output_file: str):
    """Merge two database files."""
    print(f"\n🔀 Merging databases:")
    print(f"   File 1: {file1}")
    print(f"   File 2: {file2}")
    print(f"   Output: {output_file}")
    
    fetcher = OnlineDatabaseFetcher()
    
    db1 = fetcher.load_from_file(file1) if Path(file1).exists() else FileTypeDatabase()
    db2 = fetcher.load_from_file(file2)
    
    if not db2:
        print("❌ Failed to load second database")
        return
    
    merged = fetcher.merge_databases(db1, db2)
    
    if fetcher.save_to_file(merged, output_file):
        print(f"✅ Merged {len(merged)} signatures")
        print(f"   From file1: {len(db1)} signatures")
        print(f"   From file2: {len(db2)} signatures")
        print(f"   Total unique: {len(merged)} signatures")
    else:
        print("❌ Merge failed")


def list_signatures(database_file: str = None):
    """List all signatures in a database."""
    print("\n📋 SIGNATURE DATABASE LISTING")
    print("=" * 70)
    
    fetcher = OnlineDatabaseFetcher()
    
    if database_file:
        print(f"Loading from: {database_file}")
        db = fetcher.load_from_file(database_file)
    else:
        print("Using: Default built-in database")
        db = FileTypeDatabase()
    
    if not db:
        print("❌ Failed to load database")
        return
    
    print(f"\nTotal Signatures: {len(db)}")
    print(f"File Extensions: {len(db.get_supported_extensions())}")
    print("\n" + "=" * 70)
    
    # Group by extension
    by_extension = {}
    for sig in db.get_all_signatures():
        ext = sig.extension
        if ext not in by_extension:
            by_extension[ext] = []
        by_extension[ext].append(sig)
    
    for ext in sorted(by_extension.keys()):
        signatures = by_extension[ext]
        print(f"\n.{ext.upper()}")
        print("-" * 70)
        
        for sig in signatures:
            hex_sig = sig.signature.hex().upper()
            # Format hex in groups of 2
            hex_formatted = ' '.join(hex_sig[i:i+2] for i in range(0, len(hex_sig), 2))
            
            print(f"  Signature: {hex_formatted}")
            print(f"  Offset: {sig.offset}")
            print(f"  Description: {sig.description}")
            if sig.mime_type:
                print(f"  MIME Type: {sig.mime_type}")
            print()


def create_example_file(output_file: str = "custom_signatures.json"):
    """Create an example custom signature file."""
    print(f"\n📝 Creating example custom database file: {output_file}")
    create_example_database_file(output_file)
    print("\n💡 You can edit this file to add your own signatures!")
    print("   Format: JSON with signature, extension, description, offset, mime_type")


def show_online_sources():
    """Show available online sources."""
    print("\n🌐 AVAILABLE ONLINE SOURCES")
    print("=" * 70)
    
    fetcher = OnlineDatabaseFetcher()
    
    print("\nNote: Direct fetching from websites requires HTML parsing.")
    print("For now, you can manually download and convert to JSON format.\n")
    
    for source_id, source_name in fetcher.get_available_sources():
        source_info = fetcher.SOURCES[source_id]
        print(f"📍 {source_name}")
        print(f"   ID: {source_id}")
        print(f"   URL: {source_info['url']}")
        print(f"   Format: {source_info['format']}")
        print()
    
    print("=" * 70)
    print("\n💡 Recommended Workflow:")
    print("   1. Export default database: python manage_database.py export my_db.json")
    print("   2. Edit JSON file to add custom signatures")
    print("   3. Import updated database: python manage_database.py import my_db.json")
    print("   4. Test with detector: python main.py -f <file>")


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Magic Number Database Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_database.py export my_signatures.json
  python manage_database.py import custom_signatures.json
  python manage_database.py merge default.json custom.json merged.json
  python manage_database.py list
  python manage_database.py list custom_signatures.json
  python manage_database.py example
  python manage_database.py sources
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export default database to JSON')
    export_parser.add_argument('output', help='Output JSON file path')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import custom database from JSON')
    import_parser.add_argument('input', help='Input JSON file path')
    import_parser.add_argument('--no-test', action='store_true', help='Skip validation test')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge two database files')
    merge_parser.add_argument('file1', help='First database file (or "default" for built-in)')
    merge_parser.add_argument('file2', help='Second database file')
    merge_parser.add_argument('output', help='Output merged database file')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all signatures in database')
    list_parser.add_argument('file', nargs='?', help='Database file (optional, uses default if omitted)')
    
    # Example command
    example_parser = subparsers.add_parser('example', help='Create example custom database file')
    example_parser.add_argument('output', nargs='?', default='custom_signatures.json',
                               help='Output file (default: custom_signatures.json)')
    
    # Sources command
    subparsers.add_parser('sources', help='Show available online sources')
    
    args = parser.parse_args()
    
    # Display header
    print("\n" + "=" * 70)
    print("MAGIC NUMBER DATABASE MANAGEMENT TOOL")
    print("=" * 70)
    
    # Execute command
    if args.command == 'export':
        export_default_database(args.output)
    
    elif args.command == 'import':
        import_custom_database(args.input, test=not args.no_test)
    
    elif args.command == 'merge':
        merge_databases(args.file1, args.file2, args.output)
    
    elif args.command == 'list':
        list_signatures(args.file)
    
    elif args.command == 'example':
        create_example_file(args.output)
    
    elif args.command == 'sources':
        show_online_sources()
    
    else:
        parser.print_help()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
