"""
LLM Response Generator
Generates structured legal information responses using LLaMA/Mistral
"""


from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from backend.core.config import settings
from backend.core.logging import get_logger


logger = get_logger()




class LegalLLM:
    """
    Wrapper for LLaMA / Mistral style instruct models
    Generates context-bounded legal information responses
    """


    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.llm_model_name
        logger.info(f"Loading LLM: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=settings.llm_max_tokens,
                do_sample=True,
                temperature=settings.llm_temperature
            )
            logger.info("LLM loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load LLM: {e}")
            raise


    def generate(self, prompt: str) -> str:
        """
        Generate answer from prompt
        """
        try:
            logger.info("Generating LLM response")
            output = self.generator(prompt)
            generated_text = output[0]["generated_text"]
            
            # Extract only the new generation (remove prompt)
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "I apologize, but I encountered an error. Please consult a legal professional."
