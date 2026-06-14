"""
llm_client.py

Handles communication with OpenRouter API.
Sends prompts to Nemotron model and returns AI responses.
"""

import os
import requests
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

    def get_response(self, prompt):
        """
        Send user prompt to LLM and return response.

        Args:
            prompt (str): User input text

        Returns:
            str: AI response
        """

        logger.info(f"Sending prompt to LLM: {prompt}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload
        )

        # Convert response into JSON
        response_data = response.json()

        # Extract AI response text
        ai_response = response_data["choices"][0]["message"]["content"]

        logger.info(f"LLM Response: {ai_response}")

        return ai_response