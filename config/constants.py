"""
constants.py

Stores constant paths and fixed values used across the project.
These values don't change during runtime — they define where files live
and what Nova's core personality/instructions are.
"""

# Path is used to work with file/folder paths safely across Windows, Linux, and Mac
# It's better than plain strings because it handles slashes automatically
from pathlib import Path

# __file__ = the full path to this file (constants.py)
# .resolve() = converts it to an absolute path (no relative ".." parts)
# .parent = goes one folder up (from config/ to VoiceAssistant/)
# .parent again = goes up one more level if needed — here it gives us the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# The folder where all data files (memory, history, audio) are stored
DATA_FOLDER = PROJECT_ROOT / "data"

# Full path to the JSON file that stores long-term memory facts about the user
MEMORY_FILE = DATA_FOLDER / "memory.json"

# Full path to the JSON file that stores the conversation history (chat log)
CONVERSATION_HISTORY_FILE = DATA_FOLDER / "conversation_history.json"

# Folder where log files are written (one log file per session/day)
LOG_FOLDER = DATA_FOLDER / "logs"

# Folder where icons, sounds, and wake word models are stored
ASSETS_FOLDER = PROJECT_ROOT / "assets"

# Path to the temporary WAV file created every time the user speaks
# This file gets overwritten on each recording — it's not saved permanently
TEMP_AUDIO_FILE = DATA_FOLDER / "temp_audio.wav"

# The system prompt that defines who Nova is and how she should behave
# This is sent to the AI at the start of every conversation as a "role" instruction
# Think of it as the personality and rule sheet for the AI
SYSTEM_PROMPT = """
You are Nova, a desktop AI voice assistant created by Ved.

Your personality:
- Helpful
- Smart
- Friendly
- Conversational
- Concise unless detailed explanation is needed

Rules:
- Use memory when relevant
- Remember user preferences
- Give practical and accurate responses
"""
