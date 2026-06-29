"""
transcriber.py - Converts audio files to text using Faster Whisper.
"""

from faster_whisper import WhisperModel
from utils.logger import logger


class Transcriber:

    def __init__(self, model_size="small"):
        logger.info("Loading Faster Whisper model...")

        # small is a good middle ground — accurate enough, not too slow on CPU
        # int8 cuts memory usage roughly in half with minimal quality loss
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

        logger.info(f"Whisper model '{model_size}' loaded successfully")

    def transcribe(self, audio_file):
        logger.info(f"Transcribing audio: {audio_file}")

        # Whisper splits the audio into chunks (segments) and transcribes each one
        segments, info = self.model.transcribe(audio_file)

        # Join all the segment texts into one string
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "

        full_text = full_text.strip()

        logger.info(f"Detected language: {info.language}")
        logger.info(f"Transcription result: {full_text}")

        return full_text
