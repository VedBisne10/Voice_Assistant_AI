"""
tool_router.py - Figures out if the LLM wants to run an action, then runs it.

When the model decides to do something instead of just talking, it returns JSON like:
    {"tool": "open_app", "parameters": {"app_name": "chrome"}}

This file detects that, pulls out the tool name and parameters,
and calls the matching function from the actions/ folder.
"""

import json
import re
from utils.logger import logger

from actions.app_actions import open_app
from actions.browser_actions import search_web, open_website, compose_email
from actions.file_actions import open_folder, open_file, find_file
from actions.system_actions import (
    get_time, get_date, take_screenshot,
    set_volume, lock_screen, shutdown_system, restart_system
)


# Maps the tool name the LLM uses to the actual Python function.
# When you add a new action, register it here.
TOOL_REGISTRY = {
    "open_app":        open_app,
    "search_web":      search_web,
    "open_website":    open_website,
    "compose_email":   compose_email,
    "open_folder":     open_folder,
    "open_file":       open_file,
    "find_file":       find_file,
    "get_time":        get_time,
    "get_date":        get_date,
    "take_screenshot": take_screenshot,
    "set_volume":      set_volume,
    "lock_screen":     lock_screen,
    "shutdown_system": shutdown_system,
    "restart_system":  restart_system,
}


def is_tool_call(response: str) -> bool:
    # Just checks if the response contains a JSON object with a "tool" key
    return bool(re.search(r'\{\s*"tool"\s*:', response))


def parse_tool_call(response: str) -> dict | None:
    # The model sometimes wraps the JSON in markdown fences or adds text around it.
    # This pulls out just the JSON part and parses it.
    try:
        json_match = re.search(r'\{.*"tool".*\}', response, re.DOTALL)

        if not json_match:
            return None

        tool_call = json.loads(json_match.group(0))

        if "tool" not in tool_call:
            return None

        # Some tools have no parameters — default to empty dict so nothing breaks
        if "parameters" not in tool_call:
            tool_call["parameters"] = {}

        return tool_call

    except json.JSONDecodeError as e:
        logger.error(f"Couldn't parse tool call JSON: {e}")
        return None


def execute_tool(tool_call: dict, llm_client=None) -> str:
    tool_name = tool_call.get("tool")
    parameters = tool_call.get("parameters", {})

    if tool_name not in TOOL_REGISTRY:
        logger.warning(f"Unknown tool: {tool_name}")
        return f"I don't know how to do '{tool_name}' yet."

    logger.info(f"Running tool: {tool_name} | params: {parameters}")

    try:
        action_func = TOOL_REGISTRY[tool_name]

        # Utility actions (like draft_email) need access to the LLM to generate content.
        # Inject the client only if the function actually expects it.
        if llm_client and "llm_client" in action_func.__code__.co_varnames:
            parameters["llm_client"] = llm_client

        return action_func(**parameters)

    except TypeError as e:
        logger.error(f"Wrong params for {tool_name}: {e}")
        return f"I had a problem running {tool_name} — the parameters didn't match."

    except Exception as e:
        logger.error(f"Error running {tool_name}: {e}")
        return f"Something went wrong with {tool_name}."
