"""
orchestrator.py

Main controller of Nova.
Connects all assistant components together.
"""

# Import all the main components of the assistant
from assistant.listener import Listener         # Records audio from microphone
from assistant.transcriber import Transcriber   # Converts audio to text
from assistant.speaker import Speaker           # Speaks text out loud

from ai.local_llm_client import LocalLLMClient        # Sends messages to the AI model and gets responses
from ai.memory_manager import MemoryManager  # Manages short-term and long-term memory

from utils.logger import logger              # Custom logger for info/warning messages

from config.constants import SYSTEM_PROMPT   # The base instructions that define Nova's personality and behavior


class Orchestrator:
    """
    Controls Nova's full workflow.
    """

    def __init__(self):
        """
        Initialize all assistant components.
        """

        logger.info("Initializing Nova...")

        # Set up each component — order doesn't matter here, just initialization
        self.listener = Listener()       # Microphone recorder
        self.transcriber = Transcriber() # Speech-to-text engine
        self.speaker = Speaker()         # Text-to-speech engine
        self.llm = LocalLLMClient()      # AI language model client
        self.memory = MemoryManager()    # Memory and conversation history handler

        logger.info("Nova initialized successfully")

    def run_once(self):
        """
        Execute one complete assistant cycle:
        listen → transcribe → extract memory → get AI response → speak
        """

        # Step 1: Record the user's voice and save it as a WAV file
        audio_file = self.listener.listen()

        # Step 2: Convert the recorded audio file into a text string
        user_text = self.transcriber.transcribe(audio_file)

        # Step 3: If no speech was detected (empty string), skip this cycle
        if not user_text:
            logger.warning("No speech detected")
            return None

        # # Step 4: Ask the AI to pull out any important facts from what the user said
        # # e.g., name, preferences, goals — things worth remembering long-term
        # extracted_memory = self.llm.extract_memory(user_text)

        # # Step 5: Save each extracted fact into long-term memory
        # # key = fact category (e.g., "name"), value = the actual info (e.g., "Alex")
        # for key, value in extracted_memory.items():
        #     self.memory.remember(key, value)

        # Step 6: Build the full message list to send to the AI
        # Includes system prompt, memory facts, chat history, and the new user message
        messages = self.build_messages(user_text)

        # Step 7: Send the messages to the AI and get its text response
        ai_response = self.llm.get_response(messages)

        # Step 8: Save both the user's message and AI's response to conversation history
        # Done after getting the response to avoid the current message being included twice
        self.memory.add_message("user", user_text)
        self.memory.add_message("assistant", ai_response)

        # Step 9: Speak the AI's response out loud
        self.speaker.speak(ai_response)

        # Return the user's text so run_forever() can check for exit commands
        return user_text

    def build_messages(self, user_text):
        """
        Build the complete message list to send to the LLM.
        The LLM needs the full context — not just the latest message.
        """

        # Start with an empty list — we'll build it up in order
        messages = []

        # Add the system prompt first — this tells the AI who it is and how to behave
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })

        # If there are any saved memory facts, inject them as a system message
        # This lets the AI "know" things about the user across conversations
        if self.memory.memory:
            memory_text = f"Known user facts: {self.memory.memory}"

            messages.append({
                "role": "system",
                "content": memory_text
            })

        # Add the full conversation history (previous user + assistant messages)
        # This gives the AI context so it doesn't forget what was said earlier
        history = self.memory.get_history()
        
        messages.extend(history[-6:])

        # Add the current user message at the end — this is what the AI responds to
        messages.append({
            "role": "user",
            "content": user_text
        })

        return messages

    def run_forever(self):
        """
        Keep the assistant running in a loop until the user says a goodbye command.
        """

        logger.info("Starting continuous conversation mode")

        # List of phrases that will end the conversation when spoken
        EXIT_COMMANDS = [
            "end conversation",
            "stop conversation",
            "goodbye nova",
            "exit"
        ]

        # Keep looping — each iteration is one full listen → respond cycle
        while True:
            user_text = self.run_once()

            # If run_once returned None (no speech), just try listening again
            if not user_text:
                continue

            # If the user said a goodbye phrase, say farewell and stop the loop
            if user_text.lower() in EXIT_COMMANDS:
                self.speaker.speak("Ending conversation. Goodbye.")
                logger.info("Conversation ended")
                break
