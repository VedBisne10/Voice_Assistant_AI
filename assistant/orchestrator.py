"""
orchestrator.py

Main controller of Nova.
Connects all assistant components together.
"""

from assistant.listener import Listener
from assistant.transcriber import Transcriber
from assistant.speaker import Speaker

from ai.llm_client import LLMClient
from ai.memory_manager import MemoryManager

from utils.logger import logger


class Orchestrator:
    """
    Controls Nova's full workflow.
    """

    def __init__(self):
        """
        Initialize all assistant components.
        """

        logger.info("Initializing Nova...")

        self.listener = Listener()
        self.transcriber = Transcriber()
        self.speaker = Speaker()
        self.llm = LLMClient()
        self.memory = MemoryManager()

        logger.info("Nova initialized successfully")

    def run_once(self):
        """
        Execute one complete assistant cycle.
        """

        # Record user speech
        audio_file = self.listener.listen()

        # Convert speech to text
        user_text = self.transcriber.transcribe(audio_file)

        # Stop if no speech detected
        if not user_text:
            logger.warning("No speech detected")
            return

        # Store user message in history
        self.memory.add_message("user", user_text)

        # Get AI response
        ai_response = self.llm.get_response(user_text)

        # Store assistant response in history
        self.memory.add_message("assistant", ai_response)

        # Speak response
        self.speaker.speak(ai_response)