"""
speaker.py

Handles text-to-speech for the voice assistant.
Converts text responses into spoken audio.
"""

import pyttsx3   # Offline text-to-speech library — works without internet

from config.settings import SPEECH_RATE, SPEECH_VOLUME   # Speed and volume settings from config
from utils.logger import logger                           # Custom logger for info/warning messages


class Speaker:
    """
    Handles all speaking operations of Nova.
    """

    def __init__(self):
        """
        Initialize speech engine and apply settings.
        """

        # Create the pyttsx3 speech engine instance
        # This sets up the underlying TTS engine (e.g., SAPI5 on Windows)
        self.engine = pyttsx3.init()

        # Set how fast Nova speaks — higher number = faster speech
        self.engine.setProperty("rate", SPEECH_RATE)

        # Set the volume — range is 0.0 (silent) to 1.0 (full volume)
        self.engine.setProperty("volume", SPEECH_VOLUME)

        logger.info("Speech engine initialized successfully")

    def speak(self, text):
        """
        Speak the given text aloud.

        Args:
            text (str): Text to speak
        """

        # Log what Nova is about to say (useful for debugging)
        logger.info(f"Nova says: {text}")

        # Queue the text to be spoken — does not speak immediately
        self.engine.say(text)

        # Process the speech queue and block until all speech is done
        # Without this, the program would move on before Nova finishes speaking
        self.engine.runAndWait()
