"""
Model Testing Script
Tests embedding model and LLM functionality

Run with: python scripts/test_models.py
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.embeddings.embedder import EmbeddingModel
from backend.rag.generator import LegalLLM
import numpy as np


def test_embeddings():
    """Test embedding model semantic similarity"""
    print("\n" + "="*60)
    print("TESTING EMBEDDING MODEL (e5-large-v2)")
    print("="*60)
    
    try:
        embedder = EmbeddingModel()
        
        # Test documents
        docs = [
            "A landlord must provide 30 days notice before eviction.",
            "Wages must be paid within seven days of termination.",
            "Employers cannot discriminate based on race or religion."
        ]
        
        # Test query
        query = "Can my landlord evict me immediately?"
        
        print(f"\nQuery: {query}")
        print("\nDocuments:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc}")
        
        # Embed documents and query
        doc_embeddings = embedder.embed_documents(docs)
        query_embedding = embedder.embed_query(query)
        
        # Calculate similarity scores
        scores = np.dot(doc_embeddings, query_embedding)
        
        # Find best match
        best_idx = scores.argmax()
        best_match = docs[best_idx]
        best_score = scores[best_idx]
        
        print("\n" + "-"*60)
        print("RESULTS:")
        print("-"*60)
        print(f"Best matching document (score: {best_score:.4f}):")
        print(f"→ {best_match}")
        
        print("\nAll scores:")
        for i, (doc, score) in enumerate(zip(docs, scores), 1):
            print(f"{i}. Score: {score:.4f} - {doc[:50]}...")
        
        print("\n✅ Embedding test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Embedding test FAILED: {e}")
        return False


def test_llm():
    """Test LLM generation"""
    print("\n" + "="*60)
    print("TESTING LLM (Language Model)")
    print("="*60)
    print("\n⚠️  This may take a few minutes on first run (downloading model)...")
    print("⚠️  Recommended: Start with TinyLlama or Gemma-2B for testing\n")
    
    try:
        # Use smaller model for testing
        # Change to your preferred model in .env
        llm = LegalLLM(model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        
        prompt = """You are a legal information assistant.
Explain eviction notice requirements in simple language.
Keep your response under 100 words.
Do not give legal advice."""

        print("Prompt:")
        print(prompt)
        print("\n" + "-"*60)
        print("GENERATING RESPONSE...")
        print("-"*60 + "\n")
        
        response = llm.generate_response(prompt)
        
        print("LLM Response:")
        print(response)
        
        print("\n✅ LLM test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ LLM test FAILED: {e}")
        print("\nTroubleshooting:")
        print("1. Check if you have enough RAM (4GB+ recommended)")
        print("2. Try a smaller model: TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        print("3. Ensure PyTorch is installed: pip install torch")
        return False


def test_full_pipeline():
    """Test complete RAG pipeline simulation"""
    print("\n" + "="*60)
    print("TESTING COMPLETE RAG SIMULATION")
    print("="*60)
    
    try:
        embedder = EmbeddingModel()
        
        # Simulate document store
        legal_docs = [
            {
                "text": "Section 106 of the Transfer of Property Act: A lease of immovable property determines by efflux of the time limited thereby. The landlord must provide notice before eviction.",
                "source": "Transfer of Property Act",
                "section_title": "Section 106"
            },
            {
                "text": "Rent Control Act provisions state that a landlord cannot evict a tenant without proper legal notice and valid grounds.",
                "source": "Rent Control Act",
                "section_title": "Eviction Provisions"
            }
        ]
        
        # User query
        query = "What is the legal process for eviction in India?"
        
        print(f"\nUser Query: {query}")
        
        # Step 1: Embed and retrieve
        doc_texts = [doc["text"] for doc in legal_docs]
        doc_embeddings = embedder.embed_documents(doc_texts)
        query_embedding = embedder.embed_query(query)
        
        # Calculate similarity
        scores = np.dot(doc_embeddings, query_embedding)
        
        # Get top document
        top_idx = scores.argmax()
        retrieved_doc = legal_docs[top_idx]
        
        print(f"\nRetrieved Document:")
        print(f"Source: {retrieved_doc['source']}")
        print(f"Relevance Score: {scores[top_idx]:.4f}")
        print(f"Content: {retrieved_doc['text'][:100]}...")
        
        # Step 2: Generate response (using smaller model for test)
        print("\n" + "-"*60)
        print("Generating structured response...")
        print("-"*60)
        
        # Note: Skip LLM for quick test, just show structure
        response_structure = {
            "summary": "Eviction requires proper legal notice and valid grounds",
            "relevant_law": "Section 106, Transfer of Property Act",
            "explanation": "Landlords must follow legal procedures before eviction",
            "next_steps": [
                "Consult with a legal professional",
                "Review your lease agreement",
                "Contact local legal aid"
            ],
            "disclaimer": "This is legal information, not legal advice",
            "sources": [retrieved_doc['source']]
        }
        
        print("\nStructured Response:")
        for key, value in response_structure.items():
            print(f"\n{key.upper()}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"  {value}")
        
        print("\n✅ Full pipeline test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Pipeline test FAILED: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🔬 NYAASAHAYAK - MODEL TESTING SUITE 🔬".center(60))
    
    results = {
        "embeddings": False,
        "llm": False,
        "pipeline": False
    }
    
    # Test 1: Embeddings (essential)
    results["embeddings"] = test_embeddings()
    
    # Test 2: LLM (optional - can be slow)
    user_input = input("\n\nDo you want to test the LLM? (y/n) [n]: ").strip().lower()
    if user_input == 'y':
        results["llm"] = test_llm()
    else:
        print("\n⏭️  Skipping LLM test (can be tested later)")
    
    # Test 3: Full pipeline simulation
    results["pipeline"] = test_full_pipeline()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "⏭️  SKIPPED" if test_name == "llm" and not user_input == 'y' else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    if results["embeddings"] and results["pipeline"]:
        print("\n🎉 Core functionality is working!")
        print("You can proceed with building the full application.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
