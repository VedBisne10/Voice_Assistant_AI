"""
memory_manager.py - Handles Nova's memory.

Two types:
- Long-term: facts about the user that persist across sessions (memory.json)
- Short-term: the recent conversation history (conversation_history.json)
"""

from utils.file_helper import load_json, save_json  # all file I/O goes through here — no raw open() calls scattered around
from utils.logger import logger  # shared logger for the project
from config.constants import MEMORY_FILE, CONVERSATION_HISTORY_FILE  # the two file paths this class manages
from config.settings import MAX_CONVERSATION_HISTORY  # max number of messages to keep in the history list


class MemoryManager:  # owns both memory stores and exposes clean methods to read and write them

    def __init__(self):  # load whatever was saved from the last session so we pick up where we left off
        # Load whatever was saved from last session
        self.memory = load_json(MEMORY_FILE)  # long-term facts — things like name, preferences, ongoing projects
        self.history = load_json(CONVERSATION_HISTORY_FILE)  # recent conversation turns as role/content dicts

        logger.info("Memory Manager initialized successfully")  # both files loaded, ready to go

    def save_memory(self):  # write the current memory dict to disk immediately
        save_json(MEMORY_FILE, self.memory)  # persist so nothing is lost if the program exits

    def save_history(self):  # write the current conversation history list to disk immediately
        save_json(CONVERSATION_HISTORY_FILE, self.history)  # keep the file in sync with the in-memory list

    def remember(self, key, value):  # store a single fact and immediately flush it to disk
        # Store a fact and immediately write to disk
        self.memory[key] = value  # add or overwrite the fact in the in-memory dict
        self.save_memory()  # write to disk right away so it survives a crash
        logger.info(f"Stored memory: {key} = {value}")  # log every stored fact so we can trace what's being remembered

    def recall(self, key):  # retrieve a single fact by key — returns None if it doesn't exist
        # .get() returns None if the key doesn't exist, no crash
        value = self.memory.get(key)  # safe lookup — won't throw a KeyError if the key is missing
        logger.info(f"Retrieved memory: {key} = {value}")  # log the retrieval so we can see what was looked up
        return value  # hand back the value, or None if we don't know this fact yet

    def add_message(self, role, content):  # append one message to the history and trim if it gets too long
        self.history.append({"role": role, "content": content})  # add the new message dict to the end of the list

        # Keep only the most recent N messages so the history doesn't grow forever
        self.history = self.history[-MAX_CONVERSATION_HISTORY:]  # slice from the end — oldest messages get dropped first

        self.save_history()  # write to disk immediately after every message
        logger.info(f"Added message to history: {role}")  # log which role spoke — "user" or "assistant"

    def get_history(self):  # return the full current history list for building the LLM prompt
        return self.history  # caller gets the raw list — they can slice it if they want fewer messages

    def clear_history(self):  # wipe the conversation history — useful for starting fresh
        self.history = []  # reset the in-memory list to empty
        self.save_history()  # push the empty list to disk immediately
        logger.info("Conversation history cleared")  # log that the reset happened
