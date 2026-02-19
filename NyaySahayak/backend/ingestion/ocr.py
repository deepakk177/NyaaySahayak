"""
OCR Pipeline using Tesseract
Handles scanned PDFs and image-based documents with preprocessing
"""

import cv2
import pytesseract
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Union
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger()


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Improve OCR accuracy for scanned legal documents
    
    Preprocessing steps:
    1. Convert to grayscale
    2. Apply Otsu's thresholding
    3. Denoise (optional)
    
    Args:
        image: PIL Image object
    
    Returns:
        Preprocessed numpy array optimized for OCR
    """
    try:
        # Convert PIL Image to numpy array
        img = np.array(image.convert("RGB"))
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Apply Otsu's thresholding for better text contrast
        thresh = cv2.threshold(
            gray, 
            0, 
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        
        # Optional: Denoise (can improve accuracy for noisy scans)
        # denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        logger.debug("Image preprocessed for OCR")
        return thresh
        
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        # Return original as grayscale fallback
        return np.array(image.convert("L"))


def extract_text_from_image(image: Image.Image, lang: str = None) -> str:
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image: PIL Image object
        lang: Language code for OCR (default: eng+hin for English+Hindi)
    
    Returns:
        Extracted text
    """
    try:
        lang = lang or settings.tesseract_lang or "eng+hin"
        
        logger.info(f"Extracting text with OCR (lang={lang})")
        
        # Preprocess image for better OCR
        processed_img = preprocess_image(image)
        
        # Perform OCR
        text = pytesseract.image_to_string(
            processed_img,
            lang=lang,
            config='--psm 3'  # Fully automatic page segmentation
        )
        
        logger.info(f"OCR extracted {len(text)} characters")
        return text
        
    except pytesseract.TesseractNotFoundError:
        logger.error("Tesseract OCR not found! Please install Tesseract.")
        raise RuntimeError(
            "Tesseract OCR is not installed or not in PATH. "
            "Install from: https://github.com/tesseract-ocr/tesseract"
        )
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return ""


def extract_text_from_pdf_images(pdf_path: Union[str, Path], resolution: int = 300) -> str:
    """
    Extract text from scanned PDF using OCR
    
    Args:
        pdf_path: Path to PDF file
        resolution: DPI resolution for image conversion (higher = better quality)
    
    Returns:
        Extracted text from all pages
    """
    try:
        import pdfplumber
        
        logger.info(f"Processing scanned PDF with OCR: {pdf_path}")
        
        full_text = ""
        page_count = 0
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                logger.info(f"OCR processing page {page_num}/{total_pages}")
                
                try:
                    # Convert page to image at specified resolution
                    image = page.to_image(resolution=resolution).original
                    
                    # Extract text with OCR
                    page_text = extract_text_from_image(image)
                    
                    if page_text.strip():
                        full_text += f"\n--- Page {page_num} ---\n{page_text}\n"
                        page_count += 1
                    
                except Exception as e:
                    logger.warning(f"Failed to OCR page {page_num}: {e}")
                    continue
        
        logger.info(f"OCR completed for {page_count}/{total_pages} pages")
        return full_text
        
    except Exception as e:
        logger.error(f"PDF OCR processing failed: {e}")
        raise


def is_pdf_scanned(pdf_path: Union[str, Path], sample_pages: int = 3) -> bool:
    """
    Heuristic to detect if a PDF is scanned (image-based)
    
    Args:
        pdf_path: Path to PDF file
        sample_pages: Number of pages to sample for detection
    
    Returns:
        True if PDF appears to be scanned
    """
    try:
        import pdfplumber
        
        with pdfplumber.open(pdf_path) as pdf:
            total_chars = 0
            pages_checked = 0
            
            # Check first few pages
            for page in pdf.pages[:sample_pages]:
                text = page.extract_text()
                if text:
                    total_chars += len(text.strip())
                pages_checked += 1
            
            # Heuristic: If very little text per page, likely scanned
            avg_chars_per_page = total_chars / max(pages_checked, 1)
            
            is_scanned = avg_chars_per_page < 100
            
            logger.info(
                f"PDF scan detection: avg {avg_chars_per_page:.0f} chars/page "
                f"-> {'SCANNED' if is_scanned else 'TEXT-BASED'}"
            )
            
            return is_scanned
            
    except Exception as e:
        logger.warning(f"Scan detection failed: {e}, assuming scanned")
        return True  # Safer to assume scanned if detection fails


class OCRProcessor:
    """Enhanced OCR processor with configurable settings"""
    
    def __init__(self, lang: str = "eng+hin", resolution: int = 300):
        """
        Initialize OCR processor
        
        Args:
            lang: Tesseract language code
            resolution: Image resolution for PDF conversion
        """
        self.lang = lang
        self.resolution = resolution
        
        # Configure Tesseract path if specified
        if settings.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path
        
        logger.info(f"OCR initialized: lang={lang}, resolution={resolution}")
    
    def process_image(self, image_path: Union[str, Path]) -> str:
        """Process a single image file"""
        image = Image.open(image_path)
        return extract_text_from_image(image, lang=self.lang)
    
    def process_scanned_pdf(self, pdf_path: Union[str, Path]) -> str:
        """Process scanned PDF"""
        return extract_text_from_pdf_images(pdf_path, resolution=self.resolution)


# Global OCR processor instance
_ocr_processor = None


def get_ocr_processor() -> OCRProcessor:
    """Get or create global OCR processor"""
    global _ocr_processor
    if _ocr_processor is None:
        _ocr_processor = OCRProcessor()
    return _ocr_processor
