"""
browser_actions.py - Browser stuff: searching, opening sites, composing emails.
"""

import webbrowser
import urllib.parse
from utils.logger import logger


SEARCH_ENGINE_URL = "https://www.google.com/search?q="

# Gmail's compose URL — we pre-fill to/subject/body via query params
GMAIL_COMPOSE_URL = "https://mail.google.com/mail/?view=cm&to={to}&su={subject}&body={body}"

GITHUB_URL = "https://github.com/VedBisne10"


def search_web(query: str) -> str:
    # Encode the query so spaces and symbols don't break the URL
    url = SEARCH_ENGINE_URL + urllib.parse.quote(query)
    webbrowser.open(url)
    logger.info(f"Searching: {query}")
    return f"Searching for {query}."


def open_website(url: str) -> str:
    # Be forgiving if the user didn't say "https://"
    if not url.startswith("http"):
        url = "https://" + url

    webbrowser.open(url)
    logger.info(f"Opening: {url}")
    return f"Opening {url}."


def compose_email(to: str = "", subject: str = "", body: str = "") -> str:
    # Each field needs to be URL-encoded or Gmail will choke on spaces/symbols
    url = GMAIL_COMPOSE_URL.format(
        to=urllib.parse.quote(to),
        subject=urllib.parse.quote(subject),
        body=urllib.parse.quote(body)
    )

    webbrowser.open(url)
    logger.info(f"Gmail compose opened — to: {to}, subject: {subject}")
    return "Opening Gmail with your draft."
