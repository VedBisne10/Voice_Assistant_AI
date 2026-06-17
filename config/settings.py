"""
settings.py

Stores all configurable settings for the Voice Assistant.
If you want to tweak Nova's behavior, change values here
instead of hunting through multiple files.
"""

# The display name of the assistant — used in greetings and logs
ASSISTANT_NAME = "Nova"

# The first thing Nova says when she starts up
# Uses an f-string to include the assistant's name dynamically
STARTUP_MESSAGE = (
    f"Hello, {ASSISTANT_NAME} at your service Sir. "
)

# How fast Nova speaks — measured in words per minute
# 180 is natural conversational speed; lower = slower, higher = faster
SPEECH_RATE = 180

# How loud Nova speaks — range is 0.0 (silent) to 1.0 (maximum volume)
SPEECH_VOLUME = 1.0

# The AI model Nova uses to understand and respond to messages
# This is an OpenRouter model ID — change this to switch to a different model
# ":free" at the end means this is the free-tier version of the model
MODEL_NAME = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

# How many past messages to include when sending context to the AI
# Keeping this smaller saves tokens; keeping it larger gives the AI more memory of the chat
# e.g., 10 means the last 10 messages (5 user + 5 assistant turns)
MAX_CONVERSATION_HISTORY = 10

# Whether to print log messages in the terminal while Nova is running
# Set to False to silence terminal output (logs will still be written to file)
ENABLE_CONSOLE_LOGS = True

# How many seconds to wait before Nova starts listening again after speaking
# Prevents Nova from picking up her own voice as the next user input
LISTENING_DELAY = 1
