"""
Language Detection
Detects input language (English/Hindi)
"""

from langdetect import detect, LangDetectException
from backend.core.logging import get_logger

logger = get_logger()


def detect_language(text: str) -> str:
    """
    Detect language of input text
    
    Args:
        text: Input text
    
    Returns:
        Language code ('en' or 'hi')
    """
    try:
        # langdetect returns ISO 639-1 codes
        lang = detect(text)
        
        # Map to our supported languages
        if lang in ['en']:
            detected = 'en'
        elif lang in ['hi']:
            detected = 'hi'
        else:
            # Default to English for unsupported languages
            logger.warning(f"Unsupported language detected: {lang}, defaulting to English")
            detected = 'en'
        
        logger.info(f"Detected language: {detected}")
        return detected
        
    except LangDetectException as e:
        logger.error(f"Language detection failed: {e}, defaulting to English")
        return 'en'
