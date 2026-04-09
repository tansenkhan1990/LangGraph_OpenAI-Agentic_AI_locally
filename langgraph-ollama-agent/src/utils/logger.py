"""
Logging configuration for the application
"""

import sys
from loguru import logger
import os
from datetime import datetime

def setup_logger():
    """Configure the logger for the application"""
    
    # Remove default logger
    logger.remove()
    
    # Add console logging
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
        level=os.getenv("LOG_LEVEL", "INFO"),
        colorize=True,
    )
    
    # Add file logging
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logger.add(
        f"{log_dir}/app_{datetime.now().strftime('%Y%m%d')}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} - {message}",
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
    )
    
    return logger

# Create a global logger instance
app_logger = setup_logger()