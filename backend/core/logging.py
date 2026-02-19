"""
Centralized Logging Configuration
Uses loguru for structured, context-aware logging
"""

import sys
from loguru import logger
from pathlib import Path
from .config import settings


def setup_logging():
    """Configure application-wide logging"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler with color
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File handler
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        settings.log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )
    
    logger.info("Logging configured successfully")
    return logger


# Initialize logger
app_logger = setup_logging()


def get_logger():
    """Get application logger instance"""
    return app_logger
