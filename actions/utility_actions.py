"""
utility_actions.py - LLM-powered actions: drafting emails, summarizing, translating.
These all make a separate LLM call to generate the content.
"""

from utils.logger import logger


def draft_email(to: str, subject: str, context: str, llm_client) -> str:
    logger.info(f"Drafting email — to: {to}, subject: {subject}")

    # Give the model a tight, focused prompt so it just writes the email body
    prompt = f"""Write a professional email.
        To: {to}
        Subject: {subject}
        Details: {context}

        Write only the email body. No explanations.
    """

    messages = [{"role": "user", "content": prompt}]

    try:
        email_text = llm_client.get_response(messages)
        logger.info("Email draft ready")
        return email_text

    except Exception as e:
        logger.error(f"Email draft failed: {e}")
        return "Couldn't generate the email draft."


def create_todo(items: list) -> str:
    if not items:
        return "No items to add to the list."

    # Number each item and join them into a readable list
    formatted = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    logger.info(f"Created to-do list with {len(items)} items")
    return f"Here's your to-do list:\n{formatted}"


def summarize_text(text: str, llm_client) -> str:
    logger.info("Summarizing text")

    prompt = f"Summarize this in 2-3 sentences:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]

    try:
        return llm_client.get_response(messages)
    except Exception as e:
        logger.error(f"Summary failed: {e}")
        return "Couldn't summarize that."


def translate_text(text: str, target_language: str, llm_client) -> str:
    logger.info(f"Translating to {target_language}")

    prompt = f"Translate this to {target_language}. Return only the translation:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]

    try:
        return llm_client.get_response(messages)
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return f"Couldn't translate that to {target_language}."
