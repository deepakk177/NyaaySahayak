"""
Legal Text Preprocessing
Cleans and normalizes legal documents while preserving structure
"""

import re
from typing import Tuple, Dict
from langdetect import detect, LangDetectException
from backend.core.logging import get_logger

logger = get_logger()


def detect_language(text: str) -> str:
    """
    Detect language of the document.
    Returns ISO code: 'en' or 'hi'
    
    Args:
        text: Input text to analyze
    
    Returns:
        Language code ('en' or 'hi')
    """
    try:
        # Skip very short text
        if len(text.strip()) < 20:
            logger.warning("Text too short for reliable language detection")
            return "en"
        
        lang = detect(text)
        
        logger.info(f"Detected language: {lang}")
        
        # Map to supported languages
        if lang in ["en"]:
            return "en"
        elif lang in ["hi"]:
            return "hi"
        else:
            logger.warning(f"Unsupported language '{lang}', defaulting to English")
            return "en"  # fallback to English
            
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}, defaulting to English")
        return "en"
    except Exception as e:
        logger.error(f"Unexpected error in language detection: {e}")
        return "en"


def remove_headers_and_footers(text: str) -> str:
    """
    Remove common legal document noise:
    - Page numbers (e.g., "Page 1", "1 of 10")
    - Repeating headers/footers
    - Standalone numbers
    - Excessive punctuation lines
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines (will be normalized later)
        if not line_stripped:
            cleaned_lines.append("")
            continue
        
        # Remove page numbers
        if re.match(r"^page\s*\d+$", line_stripped, re.IGNORECASE):
            logger.debug(f"Removed page number: {line_stripped}")
            continue
        
        # Remove "Page X of Y" patterns
        if re.match(r"^(page\s+)?\d+\s+of\s+\d+$", line_stripped, re.IGNORECASE):
            logger.debug(f"Removed page indicator: {line_stripped}")
            continue
        
        # Remove standalone numbers (likely page numbers)
        if re.match(r"^\d+$", line_stripped):
            logger.debug(f"Removed standalone number: {line_stripped}")
            continue
        
        # Remove lines with only punctuation/special characters
        if re.match(r"^[\W_]+$", line_stripped):
            logger.debug(f"Removed punctuation-only line: {line_stripped}")
            continue
        
        # Remove common OCR artifacts
        if re.match(r"^-{3,}$", line_stripped):  # "---" separators
            logger.debug("Removed separator line")
            continue
        
        cleaned_lines.append(line)
    
    result = "\n".join(cleaned_lines)
    logger.info(f"Headers/footers removed: {len(lines)} → {len(cleaned_lines)} lines")
    
    return result


def normalize_whitespace(text: str) -> str:
    """
    Normalize spacing without destroying clause structure
    
    - Replace multiple spaces with single space
    - Normalize line breaks (max 2 consecutive)
    - Preserve paragraph breaks
    
    Args:
        text: Input text
    
    Returns:
        Normalized text
    """
    # Replace tabs with spaces
    text = text.replace("\t", " ")
    
    # Replace multiple spaces with one (but not across lines)
    lines = text.splitlines()
    normalized_lines = [re.sub(r"[ ]+", " ", line) for line in lines]
    text = "\n".join(normalized_lines)
    
    # Normalize multiple newlines (max 2 for paragraph separation)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Remove trailing/leading whitespace
    text = text.strip()
    
    logger.info("Whitespace normalized")
    return text


def preserve_legal_structure(text: str) -> str:
    """
    Preserve and enhance legal document structure:
    - Section markers
    - Clause numbering
    - Article references
    
    Args:
        text: Input text
    
    Returns:
        Structurally enhanced text
    """
    # Ensure space after section numbers (e.g., "1.Text" → "1. Text")
    text = re.sub(r"(\d+\.)\s*([A-Za-z])", r"\1 \2", text)
    
    # Add line break before "Section X" (case-insensitive)
    text = re.sub(r"(?<!\n)(Section\s+\d+)", r"\n\n\1", text, flags=re.IGNORECASE)
    
    # Add line break before "Clause X"
    text = re.sub(r"(?<!\n)(Clause\s+\d+)", r"\n\1", text, flags=re.IGNORECASE)
    
    # Add line break before "Article X"
    text = re.sub(r"(?<!\n)(Article\s+\d+)", r"\n\1", text, flags=re.IGNORECASE)
    
    # Normalize "Sec." to "Section" for consistency
    text = re.sub(r"\bSec\.\s*(\d+)", r"Section \1", text)
    
    # Normalize "Art." to "Article"
    text = re.sub(r"\bArt\.\s*(\d+)", r"Article \1", text)
    
    logger.info("Legal structure preserved and enhanced")
    return text


def remove_boilerplate(text: str, aggressive: bool = False) -> str:
    """
    Remove common legal boilerplate text
    
    Args:
        text: Input text
        aggressive: If True, remove more aggressively
    
    Returns:
        Text with boilerplate removed
    """
    boilerplate_patterns = [
        r"This document is for informational purposes only.*?\.",
        r"Confidential and Proprietary.*?\.",
        r"All rights reserved.*?\.",
    ]
    
    if aggressive:
        # Add more aggressive patterns
        boilerplate_patterns.extend([
            r"Copyright \d{4}.*?\.",
            r"Printed on.*?\.",
        ])
    
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
    
    logger.info(f"Boilerplate removed (aggressive={aggressive})")
    return text


def clean_ocr_artifacts(text: str) -> str:
    """
    Clean common OCR artifacts
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Fix common OCR mistakes for legal terms
    ocr_fixes = {
        r'\bl\s+(\w+)': r'I \1',  # "l" → "I" at word start
        r'(\w+)\s+l\b': r'\1 I',  # "l" → "I" at word end
        r'\b0\s+': r'O ',         # "0" → "O" in words
    }
    
    for pattern, replacement in ocr_fixes.items():
        text = re.sub(pattern, replacement, text)
    
    logger.debug("OCR artifacts cleaned")
    return text


