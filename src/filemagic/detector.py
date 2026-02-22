"""
FileTypeDetector Class - Performs file type identification and mismatch detection.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

from .magic_number import MagicNumber
from .database import FileTypeDatabase


@dataclass
class DetectionResult:
    """
    Result of a file type detection operation.
    
    Attributes:
        file_path: Path to the analyzed file
        detected_type: The file type detected from magic numbers
        claimed_extension: The file extension from the filename
        is_mismatch: Whether there's a mismatch between detected and claimed types
        confidence: Confidence level of the detection
        mime_type: Detected MIME type
        description: Description of the detected file type
        file_size: Size of the file in bytes
    """
    file_path: str
    detected_type: Optional[str]
    claimed_extension: Optional[str]
    is_mismatch: bool
    confidence: str
    mime_type: Optional[str] = None
    description: Optional[str] = None
    file_size: int = 0
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "⚠️ MISMATCH" if self.is_mismatch else "✓ Match"
        detected = self.detected_type or "UNKNOWN"
        claimed = self.claimed_extension or "NONE"
        
        result = f"\n{'='*70}\n"
        result += f"File: {self.file_path}\n"
        result += f"Status: {status}\n"
        result += f"Claimed Extension: .{claimed}\n"
        result += f"Detected Type: .{detected}\n"
        result += f"Confidence: {self.confidence}\n"
        
        if self.description:
            result += f"Description: {self.description}\n"
        if self.mime_type:
            result += f"MIME Type: {self.mime_type}\n"
        
        result += f"File Size: {self.file_size:,} bytes\n"
        result += f"{'='*70}\n"
        
        return result


class FileTypeDetector:
    """
    Detects file types based on magic numbers and identifies mismatches.
    
    This class reads file headers and compares them against a database
    of known magic numbers to identify the true file type, then flags
    any mismatches with the file extension.
    """
    
    def __init__(self, database: Optional[FileTypeDatabase] = None, max_read_bytes: int = 8192):
        """
        Initialize the FileTypeDetector.
        
        Args:
            database: FileTypeDatabase instance (creates default if None)
            max_read_bytes: Maximum number of bytes to read from file header
        """
        self.database = database or FileTypeDatabase()
        self.max_read_bytes = max_read_bytes
    
    def detect_file(self, file_path: str) -> DetectionResult:
        """
        Detect the file type and check for mismatches.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            DetectionResult object with analysis results
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            PermissionError: If the file can't be read
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Get file information
        file_size = path.stat().st_size
        claimed_extension = path.suffix.lstrip('.').lower() if path.suffix else None
        
        # Read file header
        try:
            with open(file_path, 'rb') as f:
                header_bytes = f.read(self.max_read_bytes)
        except PermissionError as e:
            raise PermissionError(f"Permission denied: {file_path}") from e
        
        # Detect file type from magic numbers
        if detected_magic := self._match_signature(header_bytes):
            detected_type = detected_magic.extension
            mime_type = detected_magic.mime_type
            description = detected_magic.description
            confidence = "HIGH"
        else:
            detected_type = None
            mime_type = None
            description = "Unknown file type"
            confidence = "NONE"
        
        # Check for mismatch
        is_mismatch = self._is_mismatch(claimed_extension, detected_type)
        
        return DetectionResult(
            file_path=str(path),
            detected_type=detected_type,
            claimed_extension=claimed_extension,
            is_mismatch=is_mismatch,
            confidence=confidence,
            mime_type=mime_type,
            description=description,
            file_size=file_size
        )
    
    def detect_directory(self, directory_path: str, recursive: bool = False) -> List[DetectionResult]:
        """
        Detect file types for all files in a directory.
        
        Args:
            directory_path: Path to the directory
            recursive: Whether to search subdirectories
            
        Returns:
            List of DetectionResult objects
        """
        path = Path(directory_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        results = []
        
        files = path.rglob('*') if recursive else path.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                try:
                    result = self.detect_file(str(file_path))
                    results.append(result)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        return results
    
    def get_mismatches_only(self, results: List[DetectionResult]) -> List[DetectionResult]:
        """
        Filter results to only include mismatches.
        
        Args:
            results: List of DetectionResult objects
            
        Returns:
            List containing only mismatched files
        """
        return [r for r in results if r.is_mismatch]
    
    def _match_signature(self, file_bytes: bytes) -> Optional[MagicNumber]:
        """
        Match file bytes against known signatures.
        
        Args:
            file_bytes: Bytes read from file
            
        Returns:
            Matching MagicNumber or None
        """
        return next(
            (signature for signature in self.database.get_all_signatures() 
             if signature.matches(file_bytes)),
            None
        )
    
    def _is_mismatch(self, claimed_ext: Optional[str], detected_ext: Optional[str]) -> bool:
        """
        Determine if there's a mismatch between claimed and detected extensions.
        
        Args:
            claimed_ext: Extension from filename
            detected_ext: Extension detected from magic number
            
        Returns:
            True if there's a mismatch, False otherwise
        """
        if claimed_ext is None or detected_ext is None:
            return False
        
        # Normalize extensions
        claimed = claimed_ext.lower().lstrip('.')
        detected = detected_ext.lower().lstrip('.')
        
        # Direct match
        if claimed == detected:
            return False
        
        # Check for known aliases (jpg/jpeg, htm/html, etc.)
        aliases = {
            'jpg': 'jpeg',
            'jpeg': 'jpg',
            'htm': 'html',
            'html': 'htm',
            'tif': 'tiff',
            'tiff': 'tif'
        }
        
        if claimed in aliases and aliases[claimed] == detected:
            return False
        
        # Check if both extensions share the same signature
        # (e.g., docx, xlsx, pptx all use ZIP signature)
        claimed_sigs = self.database.get_signatures_by_extension(claimed)
        detected_sigs = self.database.get_signatures_by_extension(detected)
        
        for c_sig in claimed_sigs:
            for d_sig in detected_sigs:
                if c_sig.signature == d_sig.signature and c_sig.offset == d_sig.offset:
                    return False
        
        return True
    
    def generate_report(self, results: List[DetectionResult]) -> str:
        """
        Generate a comprehensive report from detection results.
        
        Args:
            results: List of DetectionResult objects
            
        Returns:
            Formatted report string
        """
        total = len(results)
        mismatches = len([r for r in results if r.is_mismatch])
        matches = total - mismatches
        
        report = "\n" + "="*70 + "\n"
        report += "FILE TYPE IDENTIFICATION REPORT\n"
        report += "="*70 + "\n\n"
        report += f"Total Files Analyzed: {total}\n"
        report += f"Matches: {matches} ✓\n"
        report += f"Mismatches: {mismatches} ⚠️\n"
        report += f"Success Rate: {(matches/total*100):.1f}%\n" if total > 0 else "N/A\n"
        report += "\n" + "="*70 + "\n"
        
        if mismatches > 0:
            report += "\nMISMATCHED FILES (POTENTIAL SECURITY RISK):\n"
            report += "="*70 + "\n"
            for result in results:
                if result.is_mismatch:
                    report += str(result)
        
        return report


# Example usage and testing
if __name__ == "__main__":
    print("File Type Detector - Magic Number Analysis")
    print("=" * 70)
    
    # Create detector instance
    detector = FileTypeDetector()
    
    # Display supported file types
    print(f"\nSupported file types: {len(detector.database)}")
    print(f"Extensions: {', '.join(detector.database.get_supported_extensions()[:20])}...")
    
    print("\n" + "=" * 70)
    print("Ready to analyze files!")
    print("=" * 70)
