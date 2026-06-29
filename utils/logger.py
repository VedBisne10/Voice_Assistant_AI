"""
logger.py - Sets up the shared logger used across the whole project.
Every module imports `logger` from here.
"""

import logging
from config.settings import ENABLE_CONSOLE_LOGS


def setup_logger():
    logger = logging.getLogger("VoiceAssistant")
    logger.setLevel(logging.INFO)

    # Guard against double-adding handlers if this gets called more than once
    if logger.handlers:
        return logger

    # Format: [INFO] 14:32:01 - Some message here
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    if ENABLE_CONSOLE_LOGS:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# One instance, shared everywhere via `from utils.logger import logger`
logger = setup_logger()
