import faiss
import numpy as np
import os
from typing import List, Dict
from backend.embeddings.embedder import EmbeddingModel
from backend.db.session import SessionLocal
from backend.db.models import Document, Chunk




class FAISSVectorStore:
    def __init__(self, embedding_dim: int = 1024, index_path: str = None):
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.embedder = EmbeddingModel()
        
        # Load existing index if path provided and exists
        if index_path and os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            self.index = faiss.IndexFlatIP(embedding_dim)


    def add_document_chunks(
        self,
        chunks: List[Dict],
        document_metadata: Dict
    ):
        """
        Store document in DB and embeddings in FAISS.
        """


        db = SessionLocal()


        # 1. Create Document record
        document = Document(
            filename=document_metadata.get("filename"),
            source_type=document_metadata.get("source_type"),
            language=document_metadata.get("language"),
            jurisdiction=document_metadata.get("jurisdiction", "Unknown")
        )
        db.add(document)
        db.commit()
        db.refresh(document)


        # 2. Embed chunks
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.embed_documents(texts).astype("float32")


        # 3. Add to FAISS
        start_index = self.index.ntotal
        self.index.add(embeddings)


        # 4. Store chunk records with FAISS index mapping
        for i, chunk in enumerate(chunks):
            chunk_record = Chunk(
                document_id=document.id,
                faiss_index_id=start_index + i,
                text=chunk["text"]
            )
            db.add(chunk_record)


        db.commit()
        db.close()


    def similarity_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve results using FAISS and fetch metadata from DB.
        """


        db = SessionLocal()


        query_embedding = self.embedder.embed_query(query).astype("float32")
        query_embedding = np.expand_dims(query_embedding, axis=0)


        scores, indices = self.index.search(query_embedding, top_k)


        results = []


        for idx in indices[0]:
            chunk = (
                db.query(Chunk)
                .filter(Chunk.faiss_index_id == int(idx))
                .first()
            )
            if chunk:
                results.append({
                    "text": chunk.text,
                    "document_id": str(chunk.document_id)
                })


        db.close()
        return results


    def save_index(self, path: str = None):
        """
        Save FAISS index to disk
        """
        save_path = path or self.index_path
        if save_path:
            faiss.write_index(self.index, save_path)
            print(f"Index saved to {save_path}")
        else:
            print("Warning: No index path specified, index not saved")


    def load_index(self, path: str):
        """
        Load FAISS index from disk
        """
        if os.path.exists(path):
            self.index = faiss.read_index(path)
            self.index_path = path
            print(f"Index loaded from {path}")
        else:
            print(f"Warning: Index file not found at {path}")
