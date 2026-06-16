"""
llm_client.py

Handles communication with OpenRouter API.
Sends prompts to Nemotron model and returns AI responses.
"""

import os
import requests
import json
from dotenv import load_dotenv

from config.settings import MODEL_NAME
from utils.logger import logger


# Load environment variables from .env file
load_dotenv()


class LLMClient:
    """
    Handles all LLM communication.
    """

    def __init__(self):
        """
        Initialize API configuration.
        """

        # Read API key from .env
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        # OpenRouter endpoint
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")

        logger.info("LLM Client initialized successfully")

    def get_response(self, messages):
        """
        Send user prompt to LLM and return response.

        Args:
            messages (list): Full LLM conversation context

        Returns:
            str: AI response
        """

        logger.info(f"Sending prompt to LLM")
 
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": messages
            }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload
            )

        response_data = response.json()

        ai_response = response_data["choices"][0]["message"]["content"]

        if "choices" not in response_data:
            raise Exception(f"OpenRouter Error: {response_data}")

        logger.info(f"LLM Response: {ai_response}")

        return ai_response

    def extract_memory(self, user_text):
        """
        Extract important user information for long-term memory.

        Args:
            user_text (str): User message

        Returns:
            dict: Extracted memory
        """

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

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": memory_prompt
                }
            ]
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload
        )

        response_data = response.json()

        memory_text = response_data["choices"][0]["message"]["content"]

        logger.info(f"Memory extraction output: {memory_text}")

        try:
            extracted_memory = json.loads(memory_text)
            return extracted_memory
        
        except Exception:
            logger.warning("Failed to parse extracted memory JSON")
            return {}
    
        