"""
speaker.py - Turns text into speech using ElevenLabs.
Saves the audio to a temp file and plays it via Windows Media Foundation.
"""

import os
import tempfile
import subprocess
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from config.settings import ELEVENLABS_VOICE_ID
from utils.logger import logger

load_dotenv()


class Speaker:

    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")

        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in .env file")

        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = ELEVENLABS_VOICE_ID

        logger.info("Speech engine initialized successfully")

    def speak(self, text):
        logger.info(f"Nova says: {text}")

        try:
            # turbo_v2_5 is the fastest ElevenLabs model — good for real-time use
            audio = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_turbo_v2_5",
            )

            # Write the audio chunks to a temp MP3 file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                for chunk in audio:
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name

            # Play via PowerShell + Windows Media Foundation
            # 800ms sleep gives WMF time to buffer the file before playback starts
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

            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            os.remove(tmp_path)

        except Exception as e:
            logger.error(f"Speech engine error: {e}")
