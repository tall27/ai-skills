"""Email parsing utilities."""

import base64
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def extract_text(html: str) -> str:
    """Extract plain text from HTML content."""
    if not html:
        return ""

    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except ImportError:
        pass

    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_email(msg: dict[str, Any]) -> dict[str, Any]:
    """Parse raw mail.tm message into structured format."""
    parsed = {
        "id": msg.get("id"),
        "from": msg.get("from", {}).get("address", "unknown"),
        "from_name": msg.get("from", {}).get("name"),
        "subject": msg.get("subject", "(no subject)"),
        "intro": msg.get("intro", []),
        "has_attachments": msg.get("hasAttachments", False),
        "attachments": [],
    }

    if msg.get("text"):
        parsed["body_text"] = msg["text"]
    elif msg.get("html"):
        parsed["body_text"] = extract_text(msg["html"])
        parsed["body_html"] = msg["html"]
    else:
        parsed["body_text"] = ""

    if msg.get("attachments"):
        parsed["attachments"] = [
            {
                "filename": att.get("filename"),
                "content_type": att.get("contentType"),
                "size": att.get("size"),
                "id": att.get("id"),
            }
            for att in msg["attachments"]
        ]

    return parsed


def decode_attachment(content: str, encoding: str = "base64") -> bytes:
    """Decode attachment content from string to bytes."""
    if encoding.lower() == "base64":
        return base64.b64decode(content)
    elif encoding.lower() == "quoted-printable":
        import quopri

        return quopri.decodestring(content)
    else:
        return content.encode("utf-8") if isinstance(content, str) else content
