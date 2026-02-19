from backend.vectorstore.faiss_store import FAISSVectorStore
from backend.vectorstore.postgres_store import PostgresVectorStore
from backend.embeddings.embedder import EmbeddingModel
import os


class VectorManager:
    """
    Manages two vector stores:
    1. General law knowledge base (Persistent via PostgreSQL/pgvector)
    2. User uploaded documents (Session-based via FAISS)
    """

    def __init__(self):
        # Persistent storage for general laws
        self.general_store = PostgresVectorStore()
        
        # Session storage for user uploads (temporary, fast)
        os.makedirs("data/indexes", exist_ok=True)
        self.user_store = FAISSVectorStore(
            index_path="data/indexes/faiss_user.index"
        )
        
        self.embedder = EmbeddingModel()

    def add_general_documents(self, chunks, metadata):
        """Add documents to the persistent database store"""
        metadata["source"] = "general"
        texts = [c["text"] if isinstance(c, dict) else c for c in chunks]
        embeddings = self.embedder.embed_documents(texts)
        self.general_store.add_document_chunks(texts, embeddings, metadata)

    def add_user_documents(self, chunks, metadata):
        """Add documents to the local FAISS index (session-only)"""
        metadata["source"] = "user"
        self.user_store.add_document_chunks(chunks, metadata)
        self.user_store.save_index()

    def search(self, query, top_k=5):
        """Hybrid search with priority for user documents"""
        query_emb = self.embedder.embed_query(query)
        
        # Search User FAISS first
        user_results = self.user_store.similarity_search(query, top_k)
        
        # Search General Postgres
        general_results = self.general_store.similarity_search(query_emb, top_k)

        # Merge results, prioritizing user docs
        combined = user_results + general_results
        return combined[:top_k]
