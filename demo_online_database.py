"""
Demonstration: Using Online Magic Number Databases
Shows how to work with custom databases from online sources.
"""

from src.filemagic import FileTypeDetector, FileTypeDatabase
from src.filemagic.online_database import OnlineDatabaseFetcher


def demo_export_default():
    """Demo: Export the default database to JSON."""
    print("\n" + "="*70)
    print("DEMO 1: Export Default Database")
    print("="*70)
    
    fetcher = OnlineDatabaseFetcher()
    output_file = "exported_default.json"
    
    if fetcher.export_default_database(output_file):
        print(f"\n✅ Exported default database to: {output_file}")
        print("   You can now:")
        print("   1. Edit this file to add signatures from online sources")
        print("   2. Share it with your team")
        print("   3. Keep it in version control")


def demo_load_custom():
    """Demo: Load a custom database from JSON."""
    print("\n" + "="*70)
    print("DEMO 2: Load Custom Database")
    print("="*70)
    
    fetcher = OnlineDatabaseFetcher()
    
    # Try to load custom database
    custom_file = "custom_signatures.json"
    
    if (db := fetcher.load_from_file(custom_file)):
        print(f"\n✅ Loaded custom database: {custom_file}")
        print(f"   Total signatures: {len(db)}")
        print(f"   Supported extensions: {len(db.get_supported_extensions())}")
        
        # Use it with detector
        detector = FileTypeDetector(database=db)
        print("\n✅ Detector ready with custom database!")
        print("   Can now detect files using your custom signatures")
    else:
        print(f"\n❌ Could not load {custom_file}")
        print("   Run: python manage_database.py example")


def demo_merge_databases():
    """Demo: Merge default and custom databases."""
    print("\n" + "="*70)
    print("DEMO 3: Merge Databases")
    print("="*70)
    
    fetcher = OnlineDatabaseFetcher()
    
    # Load default
    default_db = FileTypeDatabase()
    print(f"\n📦 Default database: {len(default_db)} signatures")
    
    # Load custom if exists
    try:
        if (custom_db := fetcher.load_from_file("custom_signatures.json")):
            print(f"📦 Custom database: {len(custom_db)} signatures")
            
            # Merge them
            merged_db = fetcher.merge_databases(default_db, custom_db)
            print(f"📦 Merged database: {len(merged_db)} signatures")
            
            # Save merged
            output = "merged_database.json"
            if fetcher.save_to_file(merged_db, output):
                print(f"\n✅ Saved merged database to: {output}")
                print("   This combines built-in + custom signatures")
        else:
            print("⚠️  No custom database found to merge")
    except Exception:
        print("⚠️  No custom database found to merge")


def demo_parse_hex():
    """Demo: Parse various hex string formats."""
    print("\n" + "="*70)
    print("DEMO 4: Parse Hex Strings (from online sources)")
    print("="*70)
    
    fetcher = OnlineDatabaseFetcher()
    
    # Different formats you might find online
    hex_formats = [
        ("FFD8FF", "No spaces (common)"),
        ("FF D8 FF", "Space-separated"),
        ("0xFFD8FF", "With 0x prefix"),
        ("FF-D8-FF", "Dash-separated"),
        ("FF:D8:FF", "Colon-separated"),
    ]
    
    print("\n📝 Examples of hex formats from online sources:")
    print("   (All of these work with our parser)\n")
    
    for hex_str, description in hex_formats:
        if (result := fetcher.parse_hex_string(hex_str)):
            print(f"✅ {hex_str:<20} ({description})")
            print(f"   → {result.hex().upper()}")
        else:
            print(f"❌ {hex_str:<20} Failed to parse")


def demo_online_sources():
    """Demo: Show available online sources."""
    print("\n" + "="*70)
    print("DEMO 5: Available Online Sources")
    print("="*70)
    
    fetcher = OnlineDatabaseFetcher()
    
    print("\n🌐 Trusted sources for magic numbers:\n")
    
    sources = [
        ("Gary Kessler's Database", 
         "https://www.garykessler.net/library/file_sigs.html",
         "500+ signatures, industry standard"),
        
        ("Wikipedia",
         "https://en.wikipedia.org/wiki/List_of_file_signatures",
         "200+ common signatures, well-documented"),
        
        ("FileSignatures.net",
         "https://filesignatures.net/",
         "1000+ signatures, searchable"),
    ]
    
    for name, url, description in sources:
        print(f"📍 {name}")
        print(f"   URL: {url}")
        print(f"   Info: {description}")
        print()
    
    print("💡 How to use:")
    print("   1. Visit any of these sources")
    print("   2. Find the signature you need (e.g., 'FF D8 FF' for JPEG)")
    print("   3. Add it to your JSON database")
    print("   4. Import: python manage_database.py import your_db.json")


def demo_practical_example():
    """Demo: Practical example of adding a signature from online."""
    print("\n" + "="*70)
    print("DEMO 6: Practical Example - Adding MIDI Signature")
    print("="*70)
    
    print("\n📖 Scenario: You need to detect MIDI files")
    print("   Step 1: Visit Gary Kessler's database")
    print("   Step 2: Find MIDI signature: '4D 54 68 64'")
    print("   Step 3: Create/edit your database JSON:\n")
    
    example_json = '''
    {
      "version": "1.0",
      "replace_defaults": false,
      "signatures": [
        {
          "signature": "4D546864",
          "extension": "mid",
          "description": "MIDI Audio File",
          "offset": 0,
          "mime_type": "audio/midi"
        }
      ]
    }
    '''
    
    print(example_json)
    
    print("\n   Step 4: Import the database:")
    print("   python manage_database.py import my_db.json")
    
    print("\n   Step 5: Test detection:")
    print("   python main.py -f song.mid")
    
    print("\n✅ Now your system can detect MIDI files!")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("ONLINE DATABASE DEMONSTRATIONS")
    print("File Type Identification System")
    print("="*70)
    
    demos = [
        ("Export Default Database", demo_export_default),
        ("Load Custom Database", demo_load_custom),
        ("Merge Databases", demo_merge_databases),
        ("Parse Hex Strings", demo_parse_hex),
        ("Online Sources", demo_online_sources),
        ("Practical Example", demo_practical_example),
    ]
    
    print("\n📚 Available Demonstrations:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"   {i}. {name}")
    print("   0. Run All")
    
    try:
        choice = input("\nSelect demo (0-6): ").strip()
        
        if choice == '0':
            # Run all demos
            for name, demo_func in demos:
                demo_func()
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run selected demo
            name, demo_func = demos[int(choice) - 1]
            demo_func()
        else:
            print("Invalid choice. Running all demos...\n")
            for name, demo_func in demos:
                demo_func()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    print("\n" + "="*70)
    print("DEMONSTRATIONS COMPLETE")
    print("="*70)
    
    print("\n💡 Quick Commands:")
    print("   python manage_database.py export my.json     # Export database")
    print("   python manage_database.py import my.json     # Import database")
    print("   python manage_database.py sources            # Show sources")
    print("   python main.py -f <file>                     # Detect file type")
    
    print("\n📚 Documentation:")
    print("   See ONLINE_DATABASE_GUIDE.md for complete guide")
    print("   See ONLINE_DATABASE_SUMMARY.md for quick reference")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
