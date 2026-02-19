from backend.rag.generator import LegalLLM
import torch

try:
    print("Initializing LegalLLM...")
    llm = LegalLLM()
    print("Generating simple test...")
    res = llm.generate("Hello, who are you?")
    print(f"Result: {res}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
