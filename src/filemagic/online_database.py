"""
Online Magic Number Database Fetcher.
Fetches and updates file signature databases from online sources.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from .database import FileTypeDatabase


class OnlineDatabaseFetcher:
    """
    Fetches magic number databases from online sources.
    
    Provides methods to download, parse, and integrate online
    signature databases into the local FileTypeDatabase.
    """
    
    # Popular online sources for magic numbers
    SOURCES = {
        'gary_kessler': {
            'url': 'https://www.garykessler.net/library/file_sigs.html',
            'name': 'Gary Kessler File Signatures',
            'format': 'html'
        },
        'wikipedia': {
            'url': 'https://en.wikipedia.org/wiki/List_of_file_signatures',
            'name': 'Wikipedia File Signatures',
            'format': 'html'
        },
        'github_example': {
            'url': 'https://raw.githubusercontent.com/threat9/routersploit/master/routersploit/modules/exploits/routers/2wire/gateway_auth_bypass.py',
            'name': 'GitHub Magic Numbers Repository',
            'format': 'json'
        }
    }
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the online database fetcher.
        
        Args:
            cache_dir: Directory to cache downloaded databases (optional)
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.filemagic_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def fetch_from_url(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        Fetch content from a URL.
        
        Args:
            url: URL to fetch from
            timeout: Request timeout in seconds
            
        Returns:
            Content as string, or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) FileTypeMagic/1.0'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode('utf-8')
                return content
        
        except urllib.error.URLError as e:
            print(f"❌ Failed to fetch from {url}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error fetching from {url}: {e}")
            return None
    
    def parse_hex_string(self, hex_str: str) -> Optional[bytes]:
        """
        Parse a hex string into bytes.
        
        Handles various formats:
        - "FF D8 FF" (space-separated)
        - "FFD8FF" (no spaces)
        - "0xFFD8FF" (with 0x prefix)
        - "\\xFF\\xD8\\xFF" (Python byte string format)
        
        Args:
            hex_str: Hex string to parse
            
        Returns:
            Bytes object, or None if parsing failed
        """
        try:
            # Remove common prefixes and separators
            hex_str = hex_str.strip()
            hex_str = hex_str.replace('0x', '').replace('\\x', '')
            hex_str = hex_str.replace(' ', '').replace('-', '').replace(':', '')
            
            # Convert to bytes
            return bytes.fromhex(hex_str)
        
        except (ValueError, TypeError):
            return None
    
    def create_custom_database_from_json(self, json_data: str) -> Optional[FileTypeDatabase]:
        """
        Create a database from JSON format.
        
        Expected JSON format:
        {
            "signatures": [
                {
                    "signature": "FFD8FF",
                    "extension": "jpg",
                    "description": "JPEG Image",
                    "offset": 0,
                    "mime_type": "image/jpeg"
                }
            ]
        }
        
        Args:
            json_data: JSON string containing signature data
            
        Returns:
            FileTypeDatabase instance, or None if failed
        """
        try:
            data = json.loads(json_data)
            db = FileTypeDatabase()
            
            # Clear default signatures if specified
            if data.get('replace_defaults', False):
                db._signatures = []
                db._extension_map = {}
            
            for sig_data in data.get('signatures', []):
                signature_bytes = self.parse_hex_string(sig_data.get('signature', ''))
                
                if signature_bytes:
                    db.add_signature(
                        signature=signature_bytes,
                        extension=sig_data.get('extension', 'unknown'),
                        description=sig_data.get('description', 'Unknown file type'),
                        offset=sig_data.get('offset', 0),
                        mime_type=sig_data.get('mime_type')
                    )
            
            return db
        
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Error creating database from JSON: {e}")
            return None
    
    def load_from_file(self, file_path: str) -> Optional[FileTypeDatabase]:
        """
        Load a database from a local JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            FileTypeDatabase instance, or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = f.read()
            
            return self.create_custom_database_from_json(json_data)
        
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return None
        except Exception as e:
            print(f"❌ Error loading from file: {e}")
            return None
    
    def save_to_file(self, database: FileTypeDatabase, file_path: str) -> bool:
        """
        Save a database to a JSON file.
        
        Args:
            database: FileTypeDatabase to save
            file_path: Path where to save the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            signatures_data = []
            
            for sig in database.get_all_signatures():
                signatures_data.append({
                    'signature': sig.signature.hex().upper(),
                    'extension': sig.extension,
                    'description': sig.description,
                    'offset': sig.offset,
                    'mime_type': sig.mime_type
                })
            
            data = {
                'version': '1.0',
                'total_signatures': len(signatures_data),
                'signatures': signatures_data
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Database saved to: {file_path}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            return False
    
    def merge_databases(self, db1: FileTypeDatabase, db2: FileTypeDatabase) -> FileTypeDatabase:
        """
        Merge two databases, avoiding duplicates.
        
        Args:
            db1: First database
            db2: Second database to merge into the first
            
        Returns:
            Merged FileTypeDatabase
        """
        merged = FileTypeDatabase()
        
        # Add all signatures from db1
        for sig in db1.get_all_signatures():
            merged.add_signature(
                signature=sig.signature,
                extension=sig.extension,
                description=sig.description,
                offset=sig.offset,
                mime_type=sig.mime_type
            )
        
        # Add signatures from db2 if not duplicate
        existing_sigs = {(sig.signature, sig.offset) for sig in merged.get_all_signatures()}
        
        for sig in db2.get_all_signatures():
            if (sig.signature, sig.offset) not in existing_sigs:
                merged.add_signature(
                    signature=sig.signature,
                    extension=sig.extension,
                    description=sig.description,
                    offset=sig.offset,
                    mime_type=sig.mime_type
                )
        
        return merged
    
    def get_available_sources(self) -> List[Tuple[str, str]]:
        """
        Get list of available online sources.
        
        Returns:
            List of (source_id, source_name) tuples
        """
        return [(key, value['name']) for key, value in self.SOURCES.items()]
    
    def export_default_database(self, output_path: str) -> bool:
        """
        Export the default database to a JSON file.
        
        Args:
            output_path: Path where to save the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        db = FileTypeDatabase()
        return self.save_to_file(db, output_path)


