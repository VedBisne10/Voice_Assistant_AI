"""
speaker.py

Handles text-to-speech for the voice assistant.
Uses ElevenLabs API for high-quality neural speech synthesis.
Audio is played using Windows Media Foundation via PowerShell —
no extra dependencies or build tools required.
"""

import os           # Reads the API key from environment variables
import tempfile     # Creates a temporary MP3 file for audio output
import subprocess   # Runs PowerShell to play MP3 via Windows Media Foundation
from dotenv import load_dotenv                        # Loads .env variables into environment
from elevenlabs import ElevenLabs                     # Official ElevenLabs Python SDK
from config.settings import ELEVENLABS_VOICE_ID       # Voice ID defined in settings
from utils.logger import logger                       # Shared logger for info/error messages


# Load the API key from .env file
load_dotenv()


class Speaker:
    """
    Handles all speaking operations of Nova using ElevenLabs TTS.
    """

    def __init__(self):
        """
        Initialize the ElevenLabs client with the API key from .env
        """

        # Read the ElevenLabs API key from the .env file
        api_key = os.getenv("ELEVENLABS_API_KEY")

        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in .env file")

        # Create the ElevenLabs client — all TTS calls go through this
        self.client = ElevenLabs(api_key=api_key)

        # The voice ID Nova will speak with
        self.voice_id = ELEVENLABS_VOICE_ID

        logger.info("Speech engine initialized successfully")

    def speak(self, text):
        """
        Convert text to speech using ElevenLabs and play it aloud.

        Generates MP3 audio via ElevenLabs API, saves it to a temp file,
        plays it using Windows Media Foundation (built into Windows),
        then deletes the temp file.

        Args:
            text (str): Text to speak
        """

        logger.info(f"Nova says: {text}")

        try:
            # Call ElevenLabs API to convert text to speech
            # Returns a generator of audio bytes in MP3 format
            audio = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_turbo_v2_5",   # Fastest model — lowest latency, still high quality
            )

            # Save the MP3 audio bytes to a temporary file
            # delete=False so the file persists until we explicitly remove it after playback
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                for chunk in audio:
                    tmp_file.write(chunk)   # Write each chunk from the generator
                tmp_path = tmp_file.name

            # Play the MP3 using PowerShell + Windows Media Foundation
            # WMF is built into every Windows machine — handles MP3 natively
            # Start-Sleep 500ms gives WMF time to buffer before Play() is called
            # We then wait for the full NaturalDuration before closing
            ps_script = f"""
                Add-Type -AssemblyName presentationCore
                $player = New-Object System.Windows.Media.MediaPlayer
                $player.Open([System.Uri]"{tmp_path}")
                Start-Sleep -Milliseconds 800
                $player.Play()
                $duration = $player.NaturalDuration.TimeSpan.TotalSeconds
                Start-Sleep -Seconds ($duration + 0.5)
                $player.Close()
            """

            # Run PowerShell synchronously — blocks until audio finishes playing
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                check=True,
                stdout=subprocess.DEVNULL,   # Suppress PowerShell output in terminal
                stderr=subprocess.DEVNULL    # Suppress PowerShell errors in terminal
            )

            # Delete the temp file after playback is done
            os.remove(tmp_path)

        except Exception as e:
            logger.error(f"Speech engine error: {e}")
