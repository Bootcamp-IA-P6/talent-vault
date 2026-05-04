import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} | {message}",
    level="INFO",
)
logger.add(
    "logs/talent_vault.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)
