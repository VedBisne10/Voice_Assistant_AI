"""
file_helper.py - Read and write JSON files. All file I/O goes through here
so error handling lives in one place instead of scattered everywhere.
"""

import json  # standard library — parses JSON strings into Python dicts/lists and vice versa
from pathlib import Path  # cross-platform path objects — used in create_directory
from utils.logger import logger  # shared logger for the project


def load_json(file_path, default=None):  # read a JSON file and return its contents, or a safe default if something goes wrong
    # Default to empty list if the caller doesn't specify a fallback
    if default is None:  # caller didn't pass a default — use an empty list as a sensible fallback
        default = []  # empty list works for history; if you need a dict, pass default={} explicitly

    try:  # reading a file can fail in several ways — handle each case separately
        with open(file_path, "r", encoding="utf-8") as f:  # open for reading with explicit UTF-8 so non-ASCII characters survive
            data = json.load(f)  # parse the file contents into a Python object
        logger.info(f"Loaded JSON from {file_path}")  # confirm the load succeeded
        return data  # hand back the parsed data

    except FileNotFoundError:  # file doesn't exist yet — totally normal on first run
        # Normal on first run — the file just doesn't exist yet
        logger.error(f"File not found: {file_path}")  # log it anyway so we have a trace
        return default  # return the fallback so the caller doesn't have to handle None

    except json.JSONDecodeError:  # file exists but the JSON is broken — maybe it was corrupted
        # File exists but the contents are broken
        logger.error(f"Invalid JSON in: {file_path}")  # log which file has the bad content
        return default  # return the fallback rather than crashing


def save_json(file_path, data):  # write a Python object to a JSON file on disk
    try:  # writing can fail if the path doesn't exist or permissions are wrong
        with open(file_path, "w", encoding="utf-8") as f:  # open for writing, UTF-8 to handle any characters in the data
            # indent=4 keeps the file readable if you open it manually
            json.dump(data, f, indent=4)  # serialize the Python object to JSON with 4-space indentation
        logger.info(f"Saved JSON to {file_path}")  # confirm the write succeeded

    except Exception as e:  # catch any OS-level errors — permission denied, disk full, etc.
        logger.error(f"Failed to save JSON: {e}")  # log what went wrong — don't raise, just log


def create_directory(directory_path):  # ensure a directory exists, creating it and any missing parents if needed
    try:  # mkdir can fail if there are permission issues
        # parents=True creates any missing folders along the way
        # exist_ok=True means no error if the folder already exists
        Path(directory_path).mkdir(parents=True, exist_ok=True)  # safe to call even if the directory already exists
        logger.info(f"Directory ready: {directory_path}")  # log that the path is confirmed to exist

    except Exception as e:  # catch permission errors or other OS issues
        logger.error(f"Failed to create directory: {e}")  # log what went wrong
