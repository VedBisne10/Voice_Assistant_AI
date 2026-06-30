"""
utility_actions.py - LLM-powered actions: drafting emails, summarizing, translating.
These all make a separate LLM call to generate the content.
"""

from utils.logger import logger  # shared logger for the project


def draft_email(to: str, subject: str, context: str, llm_client) -> str:  # generate a professional email body using the LLM
    logger.info(f"Drafting email — to: {to}, subject: {subject}")  # log the key fields so we can trace what was requested

    # Give the model a tight, focused prompt so it just writes the email body
    prompt = f"""Write a professional email.
        To: {to}
        Subject: {subject}
        Details: {context}

        Write only the email body. No explanations.
    """  # structured prompt that tells the model exactly what to produce — "no explanations" stops it from adding commentary

    messages = [{"role": "user", "content": prompt}]  # single-turn request, no conversation history needed here

    try:  # the LLM call could fail — don't let that crash the assistant
        email_text = llm_client.get_response(messages)  # send to the LLM and wait for the draft
        logger.info("Email draft ready")  # log that we got something back
        return email_text  # hand back the generated email body

    except Exception as e:  # catch network errors, timeout, bad response, etc.
        logger.error(f"Email draft failed: {e}")  # log the actual error
        return "Couldn't generate the email draft."  # spoken fallback


def create_todo(items: list) -> str:  # format a list of items as a numbered to-do list
    if not items:  # if the list is empty, nothing to do
        return "No items to add to the list."  # spoken response for the empty case

    # Number each item and join them into a readable list
    formatted = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])  # "1. item one\n2. item two\n..."
    logger.info(f"Created to-do list with {len(items)} items")  # log how many items ended up in the list
    return f"Here's your to-do list:\n{formatted}"  # spoken response with the full list


def summarize_text(text: str, llm_client) -> str:  # use the LLM to condense a block of text into 2-3 sentences
    logger.info("Summarizing text")  # log that a summarization is starting

    prompt = f"Summarize this in 2-3 sentences:\n\n{text}"  # short, direct prompt — no need for elaborate instructions
    messages = [{"role": "user", "content": prompt}]  # single-turn request

    try:  # LLM call might fail
        return llm_client.get_response(messages)  # send and return the summary directly
    except Exception as e:  # catch any errors
        logger.error(f"Summary failed: {e}")  # log what went wrong
        return "Couldn't summarize that."  # spoken fallback


def translate_text(text: str, target_language: str, llm_client) -> str:  # translate a piece of text into the specified language
    logger.info(f"Translating to {target_language}")  # log the target language for tracing

    prompt = f"Translate this to {target_language}. Return only the translation:\n\n{text}"  # "return only the translation" stops the model from adding explanations
    messages = [{"role": "user", "content": prompt}]  # single-turn request — no history needed

    try:  # LLM call might fail
        return llm_client.get_response(messages)  # send and return the translation directly
    except Exception as e:  # catch any errors
        logger.error(f"Translation failed: {e}")  # log what went wrong
        return f"Couldn't translate that to {target_language}."  # spoken fallback with the target language in the message
