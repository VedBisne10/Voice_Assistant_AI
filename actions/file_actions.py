"""
file_actions.py - Opening folders, files, and searching for files by name.
Add your own folders to the FOLDERS dict below.
"""

import os
import subprocess
from utils.logger import logger


# Folder shortcuts — the key is what you say, the value is the actual path.
FOLDERS = {
    "desktop":   r"C:\Users\HP\OneDrive\Desktop",
    "downloads": r"C:\Users\HP\Downloads",
    "documents": r"C:\Users\HP\OneDrive\文档",
    "pictures":  r"C:\Users\HP\OneDrive\Pictures",
    "music":     r"C:\Users\HP\Music",
    "videos":    r"C:\Users\HP\Videos",
    "projects":  r"C:\Users\HP\OneDrive\Desktop\Projects"
}


def open_folder(folder_name: str) -> str:
    folder_key = folder_name.lower().strip()

    if folder_key not in FOLDERS:
        logger.warning(f"Unknown folder: {folder_key}")
        return f"I don't have a folder called {folder_name}. Add it to file_actions.py."

    folder_path = FOLDERS[folder_key]

    if not os.path.exists(folder_path):
        logger.error(f"Folder missing on disk: {folder_path}")
        return f"The path for {folder_name} doesn't exist on this machine."

    subprocess.Popen(["explorer", folder_path])
    logger.info(f"Opened folder: {folder_path}")
    return f"Opening your {folder_name} folder."


def open_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return f"Couldn't find a file at {file_path}."

    # startfile hands the file off to whatever Windows app handles that type
    os.startfile(file_path)
    logger.info(f"Opened file: {file_path}")

    file_name = os.path.basename(file_path)
    return f"Opening {file_name}."


def find_file(file_name: str, folder_name: str = "documents") -> str:
    folder_key = folder_name.lower().strip()

    if folder_key not in FOLDERS:
        return f"I don't know the folder '{folder_name}'. Add it to file_actions.py."

    folder_path = FOLDERS[folder_key]

    # Walk the whole folder tree looking for a filename that contains the search term
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if file_name.lower() in f.lower():
                full_path = os.path.join(root, f)
                os.startfile(full_path)
                logger.info(f"Found and opened: {full_path}")
                return f"Found {f}, opening it now."

    logger.warning(f"No file matching '{file_name}' in {folder_path}")
    return f"Couldn't find anything named {file_name} in your {folder_name} folder."
