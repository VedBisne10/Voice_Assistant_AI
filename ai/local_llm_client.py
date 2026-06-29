"""
local_llm_client.py - Talks to the local Ollama instance.
No API keys, no internet — runs fully on your machine.
"""

import requests
import json
import re
from utils.logger import logger


def _strip_thinking(text: str) -> str:
    # Gemma3 puts its reasoning inside <think>...</think> before the actual answer.
    # We don't want Nova speaking that out loud, so strip it.
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned.strip()


class LocalLLMClient:

    def __init__(self):
        self.base_url = "http://localhost:11434/api/chat"
        self.model_name = "gemma3:12b"

        logger.info("Local LLM Client initialized successfully")

        # Quick check — if Ollama isn't running, fail early with a clear message
        try:
            requests.get("http://localhost:11434", timeout=3)
            logger.info("Ollama server is running")
        except Exception:
            logger.error("Ollama server is not running")
            raise Exception("Cannot connect to Ollama. Run: ollama serve")

    def get_response(self, messages):
        logger.info("Sending messages to local LLM")

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False  # Get the whole response at once, not token by token
        }

        response = requests.post(self.base_url, json=payload)
        response_data = response.json()

        if "message" not in response_data:
            raise Exception(f"Unexpected response from Ollama: {response_data}")

        ai_response = response_data["message"]["content"]

        # Clean up any <think> blocks before returning
        ai_response = _strip_thinking(ai_response)

        logger.info(f"LLM Response: {ai_response}")
        return ai_response

    def extract_memory(self, user_text):
        logger.info("Extracting memory from user input")

        # Separate focused prompt — just extract facts, don't chat
        memory_prompt = f"""
            Extract important long-term user facts from the message.

            Store only useful facts such as:
            - name, age, profession, goals, preferences, favorite things, ongoing projects

            Do NOT store temporary information.
            Return ONLY valid JSON. If nothing important, return {{}}

            Message: {user_text}
        """

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": memory_prompt}],
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response_data = response.json()
        memory_text = response_data["message"]["content"]

        logger.info(f"Memory extraction output: {memory_text}")

        try:
            return json.loads(memory_text)
        except Exception:
            logger.warning("Couldn't parse memory JSON — skipping")
            return {}
