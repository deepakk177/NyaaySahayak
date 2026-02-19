from backend.vectorstore.faiss_store import FAISSVectorStore


chunks = [
    {
        "text": "A landlord must provide thirty days notice before eviction.",
        "metadata": {"doc": "eviction_law"}
    },
    {
        "text": "Wages must be paid within seven days of termination.",
        "metadata": {"doc": "labor_law"}
    }
]


store = FAISSVectorStore()


store.add_documents(chunks)


query = "Can my landlord evict me immediately?"
results = store.similarity_search(query)


print("Top Result:")
print(results[0]["text"])


# Save & reload
store.save("faiss.index", "metadata.pkl")


new_store = FAISSVectorStore()
new_store.load("faiss.index", "metadata.pkl")


results_after_reload = new_store.similarity_search(query)
print("\nAfter Reload:")
print(results_after_reload[0]["text"])
