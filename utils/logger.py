"""
logger.py - Sets up the shared logger used across the whole project.
Every module imports `logger` from here.
"""

import logging  # Python's built-in logging module — handles formatting, levels, and handlers
from config.settings import ENABLE_CONSOLE_LOGS  # setting that lets us toggle console output without touching this file


def setup_logger():  # creates and configures the project-wide logger, returns it
    logger = logging.getLogger("VoiceAssistant")  # named logger — using a name means all modules share the exact same instance
    logger.setLevel(logging.INFO)  # INFO and above (WARNING, ERROR, CRITICAL) will be logged — DEBUG messages are ignored

    # Guard against double-adding handlers if this gets called more than once
    if logger.handlers:  # check if handlers are already attached — this happens if setup_logger is called again
        return logger  # return early so we don't add duplicate handlers and print every message twice

    # Format: [INFO] 14:32:01 - Some message here
    formatter = logging.Formatter(  # defines how each log line will look
        "[%(levelname)s] %(asctime)s - %(message)s",  # levelname = INFO/WARNING/etc, asctime = timestamp, message = the actual text
        datefmt="%H:%M:%S"  # only show hours, minutes, seconds — no date noise in the console
    )

    if ENABLE_CONSOLE_LOGS:  # only add the console handler if settings say we want it
        handler = logging.StreamHandler()  # outputs to stdout — shows up in the terminal
        handler.setFormatter(formatter)  # attach our custom format to this handler
        logger.addHandler(handler)  # register the handler with the logger

    return logger  # hand back the fully configured logger


# One instance, shared everywhere via `from utils.logger import logger`
logger = setup_logger()  # create the logger at import time so every module that imports this gets the same object
