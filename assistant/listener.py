"""
listener.py - Records audio from the mic and saves it as a WAV file.
"""

import sounddevice as sd
import soundfile as sf

from utils.logger import logger
from config.constants import TEMP_AUDIO_FILE


class Listener:

    def __init__(self, sample_rate=16000, channels=1, duration=5):
        # 16000 Hz is the standard for speech recognition
        self.sample_rate = sample_rate
        # Mono is fine for voice — stereo would just waste space
        self.channels = channels
        # How long to record each time the user speaks
        self.duration = duration

        logger.info("Listener initialized successfully")

    def listen(self):
        logger.info("Listening... Speak now.")

        # Record for `duration` seconds — total samples = duration × sample_rate
        audio = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"  # Whisper expects float32
        )

        # Block here until recording finishes before doing anything else
        sd.wait()

        # Write to disk so the transcriber can pick it up
        sf.write(TEMP_AUDIO_FILE, audio, self.sample_rate)
        logger.info(f"Audio saved to {TEMP_AUDIO_FILE}")

        return TEMP_AUDIO_FILE
