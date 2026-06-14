"""
listener.py

Handles microphone input for the voice assistant.
Records audio and saves it as a WAV file.
"""

import sounddevice as sd
import soundfile as sf

from utils.logger import logger
from config.constants import TEMP_AUDIO_FILE


class Listener:
    """
    Handles audio recording from microphone.
    """

    def __init__(self, sample_rate=16000, channels=1, duration=5):
        """
        Initialize recording settings.
        """

        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration

        logger.info("Listener initialized successfully")

    def listen(self):
        """
        Record audio and save as WAV file.

        Returns:
            Path: Path of saved audio file
        """

        logger.info("Listening... Speak now.")

        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"
        )

        sd.wait()

        # Save recording as WAV file
        sf.write(TEMP_AUDIO_FILE, audio, self.sample_rate)

        logger.info(f"Audio saved to {TEMP_AUDIO_FILE}")

        return TEMP_AUDIO_FILE