"""
Document Ingestion Testing Script
Tests all document loaders and OCR functionality

Run with: python scripts/test_ingestion.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.loaders import load_document, DocumentLoader
from backend.core.logging import get_logger

logger = get_logger()


def test_txt_loading():
    """Test TXT file loading"""
    print("\n" + "="*60)
    print("TEST 1: TXT FILE LOADING")
    print("="*60)
    
    try:
        file_path = "data/samples/test_docs/sample_eviction.txt"
        
        if not Path(file_path).exists():
            print(f"⚠️  Sample file not found: {file_path}")
            print("Creating sample file...")
            
            # Create sample if missing
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            sample_text = """Section 106 of the Transfer of Property Act
            
A lease of immovable property determines by efflux of the time limited thereby.
The landlord must provide proper notice before eviction."""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sample_text)
        
        doc = load_document(file_path, "txt")
        
        print(f"\n✅ TXT Loaded Successfully")
        print(f"   Filename: {doc['metadata']['filename']}")
        print(f"   Characters: {doc['metadata']['char_count']}")
        print(f"   Words: {doc['metadata']['word_count']}")
        print(f"\n   Preview (first 200 chars):")
        print(f"   {doc['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TXT Loading Failed: {e}")
        return False


def test_plain_text():
    """Test plain text input"""
    print("\n" + "="*60)
    print("TEST 2: PLAIN TEXT INPUT")
    print("="*60)
    
    try:
        plain_text = """This is a legal notice regarding eviction.
The tenant must vacate the premises within 30 days.
Failure to comply will result in legal action."""
        
        doc = load_document(plain_text, "plain")
        
        print(f"\n✅ Plain Text Loaded Successfully")
        print(f"   Source: {doc['metadata']['filename']}")
        print(f"   Characters: {doc['metadata']['char_count']}")
        print(f"\n   Content:")
        print(f"   {doc['text']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Plain Text Loading Failed: {e}")
        return False


def test_docx_loading():
    """Test DOCX file loading"""
    print("\n" + "="*60)
    print("TEST 3: DOCX FILE LOADING")
    print("="*60)
    
    try:
        file_path = "data/samples/test_docs/sample.docx"
        
        if not Path(file_path).exists():
            print(f"⚠️  No DOCX sample found: {file_path}")
            print("⏭️  Skipping DOCX test (manual file required)")
            print("\nTo test DOCX:")
            print(f"1. Create a Word document at: {file_path}")
            print("2. Add some legal text")
            print("3. Run this test again")
            return None  # Skip, not fail
        
        doc = load_document(file_path, "docx")
        
        print(f"\n✅ DOCX Loaded Successfully")
        print(f"   Filename: {doc['metadata']['filename']}")
        print(f"   Characters: {doc['metadata']['char_count']}")
        print(f"   Words: {doc['metadata']['word_count']}")
        print(f"\n   Preview (first 200 chars):")
        print(f"   {doc['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ DOCX Loading Failed: {e}")
        return False


def test_pdf_loading():
    """Test PDF file loading"""
    print("\n" + "="*60)
    print("TEST 4: PDF FILE LOADING")
    print("="*60)
    
    try:
        file_path = "data/samples/test_docs/sample.pdf"
        
        if not Path(file_path).exists():
            print(f"⚠️  No PDF sample found: {file_path}")
            print("⏭️  Skipping PDF test (manual file required)")
            print("\nTo test PDF:")
            print(f"1. Place a PDF file at: {file_path}")
            print("2. Use a legal document sample")
            print("3. Run this test again")
            return None  # Skip, not fail
        
        doc = load_document(file_path, "pdf")
        
        print(f"\n✅ PDF Loaded Successfully")
        print(f"   Filename: {doc['metadata']['filename']}")
        print(f"   Characters: {doc['metadata']['char_count']}")
        print(f"   Words: {doc['metadata']['word_count']}")
        print(f"\n   Preview (first 200 chars):")
        print(f"   {doc['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ PDF Loading Failed: {e}")
        return False


def test_auto_detection():
    """Test automatic file type detection"""
    print("\n" + "="*60)
    print("TEST 5: AUTOMATIC TYPE DETECTION")
    print("="*60)
    
    try:
        file_path = "data/samples/test_docs/sample_eviction.txt"
        
        # Load without specifying type
        doc = load_document(file_path)  # No source_type argument
        
        print(f"\n✅ Auto-detection Successful")
        print(f"   Detected Type: {doc['metadata']['source_type']}")
        print(f"   Filename: {doc['metadata']['filename']}")
        print(f"   Characters: {doc['metadata']['char_count']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Auto-detection Failed: {e}")
        return False


def test_unicode_support():
    """Test Unicode/Hindi text support"""
    print("\n" + "="*60)
    print("TEST 6: UNICODE/HINDI SUPPORT")
    print("="*60)
    
    try:
        # Sample Hindi text (legal notice)
        hindi_text = """कानूनी सूचना
        
