"""
memory_manager.py - Handles Nova's memory.

Two types:
- Long-term: facts about the user that persist across sessions (memory.json)
- Short-term: the recent conversation history (conversation_history.json)
"""

from utils.file_helper import load_json, save_json
from utils.logger import logger
from config.constants import MEMORY_FILE, CONVERSATION_HISTORY_FILE
from config.settings import MAX_CONVERSATION_HISTORY


class MemoryManager:

    def __init__(self):
        # Load whatever was saved from last session
        self.memory = load_json(MEMORY_FILE)
        self.history = load_json(CONVERSATION_HISTORY_FILE)

        logger.info("Memory Manager initialized successfully")

    def save_memory(self):
        save_json(MEMORY_FILE, self.memory)

    def save_history(self):
        save_json(CONVERSATION_HISTORY_FILE, self.history)

    def remember(self, key, value):
        # Store a fact and immediately write to disk
        self.memory[key] = value
        self.save_memory()
        logger.info(f"Stored memory: {key} = {value}")

    def recall(self, key):
        # .get() returns None if the key doesn't exist, no crash
        value = self.memory.get(key)
        logger.info(f"Retrieved memory: {key} = {value}")
        return value

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

        # Keep only the most recent N messages so the history doesn't grow forever
        self.history = self.history[-MAX_CONVERSATION_HISTORY:]

        self.save_history()
        logger.info(f"Added message to history: {role}")

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.save_history()
        logger.info("Conversation history cleared")
