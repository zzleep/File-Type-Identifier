"""
FileTypeDatabase Class - Manages a collection of known file signatures.
"""

from typing import List, Dict, Optional
from .magic_number import MagicNumber


class FileTypeDatabase:
    """
    Manages a database of known file signatures (magic numbers).
    
    Provides methods to add, retrieve, and search for file signatures.
    """
    
    def __init__(self):
        """Initialize an empty database."""
        self._signatures: List[MagicNumber] = []
        self._extension_map: Dict[str, List[MagicNumber]] = {}
        self._load_default_signatures()
    
    def _load_default_signatures(self):
        """Load a comprehensive set of common file signatures."""
        
        # Document formats
        self.add_signature(b'%PDF', 'pdf', 'Portable Document Format', mime_type='application/pdf')
        self.add_signature(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', 'doc', 'Microsoft Word Document (Old)', 
                          mime_type='application/msword')
        self.add_signature(b'PK\x03\x04', 'docx', 'Microsoft Word Document (Modern)', 
                          mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        self.add_signature(b'PK\x03\x04', 'xlsx', 'Microsoft Excel Spreadsheet', 
                          mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.add_signature(b'PK\x03\x04', 'pptx', 'Microsoft PowerPoint Presentation', 
                          mime_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        
        # Images
        self.add_signature(b'\xFF\xD8\xFF', 'jpg', 'JPEG Image', mime_type='image/jpeg')
        self.add_signature(b'\xFF\xD8\xFF', 'jpeg', 'JPEG Image', mime_type='image/jpeg')
        self.add_signature(b'\x89PNG\r\n\x1a\n', 'png', 'PNG Image', mime_type='image/png')
        self.add_signature(b'GIF87a', 'gif', 'GIF Image (87a)', mime_type='image/gif')
        self.add_signature(b'GIF89a', 'gif', 'GIF Image (89a)', mime_type='image/gif')
        self.add_signature(b'BM', 'bmp', 'Bitmap Image', mime_type='image/bmp')
        self.add_signature(b'II\x2A\x00', 'tiff', 'TIFF Image (Little Endian)', mime_type='image/tiff')
        self.add_signature(b'MM\x00\x2A', 'tiff', 'TIFF Image (Big Endian)', mime_type='image/tiff')
        self.add_signature(b'RIFF', 'webp', 'WebP Image', mime_type='image/webp')
        
        # Archives
        self.add_signature(b'PK\x03\x04', 'zip', 'ZIP Archive', mime_type='application/zip')
        self.add_signature(b'PK\x05\x06', 'zip', 'ZIP Archive (Empty)', mime_type='application/zip')
        self.add_signature(b'PK\x07\x08', 'zip', 'ZIP Archive (Spanned)', mime_type='application/zip')
        self.add_signature(b'Rar!\x1A\x07', 'rar', 'RAR Archive (v1.5+)', mime_type='application/x-rar-compressed')
        self.add_signature(b'Rar!\x1A\x07\x00', 'rar', 'RAR Archive (v5.0+)', mime_type='application/x-rar-compressed')
        self.add_signature(b'\x1F\x8B', 'gz', 'GZIP Archive', mime_type='application/gzip')
        self.add_signature(b'7z\xBC\xAF\x27\x1C', '7z', '7-Zip Archive', mime_type='application/x-7z-compressed')
        self.add_signature(b'BZh', 'bz2', 'BZIP2 Archive', mime_type='application/x-bzip2')
        
        # Executables
        self.add_signature(b'MZ', 'exe', 'Windows Executable', mime_type='application/x-msdownload')
        self.add_signature(b'\x7FELF', 'elf', 'Linux Executable', mime_type='application/x-executable')
        self.add_signature(b'\xCA\xFE\xBA\xBE', 'class', 'Java Class File', mime_type='application/java-vm')
        self.add_signature(b'\xFE\xED\xFA\xCE', 'macho', 'macOS Executable (32-bit)', 
                          mime_type='application/x-mach-binary')
        self.add_signature(b'\xFE\xED\xFA\xCF', 'macho', 'macOS Executable (64-bit)', 
                          mime_type='application/x-mach-binary')
        
        # Audio
        self.add_signature(b'ID3', 'mp3', 'MP3 Audio', mime_type='audio/mpeg')
        self.add_signature(b'\xFF\xFB', 'mp3', 'MP3 Audio (No ID3)', mime_type='audio/mpeg')
        self.add_signature(b'RIFF', 'wav', 'WAV Audio', mime_type='audio/wav')
        self.add_signature(b'fLaC', 'flac', 'FLAC Audio', mime_type='audio/flac')
        self.add_signature(b'OggS', 'ogg', 'OGG Audio', mime_type='audio/ogg')
        
        # Video
        self.add_signature(b'\x00\x00\x00\x18ftypmp42', 'mp4', 'MP4 Video', offset=4, mime_type='video/mp4')
        self.add_signature(b'\x00\x00\x00\x20ftypisom', 'mp4', 'MP4 Video (isom)', offset=4, 
                          mime_type='video/mp4')
        self.add_signature(b'RIFF', 'avi', 'AVI Video', mime_type='video/x-msvideo')
        self.add_signature(b'\x1A\x45\xDF\xA3', 'mkv', 'Matroska Video', mime_type='video/x-matroska')
        self.add_signature(b'FLV\x01', 'flv', 'Flash Video', mime_type='video/x-flv')
        
        # Database
        self.add_signature(b'SQLite format 3\x00', 'sqlite', 'SQLite Database', 
                          mime_type='application/x-sqlite3')
        
        # Other
        self.add_signature(b'<!DOCTYPE html', 'html', 'HTML Document', mime_type='text/html')
        self.add_signature(b'<html', 'html', 'HTML Document', mime_type='text/html')
        self.add_signature(b'<?xml', 'xml', 'XML Document', mime_type='text/xml')
        self.add_signature(b'{', 'json', 'JSON Document', mime_type='application/json')
        self.add_signature(b'[', 'json', 'JSON Array', mime_type='application/json')
    
    def add_signature(
        self,
        signature: bytes,
        extension: str,
        description: str,
        offset: int = 0,
        mime_type: Optional[str] = None
    ):
        """
        Add a new signature to the database.
        
        Args:
            signature: Byte sequence identifying the file type
            extension: File extension
            description: Human-readable description
            offset: Byte offset where signature appears (default: 0)
            mime_type: MIME type string (optional)
        """
        magic = MagicNumber(signature, extension, description, offset, mime_type)
        self._signatures.append(magic)
        
        # Update extension map
        ext = extension.lower().lstrip('.')
        if ext not in self._extension_map:
            self._extension_map[ext] = []
        self._extension_map[ext].append(magic)
    
    def get_signatures_by_extension(self, extension: str) -> List[MagicNumber]:
        """
        Get all signatures associated with a file extension.
        
        Args:
            extension: File extension to search for
            
        Returns:
            List of MagicNumber objects
        """
        ext = extension.lower().lstrip('.')
        return self._extension_map.get(ext, [])
    
    def get_all_signatures(self) -> List[MagicNumber]:
        """
        Get all signatures in the database.
        
        Returns:
            List of all MagicNumber objects
        """
        return self._signatures.copy()
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get a list of all supported file extensions.
        
        Returns:
            Sorted list of file extensions
        """
        return sorted(self._extension_map.keys())
    
    def __len__(self) -> int:
        """Return the number of signatures in the database."""
        return len(self._signatures)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"FileTypeDatabase(signatures={len(self._signatures)})"
