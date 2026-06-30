"""
listener.py - Records audio from the mic and saves it as a WAV file.
"""

import sounddevice as sd  # cross-platform audio I/O — handles the mic recording
import soundfile as sf  # reads and writes audio files — we use it to save the WAV

from utils.logger import logger  # shared logger so we can see what's happening in the console
from config.constants import TEMP_AUDIO_FILE  # the single file path we reuse every recording


class Listener:  # wraps all the mic recording logic in one reusable object

    def __init__(self, sample_rate=16000, channels=1, duration=5):  # sensible defaults that work out of the box for speech
        # 16000 Hz is the standard for speech recognition
        self.sample_rate = sample_rate  # store sample rate — Whisper expects exactly 16 kHz input
        # Mono is fine for voice — stereo would just waste space
        self.channels = channels  # 1 channel, single mic, no need for stereo
        # How long to record each time the user speaks
        self.duration = duration  # seconds to record per turn — increase if users get cut off

        logger.info("Listener initialized successfully")  # confirm the mic layer is ready

    def listen(self):  # record one chunk of audio and return the path to the saved file
        logger.info("Listening... Speak now.")  # let the console show when recording starts

        # Record for `duration` seconds — total samples = duration × sample_rate
        audio = sd.rec(  # kick off a non-blocking recording
            int(self.duration * self.sample_rate),  # total number of samples to capture
            samplerate=self.sample_rate,  # match the rate Whisper expects
            channels=self.channels,  # mono recording
            dtype="float32"  # Whisper expects float32 — not int16 or anything else
        )

        # Block here until recording finishes before doing anything else
        sd.wait()  # holds execution until the full duration has been captured

        # Write to disk so the transcriber can pick it up
        sf.write(TEMP_AUDIO_FILE, audio, self.sample_rate)  # save to the shared temp path as a WAV
        logger.info(f"Audio saved to {TEMP_AUDIO_FILE}")  # confirm the file was written

        return TEMP_AUDIO_FILE  # hand back the path so the transcriber knows where to look
