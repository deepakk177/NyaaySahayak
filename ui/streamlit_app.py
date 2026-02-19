import streamlit as st
import os

from backend.ingestion.loaders import load_document
from backend.ingestion.preprocessing import preprocess_document
from backend.chunking.legal_chunker import LegalChunker
from backend.vectorstore.vector_manager import VectorManager
from backend.rag.pipeline import LegalRAGPipeline


# Initialize core components
chunker = LegalChunker()
vector_manager = VectorManager()
rag_pipeline = LegalRAGPipeline()


# ---------------- Sidebar ----------------
st.sidebar.title("Legal Assistant")

st.sidebar.markdown("### Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / TXT / DOCX",
    type=["pdf", "txt", "docx"]
)

jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["India", "Other"]
)

st.sidebar.markdown("---")
st.sidebar.warning(
    "This system provides legal information only, not legal advice."
)


# ---------------- Document Processing ----------------
if uploaded_file is not None:
    file_path = os.path.join("data/samples/test_docs", uploaded_file.name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    file_type = uploaded_file.name.split(".")[-1]

    # Load document
    doc = load_document(file_path, file_type)

    # Preprocess
    clean_text, metadata = preprocess_document(doc["text"], doc["metadata"])

    metadata["jurisdiction"] = jurisdiction

    # Chunk
    chunks = chunker.chunk_text(clean_text, metadata)

    # Add to USER vector store
    vector_manager.add_user_documents(chunks, metadata)

    st.sidebar.success("Document processed and indexed.")


# ---------------- Chat UI ----------------
st.title("Multilingual Legal Document Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# User input
user_query = st.chat_input("Ask your legal question...")


if user_query:
    # Save user message
    st.session_state.chat_history.append(("user", user_query))

    # Get response from RAG
    response = rag_pipeline.answer_query(user_query)

    # Save assistant message
    st.session_state.chat_history.append(("assistant", response))


# Display chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)
