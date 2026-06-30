"""
transcriber.py - Converts audio files to text using Faster Whisper.
"""

from faster_whisper import WhisperModel  # the actual transcription engine — faster than OpenAI's whisper package
from utils.logger import logger  # shared logger used across the project


class Transcriber:  # wraps the Whisper model so the orchestrator just calls transcribe() and gets a string

    def __init__(self, model_size="small"):  # "small" is the default — fast enough on CPU, accurate enough for everyday speech
        logger.info("Loading Faster Whisper model...")  # this takes a few seconds, good to log it

        # small is a good middle ground — accurate enough, not too slow on CPU
        # int8 cuts memory usage roughly in half with minimal quality loss
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")  # load the model on CPU with int8 quantization to save RAM

        logger.info(f"Whisper model '{model_size}' loaded successfully")  # confirm the model is in memory and ready

    def transcribe(self, audio_file):  # takes a WAV file path, returns the transcribed text as a string
        logger.info(f"Transcribing audio: {audio_file}")  # log which file we're working on

        # Whisper splits the audio into chunks (segments) and transcribes each one
        segments, info = self.model.transcribe(audio_file)  # run inference — segments is a generator, info has language details

        # Join all the segment texts into one string
        full_text = ""  # start with an empty string and build it up
        for segment in segments:  # iterate through each spoken chunk Whisper identified
            full_text += segment.text + " "  # append this chunk's text with a space separator

        full_text = full_text.strip()  # remove the trailing space we added in the loop

        logger.info(f"Detected language: {info.language}")  # log what language Whisper thinks was spoken
        logger.info(f"Transcription result: {full_text}")  # log the final text so we can see it in the console

        return full_text  # hand back the clean transcription string
