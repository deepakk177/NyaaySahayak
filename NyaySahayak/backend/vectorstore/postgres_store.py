from sqlalchemy import text
from backend.db.session import SessionLocal, engine, Base
from sqlalchemy import text
from backend.db.session import SessionLocal, engine, Base
# Since I updated models.py, I'll use Chunk.

class PostgresVectorStore:
    def __init__(self):
        self.engine = engine
        self.Session = SessionLocal
        # Ensure the vector extension is enabled
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        # Create tables
        Base.metadata.create_all(self.engine)

    def add_document_chunks(self, chunks, embeddings, document_metadata):
        from backend.db.models import Document, Chunk
        session = self.Session()
        try:
            # 1. Create Document record
            document = Document(
                filename=document_metadata.get("filename"),
                source_type=document_metadata.get("source_type"),
                language=document_metadata.get("language"),
                jurisdiction=document_metadata.get("jurisdiction", "Unknown")
            )
            session.add(document)
            session.commit()
            session.refresh(document)

            # 2. Add Chunks
            for chunk_text, emb in zip(chunks, embeddings):
                new_chunk = Chunk(
                    document_id=document.id,
                    text=chunk_text,
                    embedding=emb,
                    metadata_json=document_metadata
                )
                session.add(new_chunk)
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def similarity_search(self, query_embedding, top_k=5):
        from backend.db.models import Chunk
        session = self.Session()
        try:
            # Using Cosine Distance
            results = session.query(Chunk).order_by(
                Chunk.embedding.cosine_distance(query_embedding)
            ).limit(top_k).all()
            
            return [
                {"text": r.text, "metadata": r.metadata_json or {}} 
                for r in results
            ]
        finally:
            session.close()
