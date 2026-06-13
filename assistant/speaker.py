"""
speaker.py

Handles text-to-speech for the voice assistant.
Converts text responses into spoken audio.
"""

import pyttsx3

from config.settings import SPEECH_RATE, SPEECH_VOLUME
from utils.logger import logger


class Speaker:
    """
    Handles all speaking operations of Nova.
    """

    def __init__(self):
        """
        Initialize speech engine and apply settings.
        """

        # Create pyttsx3 speech engine
        self.engine = pyttsx3.init()

        # Set speaking speed
        self.engine.setProperty("rate", SPEECH_RATE)

        # Set volume (0.0 to 1.0)
        self.engine.setProperty("volume", SPEECH_VOLUME)

        logger.info("Speech engine initialized successfully")

    def speak(self, text):
        """
        Speak the given text.

        Args:
            text (str): Text to speak
        """

        # Log what assistant is about to say
        logger.info(f"Nova says: {text}")

        # Add text to speech queue
        self.engine.say(text)

        # Speak queued text and wait until completed
        self.engine.runAndWait()