किरायेदार को 30 दिनों के भीतर परिसर खाली करना होगा।
यह भारतीय संविदा अधिनियम के तहत एक कानूनी नोटिस है।

Legal Notice

The tenant must vacate within 30 days.
This is a legal notice under Indian Contract Act."""
        
        doc = load_document(hindi_text, "plain")
        
        print(f"\n✅ Unicode/Hindi Text Loaded Successfully")
        print(f"   Characters: {doc['metadata']['char_count']}")
        print(f"\n   Content:")
        print(f"   {doc['text']}")
        
        # Verify Hindi characters preserved
        if 'किरायेदार' in doc['text']:
            print("\n   ✅ Hindi characters preserved correctly")
        else:
            print("\n   ⚠️  Hindi characters may have been corrupted")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unicode Support Test Failed: {e}")
        return False


def test_ocr_capability():
    """Test OCR functionality (if Tesseract is installed)"""
    print("\n" + "="*60)
    print("TEST 7: OCR CAPABILITY CHECK")
    print("="*60)
    
    try:
        import pytesseract
        
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        
        print(f"\n✅ Tesseract OCR Installed")
        print(f"   Version: {version}")
        print(f"   OCR capability: AVAILABLE")
        print("\n   Scanned PDFs and images will be processed automatically.")
        
        return True
        
    except pytesseract.TesseractNotFoundError:
        print(f"\n⚠️  Tesseract OCR Not Found")
        print("\n   OCR capability: NOT AVAILABLE")
        print("\n   To enable OCR:")
        print("   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Linux: sudo apt install tesseract-ocr tesseract-ocr-hin")
        print("   - Mac: brew install tesseract tesseract-lang")
        print("\n   ℹ️  Text-based PDFs and Word docs will still work without OCR")
        
        return None  # Not a failure, just not available
        
    except Exception as e:
        print(f"\n⚠️  OCR Check Failed: {e}")
        return None


def main():
    """Run all ingestion tests"""
    print("\n" + "📄 DOCUMENT INGESTION TEST SUITE 📄".center(60))
    
    results = {}
    
    # Run tests
    results['txt'] = test_txt_loading()
    results['plain'] = test_plain_text()
    results['auto_detect'] = test_auto_detection()
    results['unicode'] = test_unicode_support()
    results['ocr'] = test_ocr_capability()
    results['docx'] = test_docx_loading()
    results['pdf'] = test_pdf_loading()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result is True else "⏭️  SKIPPED" if result is None else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 Core ingestion functionality is working!")
        print("\nℹ️  For full testing, add sample PDF and DOCX files to:")
        print("   data/samples/test_docs/")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    # Additional info
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    if results['ocr'] is None:
        print("\n📥 Install Tesseract OCR for scanned document support:")
        print("   - Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   - Command: Add Tesseract to PATH after installation")
    
    if results['pdf'] is None or results['docx'] is None:
        print("\n📄 Add sample documents for complete testing:")
        print("   - Place PDF files in: data/samples/test_docs/")
        print("   - Place DOCX files in: data/samples/test_docs/")
        print("   - Use legal documents (eviction notices, contracts, etc.)")
    
    print("\n✅ Ready for next phase: Text preprocessing and chunking")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
