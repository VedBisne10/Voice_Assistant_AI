"""
speaker.py - Turns text into speech using ElevenLabs.
Saves the audio to a temp file and plays it via Windows Media Foundation.
"""

import os  # used for reading env vars and deleting the temp audio file when done
import tempfile  # creates a one-off temp file so we don't pollute the project folder
import subprocess  # runs PowerShell to play the audio since there's no native Python WMF binding
from dotenv import load_dotenv  # reads the .env file and injects variables into os.environ
from elevenlabs import ElevenLabs  # official ElevenLabs Python SDK
from config.settings import ELEVENLABS_VOICE_ID  # the specific voice ID we want — configured in settings.py
from utils.logger import logger  # shared logger for the whole project

load_dotenv()  # load .env into the environment so os.getenv() can find ELEVENLABS_API_KEY


class Speaker:  # handles all text-to-speech: API call, file write, playback, cleanup

    def __init__(self):  # constructor — grabs the API key and sets up the ElevenLabs client
        api_key = os.getenv("ELEVENLABS_API_KEY")  # read the key from the environment — never hardcode this

        if not api_key:  # if the key is missing, fail loudly right at startup, not mid-conversation
            raise ValueError("ELEVENLABS_API_KEY not found in .env file")  # clear message so the fix is obvious

        self.client = ElevenLabs(api_key=api_key)  # create the authenticated ElevenLabs client
        self.voice_id = ELEVENLABS_VOICE_ID  # store the voice ID we'll use for every speak() call

        logger.info("Speech engine initialized successfully")  # confirm the TTS layer is ready

    def speak(self, text):  # convert a text string to audio and play it on the system speakers
        logger.info(f"Nova says: {text}")  # log what Nova is about to say — useful for debugging

        try:  # wrap everything so a TTS failure doesn't crash the assistant
            # turbo_v2_5 is the fastest ElevenLabs model — good for real-time use
            audio = self.client.text_to_speech.convert(  # call the ElevenLabs API
                voice_id=self.voice_id,  # use the configured voice
                text=text,  # the string we want spoken
                model_id="eleven_turbo_v2_5",  # fastest model — lower latency than standard
            )

            # Write the audio chunks to a temp MP3 file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:  # create a temp file that won't auto-delete on close
                for chunk in audio:  # ElevenLabs streams audio in chunks, iterate through all of them
                    tmp_file.write(chunk)  # write each chunk to the file
                tmp_path = tmp_file.name  # save the path so we can reference it outside the with block

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
            """  # full PowerShell script — opens the file, waits for it to buffer, plays it, then waits for it to finish

            subprocess.run(  # run the PowerShell script and wait for it to complete
                ["powershell", "-NoProfile", "-Command", ps_script],  # -NoProfile skips the user profile for faster launch
                check=True,  # raise an exception if PowerShell exits with a non-zero code
                stdout=subprocess.DEVNULL,  # swallow stdout so it doesn't pollute our console
                stderr=subprocess.DEVNULL  # swallow stderr too — errors get caught by our except block
            )

            os.remove(tmp_path)  # clean up the temp MP3 file now that playback is done

        except Exception as e:  # catch anything that goes wrong — network error, playback failure, etc.
            logger.error(f"Speech engine error: {e}")  # log the problem — don't crash the whole assistant over it
