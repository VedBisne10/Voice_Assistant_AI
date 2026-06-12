"""
settings.py

Stores all configurable settings for the Voice Assistant.
Change values here instead of modifying multiple files.
"""

# Assistant settings
ASSISTANT_NAME = "Nova"

STARTUP_MESSAGE = (
    f"Hello, {ASSISTANT_NAME} at your service Sir. "
)

# Controls how fast the assistant speaks.
SPEECH_RATE = 180

# Controls the assistant's speaking volume.
SPEECH_VOLUME = 1.0

# AI model used to understand queries
# and generate intelligent responses.
MODEL_NAME = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

# Number of recent messages to keep as conversation context.
MAX_CONVERSATION_HISTORY = 10

# Show logs in the terminal while the assistant is running.
ENABLE_CONSOLE_LOGS = True

# Wait time (in seconds) before listening again.
# Helps prevent the assistant from hearing its own voice.
LISTENING_DELAY = 1