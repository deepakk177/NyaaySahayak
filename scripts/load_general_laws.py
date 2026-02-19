import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ingestion.loaders import load_document
from backend.ingestion.preprocessing import preprocess_document
from backend.chunking.legal_chunker import LegalChunker
from backend.vectorstore.vector_manager import VectorManager


DATA_PATH = "data/general_laws"


chunker = LegalChunker()
vector_manager = VectorManager()




def process_file(file_path):
    ext = file_path.split(".")[-1]


    try:
        doc = load_document(file_path, ext)
        clean_text, metadata = preprocess_document(doc["text"], doc["metadata"])

        metadata["jurisdiction"] = "India"

        chunks = chunker.chunk_text(clean_text, metadata)

        vector_manager.add_general_documents(chunks, metadata)
        print(f"Successfully indexed: {file_path}")
        
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")




for root, _, files in os.walk(DATA_PATH):
    for file in files:
        if file.endswith(('.txt', '.pdf', '.docx', '.doc')):
            path = os.path.join(root, file)
            print("Loading:", path)
            process_file(path)


print("General laws processed.")
