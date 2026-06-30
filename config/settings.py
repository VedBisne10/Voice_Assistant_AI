"""
settings.py - All the knobs you'd want to tweak in one place.
Change things here instead of digging through the codebase.
"""

ASSISTANT_NAME = "Nova"  # the assistant's name — used in greetings and log messages

STARTUP_MESSAGE = f"Hello, {ASSISTANT_NAME} at your service Sir."  # spoken when Nova first starts up — uses the name above

# Words per minute — 170 feels natural, go lower if she sounds rushed
SPEECH_RATE = 170  # controls how fast pyttsx3 speaks — only relevant if you swap ElevenLabs for a local TTS engine

SPEECH_VOLUME = 1.0  # volume for pyttsx3 — 1.0 is max, 0.0 is silent — same caveat as SPEECH_RATE

# ElevenLabs voice — find IDs at elevenlabs.io/app/voice-lab
# "JBFqnCBsd6RMkjVDRZzb" is George, a clear deep male voice
ELEVENLABS_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # the specific voice clone or preset to use for all TTS output

# Ollama model — must be pulled first with: ollama pull <name>
MODEL_NAME = "gemma3:12b"  # the local model identifier — change this if you switch to a different Ollama model

# How many past messages to send as context to the model
# More = better memory of the conversation, but slower responses
MAX_CONVERSATION_HISTORY = 10  # cap on how many messages get stored — older ones get dropped when this is exceeded

# Toggle terminal logs on/off
ENABLE_CONSOLE_LOGS = True  # set to False to silence the logger in production if you don't want terminal output

# Pause before listening again — stops Nova from hearing her own voice
LISTENING_DELAY = 1  # seconds to wait after speaking before the mic turns on again — prevents feedback loops
