"""
Ingest General Laws Script
Processes legal documents and adds them to the vector store
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.loaders import load_document
from backend.ingestion.preprocessing import preprocess_text
from backend.chunking.legal_chunker import chunk_document
from backend.embeddings.embedder import get_embedder
from backend.vectorstore.faiss_store import get_store
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger()


def ingest_directory(directory: Path, category: str):
    """
    Ingest all documents from a directory
    
    Args:
        directory: Path to directory containing documents
        category: Legal category (e.g., 'eviction', 'labor')
    """
    logger.info(f"Ingesting documents from {directory}")
    
    # Find all document files
    supported_extensions = ['.pdf', '.docx', '.txt']
    files = []
    for ext in supported_extensions:
        files.extend(directory.glob(f"**/*{ext}"))
    
    if not files:
        logger.warning(f"No documents found in {directory}")
        return
    
    logger.info(f"Found {len(files)} documents to process")
    
    embedder = get_embedder()
    store = get_store()
    
    for file_path in files:
        try:
            logger.info(f"Processing: {file_path.name}")
            
            # Load document
            text = load_document(str(file_path))
            
            # Preprocess
            text = preprocess_text(text, deep_clean=True)
            
            # Chunk
            chunks = chunk_document(text, preserve_sections=True)
            
            # Add metadata
            for chunk in chunks:
                chunk['source'] = file_path.name
                chunk['category'] = category
                chunk['file_path'] = str(file_path)
            
            # Generate embeddings
            chunk_texts = [c['text'] for c in chunks]
            embeddings = embedder.embed_batch(chunk_texts)
            
            # Add to store
            store.add_documents(embeddings, chunks)
            
            logger.info(f"✓ Ingested {file_path.name}: {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"✗ Failed to ingest {file_path.name}: {e}")
    
    # Save index
    store.save(settings.faiss_index_path)
    logger.info(f"Index saved to {settings.faiss_index_path}")


def main():
    """Main ingestion script"""
    logger.info("Starting general laws ingestion")
    
    base_path = Path(__file__).parent.parent / "data" / "general_laws"
    
    categories = ["eviction", "labor", "welfare"]
    
    for category in categories:
        category_path = base_path / category
        if category_path.exists():
            ingest_directory(category_path, category)
    
    logger.info("Ingestion complete!")


if __name__ == "__main__":
    main()
