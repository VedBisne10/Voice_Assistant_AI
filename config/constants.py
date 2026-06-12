"""
constants.py

Stores constant paths and fixed values used across the project.
These usually do not change unless the project structure changes.
"""

# Path is used to work with folders/files safely across Windows, Linux, and Mac
from pathlib import Path

# Root folder of the project (VoiceAssistant/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folder path
DATA_FOLDER = PROJECT_ROOT / "data"

# Memory file path
MEMORY_FILE = DATA_FOLDER / "memory.json"

# Conversation history file path
CONVERSATION_HISTORY_FILE = DATA_FOLDER / "conversation_history.json"

# Logs folder path
LOG_FOLDER = DATA_FOLDER / "logs"

# Assets folder path
ASSETS_FOLDER = PROJECT_ROOT / "assets"