"""
logger.py

Handles application logging.
Used to display important system messages in a clean format.
"""

import logging    # Import Python's built-in logging module
from config.settings import ENABLE_CONSOLE_LOGS    # Import settings to check whether console logging is enabled


def setup_logger():
    """
    Creates and configures the main logger.
    
    Returns:
        logging.Logger: Configured logger object
    """

    # Create a logger object for the application
    logger = logging.getLogger("VoiceAssistant")

    # Set minimum logging level
    # INFO means INFO, WARNING, ERROR all will be shown
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if logger is initialized multiple times
    if logger.handlers:
        return logger

    # Create format for log messages
    # %(levelname)s shows: INFO, WARNING, ERROR
    # %(asctime)s shows: 12:30:41
    # %(message)s shows: Assistant started
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%H:%M:%S"
    )

    # Add console handler if enabled in settings
    if ENABLE_CONSOLE_LOGS:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Create global logger object
logger = setup_logger()
