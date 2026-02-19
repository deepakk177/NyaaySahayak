"""
Helper Utilities
Common utility functions used across the application
"""

import hashlib
from pathlib import Path
from typing import Union
from datetime import datetime, timedelta


def generate_file_hash(file_path: Union[str, Path]) -> str:
    """
    Generate SHA-256 hash of a file
    Useful for duplicate detection
    """
    sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    
    return sha256.hexdigest()


def generate_session_id() -> str:
    """Generate unique session ID"""
    timestamp = datetime.now().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()


def is_session_expired(created_at: datetime, expiry_hours: int = 24) -> bool:
    """Check if a session has expired"""
    expiry_time = created_at + timedelta(hours=expiry_hours)
    return datetime.now() > expiry_time


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
