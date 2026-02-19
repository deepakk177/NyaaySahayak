"""
Document Retrieval Logic
Retrieves relevant documents from FAISS index
"""

from typing import List, Dict
from backend.vectorstore.faiss_store import get_store
from backend.embeddings.embedder import embed_query
from backend.core.logging import get_logger

logger = get_logger()


class Retriever:
    """Document retriever using FAISS"""
    
    def __init__(self, top_k: int = 5):
        """
        Initialize retriever
        
        Args:
            top_k: Number of documents to retrieve
        """
        self.top_k = top_k
        self.store = get_store()
        logger.info(f"Retriever initialized with top_k={top_k}")
    
    def retrieve(self, query: str, k: int = None) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query text
            k: Number of documents to retrieve (overrides default)
        
        Returns:
            List of retrieved documents with metadata and scores
        """
        k = k or self.top_k
        
        logger.info(f"Retrieving documents for query: {query[:50]}...")
        
        # Generate query embedding
        query_embedding = embed_query(query)
        
        # Search in FAISS
        results = self.store.search(query_embedding, k=k)
        
        # Format results
        documents = []
        for idx, distance, metadata in results:
            documents.append({
                "id": idx,
                "text": metadata.get("text", ""),
                "section_title": metadata.get("section_title"),
                "source": metadata.get("source", "unknown"),
                "relevance_score": float(1 / (1 + distance)),  # Convert distance to similarity
                "metadata": metadata
            })
        
        logger.info(f"Retrieved {len(documents)} documents")
        return documents
    
    def retrieve_with_threshold(
        self,
        query: str,
        threshold: float = 0.5,
        max_docs: int = 10
    ) -> List[Dict]:
        """
        Retrieve documents with minimum relevance threshold
        
        Args:
            query: User query
            threshold: Minimum relevance score (0-1)
            max_docs: Maximum documents to consider
        
        Returns:
            Filtered list of relevant documents
        """
        documents = self.retrieve(query, k=max_docs)
        
        # Filter by threshold
        filtered = [
            doc for doc in documents
            if doc["relevance_score"] >= threshold
        ]
        
        logger.info(f"Filtered to {len(filtered)} documents above threshold {threshold}")
        return filtered


# Global retriever instance
_retriever = None


def get_retriever() -> Retriever:
    """Get or create global retriever"""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def retrieve_documents(query: str, k: int = 5) -> List[Dict]:
    """Convenience function for document retrieval"""
    return get_retriever().retrieve(query, k=k)
