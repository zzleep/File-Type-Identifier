"""
MagicNumber Class - Represents a file signature/magic number.
"""

from typing import Optional


class MagicNumber:
    """
    Represents a file signature (magic number) with its associated metadata.
    
    Attributes:
        signature (bytes): The byte sequence that identifies the file type
        offset (int): Position in the file where the signature appears
        extension (str): File extension associated with this signature
        description (str): Human-readable description of the file type
        mime_type (str): MIME type of the file
    """
    
    def __init__(
        self,
        signature: bytes,
        extension: str,
        description: str,
        offset: int = 0,
        mime_type: Optional[str] = None
    ):
        """
        Initialize a MagicNumber instance.
        
        Args:
            signature: Byte sequence identifying the file type
            extension: File extension (e.g., 'pdf', 'jpg')
            description: Human-readable description
            offset: Byte offset where signature appears (default: 0)
            mime_type: MIME type string (optional)
        """
        self.signature = signature
        self.offset = offset
        self.extension = extension.lower().lstrip('.')
        self.description = description
        self.mime_type = mime_type or f"application/{self.extension}"
    
    def matches(self, file_bytes: bytes) -> bool:
        """
        Check if the given bytes match this magic number.
        
        Args:
            file_bytes: Bytes read from a file
            
        Returns:
            True if the signature matches, False otherwise
        """
        if len(file_bytes) < self.offset + len(self.signature):
            return False
        
        return file_bytes[self.offset:self.offset + len(self.signature)] == self.signature
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return (f"MagicNumber(extension='{self.extension}', "
                f"signature={self.signature.hex()}, "
                f"offset={self.offset})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.extension.upper()} - {self.description}"
