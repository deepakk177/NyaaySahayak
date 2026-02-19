"""
Global Configuration Management
Loads environment variables and provides centralized config access
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application Settings"""
    
    # LLM Configuration
    llm_model_name: str = "meta-llama/Llama-3-8B-Instruct"
    llm_api_key: str = ""
    llm_api_base_url: str = "http://localhost:8000/v1"
    llm_max_tokens: int = 512
    llm_temperature: float = 0.3
    
    # Embedding Configuration
    embedding_model_name: str = "intfloat/e5-large-v2"
    embedding_device: str = "cpu"
    
    # Vector Store
    faiss_index_path: str = "./data/faiss_index"
    chunk_size: int = 700
    chunk_overlap: int = 100
    
    # Database
    database_url: str = "postgresql://localhost:5432/nyaasahayak"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    
    # Translation
    default_language: str = "en"
    supported_languages: List[str] = ["en", "hi"]
    translation_model: str = "indicnlp/IndicTrans2"
    
    # OCR
    tesseract_path: str = "/usr/bin/tesseract"
    tesseract_lang: str = "eng+hin"
    
    # Document Storage
    upload_dir: str = "./data/uploads"
    max_upload_size_mb: int = 10
    session_expiry_hours: int = 24
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    cors_origins: List[str] = ["http://localhost:8501"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Security
    secret_key: str = "change-this-secret-key"
    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True
    
    # Feature Flags
    enable_translation: bool = True
    enable_ocr: bool = True
    enable_metadata_logging: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings
