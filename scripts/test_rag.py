from backend.rag.pipeline import LegalRAGPipeline


rag = LegalRAGPipeline()

# Ensure we have some data in the store for testing
print("Adding sample data...")
chunks = [
    {"text": "A landlord must provide thirty days notice before eviction."},
    {"text": "Wages must be paid within seven days after termination."}
]
document_metadata = {
    "filename": "test_law.txt",
    "source_type": "txt",
    "language": "en",
    "jurisdiction": "India"
}
rag.vector_store.add_document_chunks(chunks, document_metadata)

query = "Can my landlord evict me without notice?"
print(f"Querying: {query}")
response = rag.answer_query(query)


print("\n=== RAG RESPONSE ===\n")
print(response)
