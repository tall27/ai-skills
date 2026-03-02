"""MailtmAgent - A reusable skill for interacting with mail.tm temporary email service."""

from mailtm_agent.agent import MailAgent
from mailtm_agent.parser import extract_text

__version__ = "1.0.0"
__all__ = ["MailAgent", "extract_text", "create_agent"]


def create_agent(**kwargs) -> MailAgent:
    """Factory function to create a MailAgent instance."""
    return MailAgent(**kwargs)
