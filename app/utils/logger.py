from loguru import logger
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logger.add(
    "logs/app.log",
    rotation="500 KB",
    retention="10 days",
    level="INFO",
    format="{time} | {level} | {message}"
)

def get_logger():
    return logger