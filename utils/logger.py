"""
logger.py

Handles application logging.
Used to display important system messages in a clean, readable format.
Every module in the project imports `logger` from here to log messages.
"""

import logging   # Python's built-in module for recording log messages

# Check settings to decide whether logs should be printed to the terminal
from config.settings import ENABLE_CONSOLE_LOGS


def setup_logger():
    """
    Creates and configures the main logger for the whole application.

    Returns:
        logging.Logger: Ready-to-use logger object
    """

    # Create (or retrieve if already exists) a logger with this specific name
    # Using a named logger instead of the root logger keeps our logs separate
    # from logs produced by third-party libraries
    logger = logging.getLogger("VoiceAssistant")

    # Set the minimum severity level of messages to capture
    # INFO = capture INFO, WARNING, ERROR, and CRITICAL (ignore DEBUG)
    logger.setLevel(logging.INFO)

    # If the logger already has handlers attached, it means setup_logger()
    # was called before — return early to avoid adding duplicate handlers
    # (which would cause every message to be printed multiple times)
    if logger.handlers:
        return logger

    # Define how each log line will look when printed
    # %(levelname)s → severity label e.g. INFO, WARNING, ERROR
    # %(asctime)s   → timestamp formatted by datefmt below e.g. 16:18:09
    # %(message)s   → the actual message passed to logger.info() / logger.error()
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%H:%M:%S"   # Show only hours:minutes:seconds (no date)
    )

    # Only add a console (terminal) handler if ENABLE_CONSOLE_LOGS is True in settings
    # StreamHandler prints log messages to the terminal (stdout)
    if ENABLE_CONSOLE_LOGS:
        console_handler = logging.StreamHandler()

        # Apply the formatter so terminal output matches our defined format
        console_handler.setFormatter(formatter)

        # Attach the handler to the logger so it knows where to send messages
        logger.addHandler(console_handler)

    return logger


# Run setup once and store the result in a module-level variable
# Every other file does: from utils.logger import logger
# They all share this same single logger instance
logger = setup_logger()
