import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.rag.pipeline import LegalRAGPipeline


rag = LegalRAGPipeline()


# Add some general law data first
print("Adding general law data...")
general_chunks = [
    {"text": "A landlord must provide thirty days notice before eviction."},
    {"text": "Wages must be paid within seven days after termination."}
]
general_metadata = {
    "filename": "general_eviction_law.txt",
    "source_type": "txt",
    "language": "en",
    "jurisdiction": "India"
}
rag.vector_manager.add_general_documents(general_chunks, general_metadata)


# Add user-specific document
print("Adding user document...")
user_chunks = [
    {"text": "According to your lease agreement, eviction requires 60 days notice, not 30."}
]
user_metadata = {
    "filename": "user_lease.pdf",
    "source_type": "pdf",
    "language": "en",
    "jurisdiction": "India"
}
rag.vector_manager.add_user_documents(user_chunks, user_metadata)


query = "What notice is required before eviction?"
print(f"\nQuerying: {query}")
response = rag.answer_query(query)


print("\n=== RAG RESPONSE ===\n")
print(response)
