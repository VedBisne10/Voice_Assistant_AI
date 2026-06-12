"""
file_helper.py

Provides helper functions for reading, writing,
and managing files used by the Voice Assistant.
"""

import json
from pathlib import Path
from utils.logger import logger


def load_json(file_path, default=None):
    """
    Load data from a JSON file.

    Args:
        file_path (Path): Path to JSON file

    Returns:
        dict or list: Loaded JSON data
    """

    # If caller doesn't provide a default,
    # use empty dictionary as fallback
    if default is None:
        default = {}

    try:
        # Open file in read mode
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        logger.info(f"Loaded JSON from {file_path}")
        return data

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return default

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in: {file_path}")
        return default


def save_json(file_path, data):
    """
    Save Python data into a JSON file.

    Args:
        file_path (Path): Path to JSON file
        data (dict/list): Data to save
    """

    try:
        # Open file in write mode
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.info(f"Saved JSON to {file_path}")

    except Exception as error:
        logger.error(f"Failed to save JSON: {error}")


def create_directory(directory_path):
    """
    Create directory if it doesn't exist.

    Args:
        directory_path (Path): Folder path
    """

    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory_path}")

    except Exception as error:
        logger.error(f"Failed to create directory: {error}")