"""
settings.py - All the knobs you'd want to tweak in one place.
Change things here instead of digging through the codebase.
"""

ASSISTANT_NAME = "Nova"

STARTUP_MESSAGE = f"Hello, {ASSISTANT_NAME} at your service Sir."

# Words per minute — 170 feels natural, go lower if she sounds rushed
SPEECH_RATE = 170

SPEECH_VOLUME = 1.0

# ElevenLabs voice — find IDs at elevenlabs.io/app/voice-lab
# "JBFqnCBsd6RMkjVDRZzb" is George, a clear deep male voice
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Ollama model — must be pulled first with: ollama pull <name>
MODEL_NAME = "gemma3:12b"

# How many past messages to send as context to the model
# More = better memory of the conversation, but slower responses
MAX_CONVERSATION_HISTORY = 10

# Toggle terminal logs on/off
ENABLE_CONSOLE_LOGS = True

# Pause before listening again — stops Nova from hearing her own voice
LISTENING_DELAY = 1
