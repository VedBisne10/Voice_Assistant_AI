"""
memory_manager.py

Handles short-term and long-term memory for Nova.
Stores conversation history and important user facts.
"""

from utils.file_helper import load_json, save_json
from utils.logger import logger
from config.constants import MEMORY_FILE, CONVERSATION_HISTORY_FILE
from config.settings import MAX_CONVERSATION_HISTORY


class MemoryManager:
    """
    Handles assistant memory.
    """

    def __init__(self):
        """
        Load memory files during initialization.
        """

        # Load long-term memory
        self.memory = load_json(MEMORY_FILE)

        # Load conversation history
        self.history = load_json(CONVERSATION_HISTORY_FILE)

        logger.info("Memory Manager initialized successfully")

    def save_memory(self):
        """
        Save long-term memory to file.
        """
        save_json(MEMORY_FILE, self.memory)

    def save_history(self):
        """
        Save conversation history to file.
        """
        save_json(CONVERSATION_HISTORY_FILE, self.history)

    def remember(self, key, value):
        """
        Store a fact in long-term memory.

        Args:
            key (str): Memory key
            value (any): Memory value
        """

        self.memory[key] = value
        self.save_memory()

        logger.info(f"Stored memory: {key} = {value}")

    def recall(self, key):
        """
        Retrieve stored memory.

        Args:
            key (str): Memory key

        Returns:
            Stored value or None
        """

        value = self.memory.get(key)

        logger.info(f"Retrieved memory: {key} = {value}")

        return value

    def add_message(self, role, content):
        """
        Add a message to conversation history.

        Args:
            role (str): user / assistant
            content (str): message text
        """

        message = {
            "role": role,
            "content": content
        }

        self.history.append(message)

        # Keep only recent conversation history
        self.history = self.history[-MAX_CONVERSATION_HISTORY:]

        self.save_history()

        logger.info(f"Added message to history: {role}")

    def get_history(self):
        """
        Return conversation history.
        """

        return self.history

    def clear_history(self):
        """
        Clear conversation history.
        """

        self.history = []
        self.save_history()

        logger.info("Conversation history cleared")