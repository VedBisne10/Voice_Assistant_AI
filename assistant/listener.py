"""
listener.py

Handles microphone input for the voice assistant.
Records audio and saves it as a WAV file.
"""

import sounddevice as sd   # Library to record audio from the microphone
import soundfile as sf      # Library to save audio data as a WAV file

from utils.logger import logger                 # Custom logger for info/warning messages
from config.constants import TEMP_AUDIO_FILE    # Path where the recorded audio will be saved


class Listener:
    """
    Handles audio recording from microphone.
    """

    def __init__(self, sample_rate=16000, channels=1, duration=5):
        """
        Initialize recording settings.
        """

        # How many audio samples to capture per second (16000 is standard for speech)
        self.sample_rate = sample_rate

        # Number of audio channels — 1 means mono (single mic input)
        self.channels = channels

        # How many seconds to record when listen() is called
        self.duration = duration

        logger.info("Listener initialized successfully")

    def listen(self):
        """
        Record audio and save as WAV file.

        Returns:
            Path: Path of saved audio file
        """

        logger.info("Listening... Speak now.")

        # Start recording audio from the microphone
        # int(duration * sample_rate) = total number of samples to capture
        audio = sd.rec(
            int(self.duration * self.sample_rate),  # Total samples = duration × rate
            samplerate=self.sample_rate,             # Capture at 16000 samples/sec
            channels=self.channels,                  # Mono recording
            dtype="float32"                          # Audio format — float32 is compatible with Whisper
        )

        # Wait (block) until the recording is fully finished before moving on
        sd.wait()

        # Save the recorded audio data to a WAV file on disk
        sf.write(TEMP_AUDIO_FILE, audio, self.sample_rate)

        logger.info(f"Audio saved to {TEMP_AUDIO_FILE}")

        # Return the file path so the next step (transcription) knows where to find it
        return TEMP_AUDIO_FILE
