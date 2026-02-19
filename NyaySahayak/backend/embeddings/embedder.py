"""
Embedding Generation using e5-large-v2
Generates dense vector representations for semantic search
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger()


class EmbeddingModel:
    """
    Wrapper for e5-large-v2 embedding model
    Uses proper query/passage prefixes for optimal performance
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model_name
        logger.info(f"Loading embedding model: {self.model_name}")
        
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Embed document passages.
        e5 requires 'passage: ' prefix for documents.
        
        Args:
            texts: List of document texts to embed
        
        Returns:
            Normalized embeddings as numpy array
        """
        if not texts:
            logger.warning("Empty text list provided for embedding")
            return np.array([])
        
        # Add passage prefix for e5 models
        prefixed_texts = [f"passage: {text}" for text in texts]
        
        logger.info(f"Embedding {len(texts)} documents")
        embeddings = self.model.encode(
            prefixed_texts, 
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 10
        )
        
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embed user query.
        e5 requires 'query: ' prefix for search queries.
        
        Args:
            query: Search query text
        
        Returns:
            Normalized query embedding
        """
        logger.info(f"Embedding query: {query[:50]}...")
        
        embedding = self.model.encode(
            f"query: {query}",
            normalize_embeddings=True
        )
        
        return embedding


# Global embedder instance (lazy loaded)
_embedder = None


def get_embedder() -> EmbeddingModel:
    """Get or create global embedder instance"""
    global _embedder
    if _embedder is None:
        _embedder = EmbeddingModel()
    return _embedder


def embed_text(text: str) -> np.ndarray:
    """Convenience function for single document embedding"""
    return get_embedder().embed_documents([text])[0]


def embed_query(query: str) -> np.ndarray:
    """Convenience function for query embedding"""
    return get_embedder().embed_query(query)


def embed_batch(texts: List[str]) -> np.ndarray:
    """Convenience function for batch embedding"""
    return get_embedder().embed_documents(texts)
