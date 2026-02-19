from backend.vectorstore.vector_manager import VectorManager
from backend.rag.generator import LegalLLM
from backend.db.session import SessionLocal
from backend.db.models import QueryLog
import os




class LegalRAGPipeline:
    def __init__(self):
        self.vector_manager = VectorManager()
        self.llm = LegalLLM()
        self.system_prompt = self._load_system_prompt()


    def _load_system_prompt(self):
        path = os.path.join(
            "backend",
            "prompts",
            "system_prompt.txt"
        )
        with open(path, "r", encoding="utf-8") as f:
            return f.read()


    def _build_context(self, retrieved_chunks):
        """
        Combine retrieved texts into a single context block.
        """
        context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
        return context


    def _build_prompt(self, query, context):
        prompt = f"""
{self.system_prompt}


Context:
{context}


User Question:
{query}


Answer:
"""
        return prompt


    def answer_query(self, query: str, language: str = "en"):
        """
        Full RAG flow
        """


        # 1. Retrieve relevant chunks
        retrieved_chunks = self.vector_manager.search(query, top_k=5)


        if not retrieved_chunks:
            return "No relevant legal information found."


        # 2. Build context
        context = self._build_context(retrieved_chunks)


        # 3. Build prompt
        prompt = self._build_prompt(query, context)


        # 4. Generate answer
        response = self.llm.generate(prompt)


        # 5. Log query
        db = SessionLocal()
        log = QueryLog(
            query_text=query,
            language=language
        )
        db.add(log)
        db.commit()
        db.close()


        return response
