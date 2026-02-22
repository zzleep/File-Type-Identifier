"""
File Type Identification System using Magic Numbers
A professional OOP-based solution for detecting file types and mismatches.
"""

__version__ = "1.0.0"
__author__ = "zzleep"

from .magic_number import MagicNumber
from .database import FileTypeDatabase
from .detector import FileTypeDetector
from .online_database import OnlineDatabaseFetcher

__all__ = ['MagicNumber', 'FileTypeDatabase', 'FileTypeDetector', 'OnlineDatabaseFetcher']
