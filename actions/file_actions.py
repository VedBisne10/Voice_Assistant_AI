"""
file_actions.py - Opening folders, files, and searching for files by name.
Add your own folders to the FOLDERS dict below.
"""

import os  # used for path existence checks, startfile, and joining paths
import subprocess  # used to open Explorer windows for folders
from utils.logger import logger  # shared logger for the project


# Folder shortcuts — the key is what you say, the value is the actual path.
FOLDERS = {  # maps spoken folder names to their actual disk paths — add yours here
    "desktop":   r"C:\Users\HP\OneDrive\Desktop",  # the user's OneDrive-synced desktop
    "downloads": r"C:\Users\HP\Downloads",  # standard Downloads folder
    "documents": r"C:\Users\HP\OneDrive\文档",  # OneDrive documents — note the Chinese folder name
    "pictures":  r"C:\Users\HP\OneDrive\Pictures",  # OneDrive pictures folder
    "music":     r"C:\Users\HP\Music",  # local music folder
    "videos":    r"C:\Users\HP\Videos",  # local videos folder
    "projects":  r"C:\Users\HP\OneDrive\Desktop\Projects"  # custom shortcut to the dev projects folder
}


def open_folder(folder_name: str) -> str:  # look up a folder by name and open it in Windows Explorer
    folder_key = folder_name.lower().strip()  # normalize input so "Downloads" and "downloads" both work

    if folder_key not in FOLDERS:  # the folder name isn't in our registry
        logger.warning(f"Unknown folder: {folder_key}")  # log the miss
        return f"I don't have a folder called {folder_name}. Add it to file_actions.py."  # spoken response pointing to the fix

    folder_path = FOLDERS[folder_key]  # get the actual disk path

    if not os.path.exists(folder_path):  # path is registered but doesn't exist on this machine
        logger.error(f"Folder missing on disk: {folder_path}")  # log the bad path
        return f"The path for {folder_name} doesn't exist on this machine."  # spoken error response

    subprocess.Popen(["explorer", folder_path])  # open Explorer at this path — non-blocking, Nova keeps running
    logger.info(f"Opened folder: {folder_path}")  # log the opened path
    return f"Opening your {folder_name} folder."  # spoken confirmation


def open_file(file_path: str) -> str:  # open a file using whatever Windows app handles that file type
    if not os.path.exists(file_path):  # file doesn't exist at the given path
        logger.error(f"File not found: {file_path}")  # log the missing file
        return f"Couldn't find a file at {file_path}."  # spoken error

    # startfile hands the file off to whatever Windows app handles that type
    os.startfile(file_path)  # equivalent to double-clicking the file in Explorer
    logger.info(f"Opened file: {file_path}")  # log the opened file

    file_name = os.path.basename(file_path)  # extract just the filename from the full path for the spoken response
    return f"Opening {file_name}."  # spoken confirmation using just the filename, not the full path


def find_file(file_name: str, folder_name: str = "documents") -> str:  # search for a file by name and open it if found
    folder_key = folder_name.lower().strip()  # normalize the folder name

    if folder_key not in FOLDERS:  # the search folder isn't in our registry
        return f"I don't know the folder '{folder_name}'. Add it to file_actions.py."  # spoken error

    folder_path = FOLDERS[folder_key]  # get the actual path to search in

    # Walk the whole folder tree looking for a filename that contains the search term
    for root, dirs, files in os.walk(folder_path):  # os.walk recursively yields (dirpath, subdirs, files) for every folder
        for f in files:  # check each file in the current directory level
            if file_name.lower() in f.lower():  # case-insensitive substring match — "report" finds "Monthly_Report.xlsx"
                full_path = os.path.join(root, f)  # build the complete file path from the directory and filename
                os.startfile(full_path)  # open the file with its default application
                logger.info(f"Found and opened: {full_path}")  # log the full path of what was opened
                return f"Found {f}, opening it now."  # spoken confirmation with the actual filename

    logger.warning(f"No file matching '{file_name}' in {folder_path}")  # log that the search came up empty
    return f"Couldn't find anything named {file_name} in your {folder_name} folder."  # spoken response when nothing matches
