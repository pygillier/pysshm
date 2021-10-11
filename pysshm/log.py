"""Loguru configuration for project"""
import sys
from loguru import logger


def configure(debug: bool) -> None:
    """Configure loguru with correct debug level"""
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "{message}",
                "level": "DEBUG" if debug else "INFO",
            },
        ]
    }
    logger.configure(**config)
