"""
app_actions.py - Opens apps and games on the system.
Add your app paths to the APPS dict below.
"""

import subprocess  # used to launch executables as separate processes
import os  # used to check if the .exe path actually exists on disk
from utils.logger import logger  # shared logger for the project


# Put the apps you want Nova to open here.
# The key is what you'd say (lowercase), the value is the .exe path.
APPS = {  # maps app names to their full .exe paths — add any app you want Nova to launch
    "chrome":   r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",  # Google Chrome browser
    "vscode":   r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe",  # Visual Studio Code editor
    "valorant": r"C:\Riot Games\Riot Client\RiotClientServices.exe"  # Riot client that launches Valorant
}


def open_app(app_name: str) -> str:  # look up the app by name and launch it as a subprocess
    # Lowercase it so "Chrome" and "chrome" both hit the same key
    app_key = app_name.lower().strip()  # normalize the input so casing and stray spaces don't cause misses

    if app_key not in APPS:  # the app name wasn't in our registry
        logger.warning(f"App not in list: {app_key}")  # log the miss so we know to add it if needed
        return f"I don't have {app_name} in my list. Add it to app_actions.py."  # spoken response pointing to the fix

    app_path = APPS[app_key]  # get the full .exe path for this app

    # Make sure the file is actually there before trying to open it
    if not os.path.exists(app_path):  # path is in the dict but the file isn't there on this machine
        logger.error(f"Path not found: {app_path}")  # log the bad path so it's easy to spot
        return f"I know {app_name} but couldn't find it at the expected path."  # spoken response explaining the issue

    try:  # the launch itself could fail — wrap it
        # Popen launches it as a separate process, Nova keeps running
        subprocess.Popen([app_path])  # fire and forget — doesn't wait for the app to open or close
        logger.info(f"Opened: {app_name}")  # confirm it launched
        return f"Opening {app_name}."  # short, natural spoken response

    except Exception as e:  # something went wrong at the OS level
        logger.error(f"Failed to open {app_name}: {e}")  # log the actual error
        return f"Something went wrong opening {app_name}."  # spoken fallback
