"""
file_helper.py

Provides helper functions for reading, writing,
and managing files used by the Voice Assistant.

All file I/O across the project goes through these functions
so error handling is done in one place.
"""

import json           # Built-in module to read and write JSON data
from pathlib import Path   # Safe cross-platform file path handling
from utils.logger import logger   # Shared logger for recording info/errors


def load_json(file_path, default=None):
    """
    Load and return data from a JSON file.

    Args:
        file_path (Path): Path to the JSON file to read
        default: Value to return if the file doesn't exist or has an error

    Returns:
        dict or list: The loaded data, or the default value on failure
    """

    # If the caller didn't provide a fallback value, default to an empty list
    # This avoids returning None which could cause errors in calling code
    if default is None:
        default = []

    try:
        # Open the file in read mode with UTF-8 encoding
        # 'with' ensures the file is automatically closed after reading
        with open(file_path, "r", encoding="utf-8") as file:
            # Parse the JSON text from the file into a Python dict or list
            data = json.load(file)

        logger.info(f"Loaded JSON from {file_path}")
        return data

    except FileNotFoundError:
        # File doesn't exist yet — this is normal on first run, return the default
        logger.error(f"File not found: {file_path}")
        return default

    except json.JSONDecodeError:
        # File exists but contains invalid/corrupted JSON — return the default safely
        logger.error(f"Invalid JSON format in: {file_path}")
        return default


def save_json(file_path, data):
    """
    Save Python data (dict or list) to a JSON file.
    Overwrites the file if it already exists.

    Args:
        file_path (Path): Path to the JSON file to write
        data (dict or list): The data to save
    """

    try:
        # Open the file in write mode — creates the file if it doesn't exist,
        # overwrites it if it does
        with open(file_path, "w", encoding="utf-8") as file:
            # Convert Python data to formatted JSON and write it to the file
            # indent=4 makes the output human-readable with 4-space indentation
            json.dump(data, file, indent=4)

        logger.info(f"Saved JSON to {file_path}")

    except Exception as error:
        # Catch any unexpected error (permissions, disk full, etc.) and log it
        logger.error(f"Failed to save JSON: {error}")


def create_directory(directory_path):
    """
    Create a folder at the given path if it doesn't already exist.
    Also creates any missing parent folders along the way.

    Args:
        directory_path (Path): The folder path to create
    """

    try:
        # parents=True  → also creates any missing parent folders automatically
        # exist_ok=True → don't raise an error if the folder already exists
        Path(directory_path).mkdir(parents=True, exist_ok=True)

        logger.info(f"Directory ready: {directory_path}")

    except Exception as error:
        # Log any failure (e.g., permission denied) without crashing the app
        logger.error(f"Failed to create directory: {error}")
