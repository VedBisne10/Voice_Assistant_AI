"""
orchestrator.py

Main controller of Nova.
Connects all assistant components together.
"""

import time
from assistant.transcriber import Transcriber
from assistant.speaker import Speaker
from assistant.listener import Listener

from ai.llm_client import LLMClient
from ai.memory_manager import MemoryManager

from utils.logger import logger

from config.constants import SYSTEM_PROMPT


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
            return None

        # Extract important memory from user input
        extracted_memory = self.llm.extract_memory(user_text)

        # Store extracted memory
        for key, value in extracted_memory.items():
            self.memory.remember(key, value)

        # Small delay to avoid hitting API rate limits back-to-back
        time.sleep(1)

        # Get AI response
        messages = self.build_messages(user_text)
        ai_response = self.llm.get_response(messages)

        # To avoid duplication of message
        self.memory.add_message("user", user_text)
        self.memory.add_message("assistant", ai_response)

        # Speak response
        self.speaker.speak(ai_response)

        return user_text    
    
    def build_messages(self, user_text):
        """
        Build complete message context for LLM.
        """

        messages = []

        # System prompt
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
            })

        # Long-term memory
        if self.memory.memory:
            memory_text = f"Known user facts: {self.memory.memory}"

            messages.append({
                "role": "system",
                "content": memory_text
                })

        # Conversation history
        messages.extend(self.memory.get_history())

        # Current message
        messages.append({
            "role": "user",
            "content": user_text
            })

        return messages

    def run_forever(self):
        """
        Keep assistant running until user ends conversation.
        """

        logger.info("Starting continuous conversation mode")

        EXIT_COMMANDS = [
            "end conversation",
            "stop conversation",
            "goodbye nova",
            "exit"
        ]

        while True:
            user_text = self.run_once()

            if not user_text:
                continue

            if user_text.lower() in EXIT_COMMANDS:
                self.speaker.speak("Ending conversation. Goodbye.")
                logger.info("Conversation ended")
                break

   
