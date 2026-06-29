"""
orchestrator.py - The main loop that ties everything together.
Listen → transcribe → think → act or talk → repeat.
"""

from assistant.listener import Listener
from assistant.transcriber import Transcriber
from assistant.speaker import Speaker

from ai.local_llm_client import LocalLLMClient
from ai.memory_manager import MemoryManager
from ai.tool_router import is_tool_call, parse_tool_call, execute_tool

from utils.logger import logger
from config.constants import SYSTEM_PROMPT


class Orchestrator:

    def __init__(self):
        logger.info("Initializing Nova...")

        self.listener = Listener()
        self.transcriber = Transcriber()
        self.speaker = Speaker()
        self.llm = LocalLLMClient()
        self.memory = MemoryManager()

        logger.info("Nova initialized successfully")

    def run_once(self):
        # Record what the user says and turn it into text
        audio_file = self.listener.listen()
        user_text = self.transcriber.transcribe(audio_file)

        if not user_text:
            logger.warning("No speech detected")
            return None

        # Build the full context — system prompt + memory + history + current message
        messages = self.build_messages(user_text)
        ai_response = self.llm.get_response(messages)

        # If the model returned a tool call JSON, run the action.
        # Otherwise it's just a normal reply — speak it directly.
        if is_tool_call(ai_response):
            logger.info("Tool call detected — executing")
            tool_call = parse_tool_call(ai_response)

            if tool_call:
                spoken_response = execute_tool(tool_call, llm_client=self.llm)
            else:
                logger.warning("Looked like a tool call but couldn't parse it")
                spoken_response = "I understood what you wanted but couldn't execute it."
        else:
            spoken_response = ai_response

        # Save to history after responding so the current exchange shows up next turn
        self.memory.add_message("user", user_text)
        self.memory.add_message("assistant", spoken_response)

        self.speaker.speak(spoken_response)
        return user_text

    def build_messages(self, user_text):
        messages = []

        # System prompt always goes first — sets Nova's behavior and lists available tools
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

        # If we know things about the user, remind the model
        if self.memory.memory:
            messages.append({
                "role": "system",
                "content": f"Known user facts: {self.memory.memory}"
            })

        # Last 6 messages for context — enough to follow the conversation without bloating the prompt
        messages.extend(self.memory.get_history()[-6:])

        # The current message goes at the end
        messages.append({"role": "user", "content": user_text})

        return messages

    def run_forever(self):
        logger.info("Starting continuous conversation mode")

        EXIT_COMMANDS = [
            "end conversation",
            "stop conversation",
            "goodbye nova",
            "exit"
        ]

        while True:
            user_text = self.run_once()

            if not user_text:
                continue

            if user_text.lower() in EXIT_COMMANDS:
                self.speaker.speak("Ending conversation. Goodbye.")
                logger.info("Conversation ended")
                break
