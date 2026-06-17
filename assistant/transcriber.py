"""
transcriber.py

Handles speech-to-text conversion using Faster Whisper.
Converts recorded audio into text.
"""

from faster_whisper import WhisperModel   # Faster Whisper — an optimized version of OpenAI's Whisper model

from utils.logger import logger           # Custom logger for info/warning messages


class Transcriber:
    """
    Handles audio transcription using Faster Whisper.
    """

    def __init__(self, model_size="small"):
        """
        Load Whisper model.

        Args:
            model_size (str): Whisper model size (tiny / base / small / medium / large)
        """

        logger.info("Loading Faster Whisper model...")

        # Load the Whisper model into memory
        # model_size controls accuracy vs speed — "small" is a good balance
        # device="cpu" means run on CPU, not GPU
        # compute_type="int8" uses less memory by compressing the model weights
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

        # Run the audio through the Whisper model
        # segments = list of transcribed chunks (each chunk has text + timestamps)
        # info = metadata like detected language and duration
        segments, info = self.model.transcribe(audio_file)

        # Start with an empty string to build the full transcription
        full_text = ""

        # Loop through each segment and join the text together
        # Whisper splits long audio into segments — we combine them into one string
        for segment in segments:
            full_text += segment.text + " "   # Add a space between segments

        # Remove any leading/trailing whitespace from the final string
        full_text = full_text.strip()

        # Log the language Whisper detected (e.g., "en" for English)
        logger.info(f"Detected language: {info.language}")

        # Log the full transcribed text
        logger.info(f"Transcription result: {full_text}")

        return full_text
