"""
Text Preprocessing Testing Script
Tests legal text cleaning and language detection

Run with: python scripts/test_preprocessing.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.preprocessing import (
    preprocess_document,
    detect_language,
    remove_headers_and_footers,
    normalize_whitespace,
    preserve_legal_structure
)


def test_basic_preprocessing():
    """Test basic preprocessing pipeline"""
    print("\n" + "="*60)
    print("TEST 1: BASIC PREPROCESSING")
    print("="*60)
    
    raw_text = """
Page 1

SECTION 1
The landlord shall provide thirty days notice.

Page 2

SECTION 2
No tenant shall be removed without due process.
"""
    
    metadata = {
        "filename": "eviction_notice.pdf",
        "source_type": "pdf"
    }
    
    clean_text, updated_metadata = preprocess_document(raw_text, metadata)
    
    print("\n📝 RAW TEXT:")
    print(raw_text)
    
    print("\n✨ CLEAN TEXT:")
    print(clean_text)
    
    print("\n📊 METADATA:")
    for key, value in updated_metadata.items():
        print(f"   {key}: {value}")
    
    # Verify page numbers removed
    assert "Page 1" not in clean_text
    assert "Page 2" not in clean_text
    
    # Verify sections preserved
    assert "SECTION 1" in clean_text
    assert "SECTION 2" in clean_text
    
    print("\n✅ Basic preprocessing PASSED")
    return True


def test_language_detection():
    """Test language detection for English and Hindi"""
    print("\n" + "="*60)
    print("TEST 2: LANGUAGE DETECTION")
    print("="*60)
    
    # English text
    english_text = "Section 106 of the Transfer of Property Act requires notice before eviction."
    lang_en = detect_language(english_text)
    
    # Hindi text
    hindi_text = """किरायेदार को 30 दिनों के भीतर परिसर खाली करना होगा।
यह भारतीय संविदा अधिनियम के तहत एक कानूनी नोटिस है।"""
    lang_hi = detect_language(hindi_text)
    
    # Mixed text (should detect primary language)
    mixed_text = """Legal Notice - कानूनी सूचना
    
This is a legal notice. The tenant must vacate within 30 days.
किरायेदार को 30 दिनों में जगह खाली करनी होगी।"""
    lang_mixed = detect_language(mixed_text)
    
    print(f"\n📝 English text detected as: {lang_en}")
    print(f"📝 Hindi text detected as: {lang_hi}")
    print(f"📝 Mixed text detected as: {lang_mixed}")
    
    assert lang_en == "en", f"Expected 'en', got '{lang_en}'"
    assert lang_hi == "hi", f"Expected 'hi', got '{lang_hi}'"
    
    print("\n✅ Language detection PASSED")
    return True


def test_header_footer_removal():
    """Test removal of headers and footers"""
    print("\n" + "="*60)
    print("TEST 3: HEADER/FOOTER REMOVAL")
    print("="*60)
    
    text_with_noise = """Page 1
    
Legal Document Title

This is the actual content.

Page 2 of 10

More content here.

123

Final section.

-------------------
"""
    
    cleaned = remove_headers_and_footers(text_with_noise)
    
    print("\n📝 ORIGINAL:")
    print(text_with_noise)
    
    print("\n✨ CLEANED:")
    print(cleaned)
    
    # Verify removals
    assert "Page 1" not in cleaned
    assert "Page 2 of 10" not in cleaned
    assert "123" not in cleaned  # Standalone number
    assert "---" not in cleaned  # Separator
    
    # Verify content preserved
    assert "Legal Document Title" in cleaned
    assert "This is the actual content" in cleaned
    assert "More content here" in cleaned
    
    print("\n✅ Header/footer removal PASSED")
    return True


def test_legal_structure_preservation():
    """Test preservation of legal structure"""
    print("\n" + "="*60)
    print("TEST 4: LEGAL STRUCTURE PRESERVATION")
    print("="*60)
    
    unstructured_text = """Section 1This is section one.Clause 1Details here.
Article 5More details.Sec. 10Additional information.Art. 3Final clause."""
    
    structured = preserve_legal_structure(unstructured_text)
    
    print("\n📝 UNSTRUCTURED:")
    print(unstructured_text)
    
    print("\n✨ STRUCTURED:")
    print(structured)
    
    # Verify structure added
    assert "\nSection 1" in structured
    assert "\nClause 1" in structured
    assert "\nArticle 5" in structured
    
    # Verify normalization
    assert "Section 10" in structured  # Sec. → Section
    assert "Article 3" in structured   # Art. → Article
    
    print("\n✅ Legal structure preservation PASSED")
    return True


def test_whitespace_normalization():
    """Test whitespace normalization"""
    print("\n" + "="*60)
    print("TEST 5: WHITESPACE NORMALIZATION")
    print("="*60)
    
    messy_text = """This    has   multiple    spaces.


And multiple


newlines.

	Tabs	here."""
    
    normalized = normalize_whitespace(messy_text)
    
    print("\n📝 MESSY:")
    print(repr(messy_text))
    
    print("\n✨ NORMALIZED:")
    print(repr(normalized))
    
    # Verify normalization
    assert "    " not in normalized  # No multiple spaces
    assert "\n\n\n" not in normalized  # Max 2 newlines
    assert "\t" not in normalized  # No tabs
    
    print("\n✅ Whitespace normalization PASSED")
    return True


def test_hindi_preservation():
    """Test that Hindi text is preserved correctly"""
    print("\n" + "="*60)
    print("TEST 6: HINDI TEXT PRESERVATION")
    print("="*60)
    
    hindi_text = """पृष्ठ 1

