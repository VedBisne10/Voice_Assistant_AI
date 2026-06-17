"""
llm_client.py

Handles all communication with the OpenRouter API.
Sends conversation messages to the AI model and returns its response.
Also handles extracting long-term memory facts from user messages.
"""

import os        # Used to read the API key from environment variables
import requests  # Used to send HTTP requests to the OpenRouter API
import json      # Used to parse the AI's JSON-formatted memory extraction output
from dotenv import load_dotenv   # Loads variables from the .env file into the environment

from config.settings import MODEL_NAME   # The AI model name to use (defined in settings)
from utils.logger import logger          # Shared logger for recording info/errors


# Read the .env file and load its values into environment variables
# Must be called before os.getenv() so the API key is available
load_dotenv()


class LLMClient:
    """
    Handles all LLM communication.
    """

    def __init__(self):
        """
        Set up API credentials and endpoint URL.
        """

        # Read the OpenRouter API key from the .env file
        # os.getenv() returns None if the key doesn't exist
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        # The OpenRouter API endpoint that accepts chat completion requests
        # This follows the same format as OpenAI's API
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

        # If no API key is found, crash early with a clear message
        # Better to fail here than get a confusing error later during a request
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")

        logger.info("LLM Client initialized successfully")

    def get_response(self, messages):
        """
        Send the full conversation context to the AI and return its reply.

        Args:
            messages (list): List of message dicts with 'role' and 'content'
                             e.g. [{"role": "user", "content": "Hello"}]

        Returns:
            str: The AI's text response
        """

        logger.info("Sending prompt to LLM")

        # HTTP headers required by OpenRouter
        # Authorization uses Bearer token format — the API key proves our identity
        # Content-Type tells the server we're sending JSON data
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # The request body — specifies which model to use and the full message history
        payload = {
            "model": MODEL_NAME,    # Which AI model should process this request
            "messages": messages    # The full conversation context (system + history + current message)
        }

        # Send a POST request to the OpenRouter API with our payload
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload    # requests automatically serializes the dict to JSON
        )

        # Parse the API's JSON response body into a Python dictionary
        response_data = response.json()

        # Check if the response contains 'choices' before accessing it
        # If 'choices' is missing, it means the API returned an error (rate limit, bad key, etc.)
        # Checking first prevents a confusing KeyError crash
        if "choices" not in response_data:
            raise Exception(f"OpenRouter Error: {response_data}")

        # Extract the AI's reply text from the response structure
        # response_data["choices"] is a list — [0] gets the first (and usually only) result
        # ["message"]["content"] is where the actual text lives
        ai_response = response_data["choices"][0]["message"]["content"]

        logger.info(f"LLM Response: {ai_response}")

        return ai_response

    def extract_memory(self, user_text):
        """
        Ask the AI to pull out any important long-term facts from the user's message.
        Returns a dict of facts (e.g. {"name": "Alex", "profession": "engineer"})
        or an empty dict if nothing notable was said.

        Args:
            user_text (str): The raw message the user just said

        Returns:
            dict: Extracted facts, or {} if none found or on error
        """

        logger.info("Extracting memory from user input")

        # This is a special prompt that instructs the AI to act as a fact extractor
        # We tell it exactly what to look for and demand pure JSON output
        # {{}} is an escaped {} — needed inside an f-string to produce a literal {}
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

        # Same auth headers as get_response()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Send the memory prompt as a standalone single-turn conversation
        # We don't include history here — this is an isolated extraction task
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": memory_prompt
                }
            ]
        }

        # Send the extraction request to the API
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload
        )

        # Parse the response JSON
        response_data = response.json()

        # Guard against API errors (rate limit, quota exceeded, etc.)
        # Return empty dict so the rest of the program continues uninterrupted
        if "choices" not in response_data:
            logger.error(f"OpenRouter Error during memory extraction: {response_data}")
            return {}

        # Get the AI's raw text output (should be a JSON string like {"name": "Alex"})
        memory_text = response_data["choices"][0]["message"]["content"]

        logger.info(f"Memory extraction output: {memory_text}")

        try:
            # Parse the AI's JSON string into a real Python dictionary
            extracted_memory = json.loads(memory_text)
            return extracted_memory

        except Exception:
            # If the AI returned something that isn't valid JSON, log and return empty
            # This can happen if the model adds extra text around the JSON
            logger.warning("Failed to parse extracted memory JSON")
            return {}
