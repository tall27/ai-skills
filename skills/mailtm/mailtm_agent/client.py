"""HTTP client for mail.tm API."""

import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://api.mail.tm"


class MailTmClient:
    """Low-level HTTP client for mail.tm API."""

    def __init__(self, token: str | None = None):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def set_token(self, token: str):
        """Set authentication token."""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        """Make HTTP request with retry logic."""
        url = f"{BASE_URL}{endpoint}"
        max_retries = 3
        backoff = 1

        for attempt in range(max_retries):
            try:
                logger.debug(f"{method} {url} - Attempt {attempt + 1}")
                response = self.session.request(method, url, **kwargs)

                if response.status_code == 401:
                    logger.debug("Token expired, needs refresh")
                    raise Exception("TOKEN_EXPIRED")

                response.raise_for_status()
                logger.debug(f"Response: {response.status_code}")
                return response.json()

            except requests.exceptions.RequestException as e:
                logger.debug(f"Request error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    raise Exception(f"Request failed after {max_retries} attempts: {e}")

        raise Exception("Max retries exceeded")

    def get_domains(self) -> list[dict[str, Any]]:
        """Get available domains."""
        result = self._request("GET", "/domains")
        return result.get("hydra:member", [])

    def create_account(self, address: str, password: str) -> dict[str, Any]:
        """Create a new email account."""
        return self._request(
            "POST", "/accounts", json={"address": address, "password": password}
        )

    def get_token(self, address: str, password: str) -> str | None:
        """Get authentication token."""
        result = self._request(
            "POST", "/token", json={"address": address, "password": password}
        )
        return result.get("token")

    def get_messages(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get messages from inbox."""
        result = self._request("GET", f"/messages?itemsPerPage={limit}")
        return result.get("hydra:member", [])

    def get_message(self, msg_id: str) -> dict[str, Any]:
        """Get a specific message by ID."""
        return self._request("GET", f"/messages/{msg_id}")

    def get_attachment(self, attachment_id: str) -> bytes:
        """Download an attachment."""
        url = f"{BASE_URL}/messages/{attachment_id}/download"
        logger.debug(f"Downloading attachment from {url}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.content
