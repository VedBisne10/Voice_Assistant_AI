"""
memory_manager.py

Handles short-term and long-term memory for Nova.

- Long-term memory: persistent facts about the user (name, preferences, etc.)
  Stored in memory.json — survives across sessions.

- Short-term memory: the current conversation history (recent messages)
  Stored in conversation_history.json — trimmed to a max length.
"""

from utils.file_helper import load_json, save_json   # Helper functions to read/write JSON files
from utils.logger import logger                       # Shared logger for info/warning messages
from config.constants import MEMORY_FILE, CONVERSATION_HISTORY_FILE   # File paths for both storage files
from config.settings import MAX_CONVERSATION_HISTORY  # Max number of messages to keep in history


class MemoryManager:
    """
    Manages Nova's memory — both persistent facts and conversation history.
    """

    def __init__(self):
        """
        Load both memory stores from disk when Nova starts up.
        """

        # Load long-term memory from memory.json into a dict
        # e.g. {"name": "Alex", "profession": "engineer"}
        self.memory = load_json(MEMORY_FILE)

        # Load conversation history from conversation_history.json into a list
        # e.g. [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]
        self.history = load_json(CONVERSATION_HISTORY_FILE)

        logger.info("Memory Manager initialized successfully")

    def save_memory(self):
        """
        Write the current long-term memory dict to memory.json on disk.
        Called automatically whenever a new fact is stored.
        """
        save_json(MEMORY_FILE, self.memory)

    def save_history(self):
        """
        Write the current conversation history list to conversation_history.json on disk.
        Called automatically whenever a message is added or cleared.
        """
        save_json(CONVERSATION_HISTORY_FILE, self.history)

    def remember(self, key, value):
        """
        Store a single fact in long-term memory and save it to disk.

        Args:
            key (str): The category of the fact e.g. "name", "favorite things"
            value (any): The actual value to store e.g. "Alex", ["jazz", "hiking"]
        """

        # Add or overwrite the fact in the in-memory dict
        self.memory[key] = value

        # Immediately persist to disk so nothing is lost if the app closes
        self.save_memory()

        logger.info(f"Stored memory: {key} = {value}")

    def recall(self, key):
        """
        Look up a specific fact from long-term memory.

        Args:
            key (str): The fact to look up e.g. "name"

        Returns:
            The stored value, or None if the key doesn't exist
        """

        # .get() returns None instead of raising a KeyError if the key is missing
        value = self.memory.get(key)

        logger.info(f"Retrieved memory: {key} = {value}")

        return value

    def add_message(self, role, content):
        """
        Append a new message to the conversation history and save it.
        Automatically trims history to the max allowed length.

        Args:
            role (str): Who sent the message — "user" or "assistant"
            content (str): The text of the message
        """

        # Build the message dict in the format the LLM API expects
        message = {
            "role": role,       # "user" or "assistant"
            "content": content  # The actual message text
        }

        # Add the new message to the end of the history list
        self.history.append(message)

        # Trim the history to only keep the most recent N messages
        # Negative slicing: [-10:] keeps the last 10 items and discards older ones
        # This prevents the context sent to the AI from growing infinitely
        self.history = self.history[-MAX_CONVERSATION_HISTORY:]

        # Persist the updated history to disk
        self.save_history()

        logger.info(f"Added message to history: {role}")

    def get_history(self):
        """
        Return the full conversation history list.
        Used by the orchestrator to build the message context for the LLM.
        """

        return self.history

    def clear_history(self):
        """
        Wipe the conversation history completely and save the empty state.
        Useful for starting a fresh conversation without restarting the app.
        """

        # Reset to an empty list
        self.history = []

        # Save the empty list to disk so the cleared state persists
        self.save_history()

        logger.info("Conversation history cleared")
