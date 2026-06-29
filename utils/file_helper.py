"""
file_helper.py - Read and write JSON files. All file I/O goes through here
so error handling lives in one place instead of scattered everywhere.
"""

import json
from pathlib import Path
from utils.logger import logger


def load_json(file_path, default=None):
    # Default to empty list if the caller doesn't specify a fallback
    if default is None:
        default = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded JSON from {file_path}")
        return data

    except FileNotFoundError:
        # Normal on first run — the file just doesn't exist yet
        logger.error(f"File not found: {file_path}")
        return default

    except json.JSONDecodeError:
        # File exists but the contents are broken
        logger.error(f"Invalid JSON in: {file_path}")
        return default


def save_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # indent=4 keeps the file readable if you open it manually
            json.dump(data, f, indent=4)
        logger.info(f"Saved JSON to {file_path}")

    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")


def create_directory(directory_path):
    try:
        # parents=True creates any missing folders along the way
        # exist_ok=True means no error if the folder already exists
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory_path}")

    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
