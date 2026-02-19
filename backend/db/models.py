from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime
from backend.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    source_type = Column(String)
    language = Column(String)
    jurisdiction = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    text = Column(String)
    metadata_json = Column(JSON)
    embedding = Column(Vector(1024))  # Adjust dimension based on your model (e5-large is usually 1024)
    faiss_index_id = Column(Integer)  # Keeping for backward compatibility or hybrid use
    created_at = Column(DateTime, default=datetime.utcnow)

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(String)
    language = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
