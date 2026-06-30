"""
tool_router.py - Figures out if the LLM wants to run an action, then runs it.

When the model decides to do something instead of just talking, it returns JSON like:
    {"tool": "open_app", "parameters": {"app_name": "chrome"}}

This file detects that, pulls out the tool name and parameters,
and calls the matching function from the actions/ folder.
"""

import json  # for parsing the JSON the model returns in tool call responses
import re  # for extracting the JSON block from whatever text the model wraps around it
from utils.logger import logger  # shared logger used across the project

from actions.app_actions import open_app  # opens installed applications by name
from actions.browser_actions import search_web, open_website, compose_email  # browser-based actions
from actions.file_actions import open_folder, open_file, find_file  # file system navigation actions
from actions.system_actions import (  # system-level actions — time, date, screenshot, volume, etc.
    get_time, get_date, take_screenshot,  # informational and capture actions
    set_volume, lock_screen, shutdown_system, restart_system  # system control actions
)


# Maps the tool name the LLM uses to the actual Python function.
# When you add a new action, register it here.
TOOL_REGISTRY = {  # dict that connects every tool name string to the callable that handles it
    "open_app":        open_app,  # launch an app like chrome or vscode
    "search_web":      search_web,  # google something in the browser
    "open_website":    open_website,  # navigate to a specific URL
    "compose_email":   compose_email,  # open Gmail with a pre-filled draft
    "open_folder":     open_folder,  # open a named folder in Windows Explorer
    "open_file":       open_file,  # open a file at a given path
    "find_file":       find_file,  # search for a file by name in a folder
    "get_time":        get_time,  # return the current time as a readable string
    "get_date":        get_date,  # return today's date as a readable string
    "take_screenshot": take_screenshot,  # capture the screen and save it to the desktop
    "set_volume":      set_volume,  # set system volume to a percentage
    "lock_screen":     lock_screen,  # lock the Windows workstation
    "shutdown_system": shutdown_system,  # shut down the PC with a 10-second delay
    "restart_system":  restart_system,  # restart the PC with a 10-second delay
}


def is_tool_call(response: str) -> bool:  # quick check — does this response look like a tool call?
    # Just checks if the response contains a JSON object with a "tool" key
    return bool(re.search(r'\{\s*"tool"\s*:', response))  # regex match — if it finds {"tool": it's likely a tool call


def parse_tool_call(response: str) -> dict | None:  # extract and parse the JSON from the raw model response
    # The model sometimes wraps the JSON in markdown fences or adds text around it.
    # This pulls out just the JSON part and parses it.
    try:  # parsing can fail in multiple ways — be defensive
        json_match = re.search(r'\{.*"tool".*\}', response, re.DOTALL)  # grab everything between the outer braces that contains "tool"

        if not json_match:  # no JSON-like block found at all
            return None  # not a tool call, return None so the caller falls back to plain text

        tool_call = json.loads(json_match.group(0))  # parse the matched string into a Python dict

        if "tool" not in tool_call:  # sanity check — JSON was found but the "tool" key is missing
            return None  # not a valid tool call format, bail out

        # Some tools have no parameters — default to empty dict so nothing breaks
        if "parameters" not in tool_call:  # model forgot to include "parameters" in the JSON
            tool_call["parameters"] = {}  # add an empty dict so execute_tool can always do **parameters safely

        return tool_call  # hand back the clean dict with guaranteed "tool" and "parameters" keys

    except json.JSONDecodeError as e:  # the regex matched something but it wasn't valid JSON
        logger.error(f"Couldn't parse tool call JSON: {e}")  # log the specific parse error for debugging
        return None  # return None so the orchestrator can handle it gracefully


def execute_tool(tool_call: dict, llm_client=None) -> str:  # look up and call the right function, return a human-readable result
    tool_name = tool_call.get("tool")  # pull the tool name string from the dict
    parameters = tool_call.get("parameters", {})  # pull the parameters dict, default to empty if missing

    if tool_name not in TOOL_REGISTRY:  # model asked for a tool that doesn't exist in our registry
        logger.warning(f"Unknown tool: {tool_name}")  # log the unknown name so we can decide if it needs adding
        return f"I don't know how to do '{tool_name}' yet."  # polite spoken response the assistant can say

    logger.info(f"Running tool: {tool_name} | params: {parameters}")  # log what's about to run for traceability

    try:  # the action itself might throw — don't let that crash the whole assistant
        action_func = TOOL_REGISTRY[tool_name]  # look up the callable by name

        # Utility actions (like draft_email) need access to the LLM to generate content.
        # Inject the client only if the function actually expects it.
        if llm_client and "llm_client" in action_func.__code__.co_varnames:  # check the function's variable names to see if it wants llm_client
            parameters["llm_client"] = llm_client  # inject it into the parameters dict before calling

        return action_func(**parameters)  # unpack parameters as keyword arguments and call the function

    except TypeError as e:  # usually means the parameters dict doesn't match the function's signature
        logger.error(f"Wrong params for {tool_name}: {e}")  # log the mismatch details
        return f"I had a problem running {tool_name} — the parameters didn't match."  # spoken fallback

    except Exception as e:  # catch anything else — file not found, subprocess error, etc.
        logger.error(f"Error running {tool_name}: {e}")  # log the actual error
        return f"Something went wrong with {tool_name}."  # generic spoken fallback
