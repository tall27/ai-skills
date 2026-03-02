"""Core MailAgent class."""

import logging
import random
import string
import time
from pathlib import Path
from typing import Any, Callable

from mailtm_agent.client import MailTmClient
from mailtm_agent.parser import parse_email
from mailtm_agent.storage import Storage

logger = logging.getLogger(__name__)


class MailAgent:
    """Main agent for interacting with mail.tm temporary email service."""

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        attachments_dir: str = "attachments",
        poll_interval: int = 15,
        debug: bool = False,
        verbose: bool = False,
    ):
        self.storage = Storage(credentials_path, attachments_dir)
        self.poll_interval = poll_interval
        self.debug = debug
        self.verbose = verbose
        self.client = None
        self.credentials = None
        self.running = False
        self._last_seen_id = None

    def _configure_logging(self, debug: bool = False):
        """Configure logging level."""
        level = logging.DEBUG if debug else logging.WARNING
        logging.basicConfig(
            level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def _generate_address(self, domain: str) -> str:
        """Generate a random email address."""
        username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{username}@{domain}"

    def _generate_password(self) -> str:
        """Generate a random password."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))

    def start(self) -> dict[str, Any]:
        """Initialize the agent - load or create credentials."""
        self._configure_logging(self.debug)

        self.credentials = self.storage.load_credentials()

        if self.credentials:
            token = self.credentials.get("token")
            self.client = MailTmClient(token)
            try:
                messages = self.client.get_messages(limit=1)
                logger.debug("Credentials validated successfully")
            except Exception as e:
                logger.debug(f"Credentials invalid: {e}")
                self.credentials = None
                self.client = None

        if not self.credentials:
            self._create_new_inbox()

        self.running = True
        creds = self.credentials
        return {
            "address": creds["address"],
            "token": creds["token"],
        }

    def _create_new_inbox(self) -> None:
        """Create a new email inbox."""
        logger.debug("Creating new inbox...")

        domains = (
            self.client.get_domains() if self.client else MailTmClient().get_domains()
        )
        if not domains:
            raise Exception("No domains available")

        domain = domains[0]["domain"]
        address = self._generate_address(domain)
        password = self._generate_password()

        client = MailTmClient()
        client.create_account(address, password)
        token = client.get_token(address, password)

        self.credentials = {
            "address": address,
            "password": password,
            "token": token,
        }
        self.client = MailTmClient(token)
        self.storage.save_credentials(self.credentials)

        if self.verbose:
            print(f"Created: {address}")

    def get_address(self) -> str | None:
        """Get current email address."""
        return self.credentials.get("address") if self.credentials else None

    def get_messages(self, limit: int = 10) -> list[dict[str, Any]]:
        """Fetch recent messages from inbox."""
        if not self.client:
            raise Exception("Agent not started. Call start() first.")

        try:
            messages = self.client.get_messages(limit)
            return [parse_email(msg) for msg in messages]
        except Exception as e:
            logger.debug(f"Failed to get messages: {e}")
            raise

    def get_message(self, msg_id: str) -> dict[str, Any]:
        """Get a specific message by ID."""
        if not self.client:
            raise Exception("Agent not started. Call start() first.")

        msg = self.client.get_message(msg_id)
        return parse_email(msg)

    def download_attachments(self, msg_id: str) -> list[Path]:
        """Download all attachments for a message."""
        if not self.client:
            raise Exception("Agent not started. Call start() first.")

        msg = self.client.get_message(msg_id)
        attachments = msg.get("attachments", [])
        paths = []

        for att in attachments:
            att_id = att.get("id")
            filename = att.get("filename", "attachment")

            if att.get("raw"):
                data = att["raw"].get("data", "")
                import base64

                data = base64.b64decode(data)
            else:
                data = self.client.get_attachment(att_id)

            path = self.storage.save_attachment(msg_id, filename, data)
            paths.append(path)

        return paths

    def monitor(self, callback: Callable[[dict[str, Any]], None]) -> None:
        """Monitor inbox and call callback for new emails."""
        if not self.running:
            raise Exception("Agent not started. Call start() first.")

        if not self.client:
            raise Exception("Client not initialized. Call start() first.")

        logger.debug(f"Starting monitoring (interval: {self.poll_interval}s)")

        while self.running:
            try:
                messages = self.client.get_messages(limit=10)

                for msg in messages:
                    msg_id = msg.get("id")

                    if self._last_seen_id is None or msg_id != self._last_seen_id:
                        parsed = parse_email(msg)
                        callback(parsed)
                        self._last_seen_id = msg_id

                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                logger.debug("Monitoring stopped by user")
                break
            except Exception as e:
                logger.debug(f"Monitor error: {e}")
                time.sleep(self.poll_interval)

    def stop(self) -> None:
        """Stop the monitoring loop."""
        self.running = False
        logger.debug("Agent stopped")
