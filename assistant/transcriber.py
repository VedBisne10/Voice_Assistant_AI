"""
transcriber.py

Handles speech-to-text conversion using Faster Whisper.
Converts recorded audio into text.
"""

from faster_whisper import WhisperModel

from utils.logger import logger


class Transcriber:
    """
    Handles audio transcription using Faster Whisper.
    """

    def __init__(self, model_size="small"):
        """
        Load Whisper model.

        Args:
            model_size (str): Whisper model size
        """

        logger.info("Loading Faster Whisper model...")

        # Load whisper model
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

        logger.info(f"Whisper model '{model_size}' loaded successfully")

    def transcribe(self, audio_file):
        """
        Convert audio file into text.

        Args:
            audio_file: Path to audio file

        Returns:
            str: Transcribed text
        """

        logger.info(f"Transcribing audio: {audio_file}")

        # Transcribe audio
        segments, info = self.model.transcribe(audio_file)

        # Collect all segment text
        full_text = ""

        for segment in segments:
            full_text += segment.text + " "

        # Remove extra spaces
        full_text = full_text.strip()

        logger.info(f"Detected language: {info.language}")
        logger.info(f"Transcription result: {full_text}")

        return full_text