def preprocess_document(
    raw_text: str,
    metadata: Dict,
    remove_boilerplate_text: bool = False,
    aggressive: bool = False
) -> Tuple[str, Dict]:
    """
    Full preprocessing pipeline for legal documents
    
    Pipeline:
    1. Detect language
    2. Remove headers/footers
    3. Clean OCR artifacts
    4. Remove boilerplate (optional)
    5. Normalize whitespace
    6. Preserve legal structure
    
    Args:
        raw_text: Raw text from document loader
        metadata: Existing metadata dict
        remove_boilerplate_text: Whether to remove boilerplate
        aggressive: Use aggressive cleaning
    
    Returns:
        Tuple of (cleaned_text, enriched_metadata)
    
    Example:
        >>> text, meta = preprocess_document(raw_text, {"filename": "law.pdf"})
        >>> print(meta["language"])  # 'en'
        >>> print(text[:100])  # Clean, structured text
    """
    logger.info("Starting document preprocessing")
    
    # Step 1: Detect language
    language = detect_language(raw_text)
    
    # Step 2: Remove headers and footers
    text = remove_headers_and_footers(raw_text)
    
    # Step 3: Clean OCR artifacts
    text = clean_ocr_artifacts(text)
    
    # Step 4: Remove boilerplate (optional)
    if remove_boilerplate_text:
        text = remove_boilerplate(text, aggressive=aggressive)
    
    # Step 5: Normalize whitespace
    text = normalize_whitespace(text)
    
    # Step 6: Preserve legal structure
    text = preserve_legal_structure(text)
    
    # Update metadata
    updated_metadata = metadata.copy()
    updated_metadata.update({
        "language": language,
        "text_length": len(text),
        "word_count": len(text.split()),
        "preprocessed": True,
        "boilerplate_removed": remove_boilerplate_text
    })
    
    logger.info(f"Preprocessing complete: {language}, {len(text)} chars")
    
    return text, updated_metadata


class TextPreprocessor:
    """
    Configurable text preprocessor for legal documents
    """
    
    def __init__(
        self,
        remove_boilerplate: bool = False,
        aggressive: bool = False
    ):
        """
        Initialize preprocessor
        
        Args:
            remove_boilerplate: Whether to remove boilerplate text
            aggressive: Use aggressive cleaning
        """
        self.remove_boilerplate = remove_boilerplate
        self.aggressive = aggressive
        
        logger.info(
            f"TextPreprocessor initialized: "
            f"boilerplate={remove_boilerplate}, aggressive={aggressive}"
        )
    
    def preprocess(self, raw_text: str, metadata: Dict) -> Tuple[str, Dict]:
        """Preprocess with instance settings"""
        return preprocess_document(
            raw_text,
            metadata,
            remove_boilerplate_text=self.remove_boilerplate,
            aggressive=self.aggressive
        )


# Global preprocessor instance
_preprocessor = None


def get_preprocessor() -> TextPreprocessor:
    """Get or create global preprocessor"""
    global _preprocessor
    if _preprocessor is None:
        _preprocessor = TextPreprocessor()
    return _preprocessor
