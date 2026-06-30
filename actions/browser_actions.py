"""
browser_actions.py - Browser stuff: searching, opening sites, composing emails.
"""

import webbrowser  # opens URLs in the default system browser — no need to specify Chrome or Edge
import urllib.parse  # URL-encodes strings so special characters and spaces don't break the URL
from utils.logger import logger  # shared logger for the project


SEARCH_ENGINE_URL = "https://www.google.com/search?q="  # base URL for Google search — query gets appended to this

# Gmail's compose URL — we pre-fill to/subject/body via query params
GMAIL_COMPOSE_URL = "https://mail.google.com/mail/?view=cm&to={to}&su={subject}&body={body}"  # template with placeholders for each field

GITHUB_URL = "https://github.com/VedBisne10"  # quick reference to the developer's GitHub — not used in actions yet


def search_web(query: str) -> str:  # encode a search query and open it in the browser
    # Encode the query so spaces and symbols don't break the URL
    url = SEARCH_ENGINE_URL + urllib.parse.quote(query)  # append the URL-encoded query to the Google search base
    webbrowser.open(url)  # launch the URL in the default browser
    logger.info(f"Searching: {query}")  # log what was searched
    return f"Searching for {query}."  # short spoken confirmation


def open_website(url: str) -> str:  # open any URL, adding https:// if the user left it off
    # Be forgiving if the user didn't say "https://"
    if not url.startswith("http"):  # catches both "google.com" and "www.google.com" style inputs
        url = "https://" + url  # prepend the scheme so the browser doesn't complain

    webbrowser.open(url)  # open the final URL in the default browser
    logger.info(f"Opening: {url}")  # log the full URL for debugging
    return f"Opening {url}."  # spoken confirmation


def compose_email(to: str = "", subject: str = "", body: str = "") -> str:  # open Gmail with the compose window pre-filled
    # Each field needs to be URL-encoded or Gmail will choke on spaces/symbols
    url = GMAIL_COMPOSE_URL.format(  # substitute the encoded values into the URL template
        to=urllib.parse.quote(to),  # encode the recipient address
        subject=urllib.parse.quote(subject),  # encode the subject line
        body=urllib.parse.quote(body)  # encode the email body
    )

    webbrowser.open(url)  # open the pre-filled compose URL in the default browser
    logger.info(f"Gmail compose opened — to: {to}, subject: {subject}")  # log the key fields for tracing
    return "Opening Gmail with your draft."  # spoken confirmation
