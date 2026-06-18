"""
local_llm_client.py

Handles communication with local Ollama model.
"""

import requests
import json

from utils.logger import logger


class LocalLLMClient:
    """
    Handles communication with local LLM.
    """

    def __init__(self):
        """
        Initialize local LLM settings.
        """

        self.base_url = "http://localhost:11434/api/chat"
        self.model_name = "qwen3.5:9b"

        logger.info("Local LLM Client initialized successfully")

        try:
            response = requests.get("http://localhost:11434", timeout=3)
            logger.info("Ollama server is running")

        except Exception:
            logger.error("Ollama server is not running")
            raise Exception("Cannot connect to Ollama")

    
    def get_response(self, messages):
        """
        Send messages to local LLM.
        """

        logger.info("Sending messages to local LLM")

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(
            self.base_url, 
            json=payload
        )

        response_data = response.json()

        logger.info(f"Raw Ollama response: {response_data}")

        ai_response = response_data["message"]["content"]

        logger.info(f"LLM Response: {ai_response}")
        
        return ai_response


    def extract_memory(self, user_text):
        logger.info("Extracting memory from user input")

        memory_prompt = f"""
            Extract important long-term user facts from the message.

            Store only useful facts such as:
            - name
            - age
            - profession
            - goals
            - preferences
            - favorite things
            - ongoing projects

            Do NOT store temporary information.

            Return ONLY valid JSON.
            If nothing important exists, return {{}}

            Message:
            {user_text}
        """

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": memory_prompt
                }
            ],
            "stream": False
        }

        response = requests.post(
            self.base_url,
            json=payload
        )

        response_data = response.json()
        memory_text = response_data["message"]["content"]

        logger.info(f"Memory extraction output: {memory_text}")
        
        try:
            extracted_memory = json.loads(memory_text)
            return extracted_memory

        except Exception:
            logger.warning("Failed to parse extracted memory JSON")
            return {}


    



