"""
app_actions.py - Opens apps and games on the system.
Add your app paths to the APPS dict below.
"""

import subprocess
import os
from utils.logger import logger


# Put the apps you want Nova to open here.
# The key is what you'd say (lowercase), the value is the .exe path.
APPS = {
    "chrome":   r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "vscode":   r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "valorant": r"C:\Riot Games\Riot Client\RiotClientServices.exe"
}


def open_app(app_name: str) -> str:
    # Lowercase it so "Chrome" and "chrome" both hit the same key
    app_key = app_name.lower().strip()

    if app_key not in APPS:
        logger.warning(f"App not in list: {app_key}")
        return f"I don't have {app_name} in my list. Add it to app_actions.py."

    app_path = APPS[app_key]

    # Make sure the file is actually there before trying to open it
    if not os.path.exists(app_path):
        logger.error(f"Path not found: {app_path}")
        return f"I know {app_name} but couldn't find it at the expected path."

    try:
        # Popen launches it as a separate process, Nova keeps running
        subprocess.Popen([app_path])
        logger.info(f"Opened: {app_name}")
        return f"Opening {app_name}."

    except Exception as e:
        logger.error(f"Failed to open {app_name}: {e}")
        return f"Something went wrong opening {app_name}."