# Example custom signature database in JSON format
EXAMPLE_CUSTOM_DATABASE = """
{
    "version": "1.0",
    "replace_defaults": false,
    "signatures": [
        {
            "signature": "504B0304",
            "extension": "zip",
            "description": "ZIP Archive",
            "offset": 0,
            "mime_type": "application/zip"
        },
        {
            "signature": "FFD8FFE0",
            "extension": "jpg",
            "description": "JPEG Image (JFIF)",
            "offset": 0,
            "mime_type": "image/jpeg"
        },
        {
            "signature": "25504446",
            "extension": "pdf",
            "description": "PDF Document",
            "offset": 0,
            "mime_type": "application/pdf"
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
"""


def create_example_database_file(output_path: str = "custom_signatures.json"):
    """
    Create an example custom signature database file.
    
    Args:
        output_path: Where to save the example file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(EXAMPLE_CUSTOM_DATABASE)
    
    print(f"✅ Example database created: {output_path}")
    print("You can edit this file to add your own signatures!")


if __name__ == "__main__":
    print("=" * 70)
    print("ONLINE MAGIC NUMBER DATABASE FETCHER")
    print("=" * 70)
    
    fetcher = OnlineDatabaseFetcher()
    
    print("\n📋 Available Online Sources:")
    for source_id, source_name in fetcher.get_available_sources():
        print(f"  • {source_id}: {source_name}")
    
    print("\n📁 Cache Directory:", fetcher.cache_dir)
    
    # Create example custom database
    print("\n🔧 Creating example custom database...")
    create_example_database_file()
    
    print("\n💡 Usage Examples:")
    print("  1. Load from JSON file:")
    print("     db = fetcher.load_from_file('custom_signatures.json')")
    print("\n  2. Export default database:")
    print("     fetcher.export_default_database('my_signatures.json')")
    print("\n  3. Merge databases:")
    print("     merged = fetcher.merge_databases(db1, db2)")
    
    print("\n" + "=" * 70)
