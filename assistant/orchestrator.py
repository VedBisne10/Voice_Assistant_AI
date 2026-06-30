"""
orchestrator.py - The main loop that ties everything together.
Listen → transcribe → think → act or talk → repeat.
"""

from assistant.listener import Listener  # mic recording — captures what the user says
from assistant.transcriber import Transcriber  # converts the recorded audio to a text string
from assistant.speaker import Speaker  # turns text back into audio and plays it

from ai.local_llm_client import LocalLLMClient  # sends messages to the local Ollama model and gets replies
from ai.memory_manager import MemoryManager  # reads and writes both long-term facts and conversation history
from ai.tool_router import is_tool_call, parse_tool_call, execute_tool  # detects, parses, and runs tool call JSON

from utils.logger import logger  # shared logger so every module logs to the same place
from config.constants import SYSTEM_PROMPT  # Nova's personality, rules, and the list of tools she can use


class Orchestrator:  # main class — owns all the components and drives the conversation loop

    def __init__(self):  # constructor — wires everything up before the first conversation starts
        logger.info("Initializing Nova...")  # log that startup is beginning so we can see it in the console

        self.listener = Listener()  # set up the microphone recorder
        self.transcriber = Transcriber()  # load the Whisper speech-to-text model
        self.speaker = Speaker()  # connect to ElevenLabs for voice output
        self.llm = LocalLLMClient()  # connect to the Ollama server running locally
        self.memory = MemoryManager()  # load existing memory and conversation history from disk

        logger.info("Nova initialized successfully")  # everything booted fine, ready to talk

    def run_once(self):  # handles a single full conversation turn: listen → think → respond
        audio_file = self.listener.listen()  # record the user's voice and save it to a temp WAV file
        user_text = self.transcriber.transcribe(audio_file)  # run Whisper on that file and get the text back

        if not user_text:  # if Whisper came back with nothing, the user probably didn't say anything
            logger.warning("No speech detected")  # log it so we know the turn was skipped
            return None  # bail early — nothing to do this turn

        messages = self.build_messages(user_text)  # assemble the full prompt with system message, memory, history, and the new input
        ai_response = self.llm.get_response(messages)  # send all of that to the LLM and wait for a reply

        # If the model returned a tool call JSON, run the action.
        # Otherwise it's just a normal reply — speak it directly.
        if is_tool_call(ai_response):  # check if the response looks like {"tool": ..., "parameters": ...}
            logger.info("Tool call detected — executing")  # log that we're about to run an action
            tool_call = parse_tool_call(ai_response)  # extract the JSON dict from the raw response string

            if tool_call:  # parsing succeeded — we have a clean tool name and parameters
                spoken_response = execute_tool(tool_call, llm_client=self.llm)  # run the action and get back a human-readable result string
            else:  # response looked like JSON but we couldn't actually parse it
                logger.warning("Looked like a tool call but couldn't parse it")  # something was malformed
                spoken_response = "I understood what you wanted but couldn't execute it."  # graceful fallback the user can hear
        else:  # plain text reply — no action to run, just speak what the model said
            spoken_response = ai_response  # use the LLM's reply directly as the spoken output

        # Save to history after responding so the current exchange shows up next turn
        self.memory.add_message("user", user_text)  # store the user's message in the conversation log
        self.memory.add_message("assistant", spoken_response)  # store Nova's reply right after

        self.speaker.speak(spoken_response)  # synthesize and play the audio response
        return user_text  # return what the user said so run_forever can check for exit commands

    def build_messages(self, user_text):  # builds the message list that gets sent to the LLM
        messages = []  # start with an empty list and fill it in order

        # System prompt always goes first — sets Nova's behavior and lists available tools
        messages.append({"role": "system", "content": SYSTEM_PROMPT})  # this is always the first message in every request

        if self.memory.memory:  # if we have stored facts about the user, include them
            messages.append({  # add a second system message with the known facts
                "role": "system",  # still a system-level instruction, not a user turn
                "content": f"Known user facts: {self.memory.memory}"  # dump the memory dict as a string into the prompt
            })

        # Last 6 messages for context — enough to follow the conversation without bloating the prompt
        messages.extend(self.memory.get_history()[-6:])  # append the tail of the history — slicing avoids sending too much

        messages.append({"role": "user", "content": user_text})  # the current user message goes at the very end

        return messages  # hand back the complete message list, ready for the LLM

    def run_forever(self):  # the infinite loop that keeps Nova listening until the user says goodbye
        logger.info("Starting continuous conversation mode")  # log that we're entering the main loop

        EXIT_COMMANDS = [  # phrases that will cleanly end the session
            "end conversation",  # one way to stop
            "stop conversation",  # another way
            "goodbye nova",  # natural farewell
            "exit"  # simple kill word
        ]

        while True:  # keep going until we hit a break
            user_text = self.run_once()  # run one full turn and get back what the user said

            if not user_text:  # nothing was heard or transcribed this turn
                continue  # skip the exit check and just try again immediately

            if user_text.lower() in EXIT_COMMANDS:  # check if the user's words match any exit phrase
                self.speaker.speak("Ending conversation. Goodbye.")  # say a proper goodbye before exiting
                logger.info("Conversation ended")  # log the clean exit
                break  # exit the loop, which lets the program terminate naturally
