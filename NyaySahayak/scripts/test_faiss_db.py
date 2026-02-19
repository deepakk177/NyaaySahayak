from backend.vectorstore.faiss_store import FAISSVectorStore


store = FAISSVectorStore()


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


store.add_document_chunks(chunks, document_metadata)


query = "Can my landlord evict me immediately?"
results = store.similarity_search(query)


print("\nTop Results:")
for r in results:
    print(r["text"])
