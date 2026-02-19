from backend.chunking.legal_chunker import LegalChunker

sample_text = """
SECTION 1
The landlord shall provide thirty days notice before eviction.

SECTION 2
A tenant may contest eviction in court.

SECTION 3
No eviction shall occur without due process.
"""

metadata = {
    "filename": "eviction_law.txt",
    "language": "en",
    "jurisdiction": "India"
}

chunker = LegalChunker(chunk_size=20, chunk_overlap=20)
chunks = chunker.chunk_text(sample_text, metadata)

for i, chunk in enumerate(chunks):
    print(f"\n--- CHUNK {i+1} ---")
    print(chunk["text"])
