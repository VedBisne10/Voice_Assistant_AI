"""
local_llm_client.py - Talks to the local Ollama instance.
No API keys, no internet — runs fully on your machine.
"""

import requests  # standard HTTP library — we use it to POST to Ollama's REST API
import json  # for parsing JSON when extracting memory facts
import re  # regex for stripping the <think> tags Gemma adds to its output
from utils.logger import logger  # shared logger for the whole project


def _strip_thinking(text: str) -> str:  # helper that removes Gemma's internal reasoning from the final reply
    # Gemma3 puts its reasoning inside <think>...</think> before the actual answer.
    # We don't want Nova speaking that out loud, so strip it.
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)  # regex replace — re.DOTALL lets . match newlines inside the tags
    return cleaned.strip()  # remove any leftover whitespace after the tags are gone


class LocalLLMClient:  # wraps all the Ollama API calls so the rest of the code just calls get_response()

    def __init__(self):  # constructor — sets the endpoint, model name, and verifies the server is up
        self.base_url = "http://localhost:11434/api/chat"  # Ollama's chat API endpoint — runs on port 11434 by default
        self.model_name = "gemma3:12b"  # the model we're using — must be pulled first with: ollama pull gemma3:12b

        logger.info("Local LLM Client initialized successfully")  # log that the config is set

        # Quick check — if Ollama isn't running, fail early with a clear message
        try:  # try to reach the Ollama root endpoint before any real work happens
            requests.get("http://localhost:11434", timeout=3)  # 3 second timeout — if it doesn't respond, the server isn't up
            logger.info("Ollama server is running")  # server responded, we're good
        except Exception:  # any connection error means Ollama isn't running
            logger.error("Ollama server is not running")  # log the problem
            raise Exception("Cannot connect to Ollama. Run: ollama serve")  # raise with a clear fix so the user knows exactly what to do

    def get_response(self, messages):  # send a list of messages to the model and return the reply as a string
        logger.info("Sending messages to local LLM")  # log every request so we can trace conversation flow

        payload = {  # build the request body Ollama expects
            "model": self.model_name,  # which model to use — must match what's been pulled
            "messages": messages,  # the full conversation context as a list of role/content dicts
            "stream": False  # Get the whole response at once, not token by token
        }

        response = requests.post(self.base_url, json=payload)  # POST to Ollama — blocks until the model finishes generating
        response_data = response.json()  # parse the JSON response body

        if "message" not in response_data:  # if Ollama returned something unexpected, surface it
            raise Exception(f"Unexpected response from Ollama: {response_data}")  # crash with useful info instead of a cryptic KeyError

        ai_response = response_data["message"]["content"]  # pull the actual text out of the nested response structure

        # Clean up any <think> blocks before returning
        ai_response = _strip_thinking(ai_response)  # remove internal reasoning so Nova doesn't speak it

        logger.info(f"LLM Response: {ai_response}")  # log the final reply for debugging
        return ai_response  # hand the clean string back to the orchestrator

    def extract_memory(self, user_text):  # separate LLM call just to pull out long-term facts from what the user said
        logger.info("Extracting memory from user input")  # log that we're doing a memory extraction pass

        # Separate focused prompt — just extract facts, don't chat
        memory_prompt = f"""
            Extract important long-term user facts from the message.

            Store only useful facts such as:
            - name, age, profession, goals, preferences, favorite things, ongoing projects

            Do NOT store temporary information.
            Return ONLY valid JSON. If nothing important, return {{}}

            Message: {user_text}
        """  # tightly scoped prompt — no personality, no tools, just extraction

        payload = {  # minimal payload for this focused call
            "model": self.model_name,  # same model
            "messages": [{"role": "user", "content": memory_prompt}],  # single-turn, no history needed
            "stream": False  # still want the full response at once
        }

        response = requests.post(self.base_url, json=payload)  # send the extraction request to Ollama
        response_data = response.json()  # parse the response
        memory_text = response_data["message"]["content"]  # grab the raw text — should be a JSON string

        logger.info(f"Memory extraction output: {memory_text}")  # log what the model returned before we parse it

        try:  # the model should return JSON but sometimes it doesn't — be defensive
            return json.loads(memory_text)  # parse the JSON string into a Python dict
        except Exception:  # invalid JSON — the model probably added extra text around it
            logger.warning("Couldn't parse memory JSON — skipping")  # log and move on, not a critical failure
            return {}  # return empty dict so the caller doesn't have to handle None