धारा 106
संपत्ति हस्तांतरण अधिनियम, 1882

पृष्ठ 2

मकान मालिक को बेदखली से पहले नोटिस देना होगा।
किरायेदार को 30 दिनों की सूचना दी जानी चाहिए।"""
    
    metadata = {"filename": "hindi_law.txt", "source_type": "txt"}
    
    clean_text, updated_metadata = preprocess_document(hindi_text, metadata)
    
    print("\n📝 ORIGINAL HINDI:")
    print(hindi_text)
    
    print("\n✨ PROCESSED HINDI:")
    print(clean_text)
    
    print(f"\n🌐 Detected Language: {updated_metadata['language']}")
    
    # Verify Hindi characters preserved
    assert "धारा" in clean_text
    assert "किरायेदार" in clean_text
    assert "मकान मालिक" in clean_text
    
    # Verify language detection
    assert updated_metadata["language"] == "hi"
    
    print("\n✅ Hindi preservation PASSED")
    return True


def test_full_pipeline():
    """Test complete preprocessing pipeline with real-world text"""
    print("\n" + "="*60)
    print("TEST 7: FULL PIPELINE (REAL-WORLD TEXT)")
    print("="*60)
    
    real_world_text = """Page 1 of 5
    
THE TRANSFER OF PROPERTY ACT, 1882

SECTION 106
Duration of certain leases in absence of written contract or local usage

Page 2 of 5

A lease of immovable property determines by efflux of the time limited thereby.

Sec. 107 Leases how made

A lease of immovable property from year to year, or for any term exceeding one year.

---

Page 3

Clause 1The lessor shall give notice to quit.
Clause 2The lessee may terminate with proper notice.

123

Art. 5 Final provisions apply.

Copyright 2024. All rights reserved.
"""
    
    metadata = {
        "filename": "property_act.pdf",
        "source_type": "pdf",
        "source": "legal_database"
    }
    
    # Process with boilerplate removal
    clean_text, updated_metadata = preprocess_document(
        real_world_text,
        metadata,
        remove_boilerplate_text=True
    )
    
    print("\n📝 RAW TEXT (excerpt):")
    print(real_world_text[:200] + "...")
    
    print("\n✨ CLEAN TEXT:")
    print(clean_text)
    
    print("\n📊 ENRICHED METADATA:")
    for key, value in updated_metadata.items():
        print(f"   {key}: {value}")
    
    # Verification
    assert "Page 1" not in clean_text
    assert "Page 2" not in clean_text
    assert "123" not in clean_text
    assert "---" not in clean_text
    
    # Content preserved
    assert "SECTION 106" in clean_text
    assert "Section 107" in clean_text  # Normalized from Sec.
    assert "Clause 1" in clean_text
    assert "Article 5" in clean_text  # Normalized from Art.
    
    # Metadata enriched
    assert updated_metadata["language"] == "en"
    assert updated_metadata["preprocessed"] is True
    assert updated_metadata["text_length"] > 0
    
    print("\n✅ Full pipeline PASSED")
    return True


def main():
    """Run all preprocessing tests"""
    print("\n" + "🧹 TEXT PREPROCESSING TEST SUITE 🧹".center(60))
    
    results = {}
    
    # Run tests
    try:
        results['basic'] = test_basic_preprocessing()
    except Exception as e:
        print(f"\n❌ Basic preprocessing FAILED: {e}")
        results['basic'] = False
    
    try:
        results['language'] = test_language_detection()
    except Exception as e:
        print(f"\n❌ Language detection FAILED: {e}")
        results['language'] = False
    
    try:
        results['headers'] = test_header_footer_removal()
    except Exception as e:
        print(f"\n❌ Header/footer removal FAILED: {e}")
        results['headers'] = False
    
    try:
        results['structure'] = test_legal_structure_preservation()
    except Exception as e:
        print(f"\n❌ Structure preservation FAILED: {e}")
        results['structure'] = False
    
    try:
        results['whitespace'] = test_whitespace_normalization()
    except Exception as e:
        print(f"\n❌ Whitespace normalization FAILED: {e}")
        results['whitespace'] = False
    
    try:
        results['hindi'] = test_hindi_preservation()
    except Exception as e:
        print(f"\n❌ Hindi preservation FAILED: {e}")
        results['hindi'] = False
    
    try:
        results['full'] = test_full_pipeline()
    except Exception as e:
        print(f"\n❌ Full pipeline FAILED: {e}")
        results['full'] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 All preprocessing tests passed!")
        print("\n✅ Text preprocessing is ready for production use")
        print("\nFeatures verified:")
        print("  ✓ Header/footer removal")
        print("  ✓ Language detection (English + Hindi)")
        print("  ✓ Legal structure preservation")
        print("  ✓ Whitespace normalization")
        print("  ✓ Unicode/Hindi character safety")
        print("  ✓ Metadata enrichment")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n✅ Ready for Phase 2.3: Legal-Aware Chunking")
    print("   Preprocessed text will feed into the chunking pipeline")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
