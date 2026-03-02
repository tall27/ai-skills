"""Storage utilities for credentials and attachments."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Storage:
    """Manages credentials and attachment storage."""

    def __init__(
        self,
        credentials_path: str = "credentials.json",
        attachments_dir: str = "attachments",
    ):
        self.credentials_path = Path(credentials_path)
        self.attachments_dir = Path(attachments_dir)

    def load_credentials(self) -> dict[str, Any] | None:
        """Load credentials from file."""
        if not self.credentials_path.exists():
            logger.debug(f"Credentials file not found: {self.credentials_path}")
            return None

        try:
            with open(self.credentials_path, "r") as f:
                creds = json.load(f)
            logger.debug(f"Loaded credentials for: {creds.get('address', 'unknown')}")
            return creds
        except (json.JSONDecodeError, IOError) as e:
            logger.debug(f"Failed to load credentials: {e}")
            return None

    def save_credentials(self, credentials: dict[str, Any]) -> None:
        """Save credentials to file."""
        self.credentials_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.credentials_path, "w") as f:
            json.dump(credentials, f, indent=2)
        logger.debug(f"Saved credentials for: {credentials.get('address')}")

    def get_attachment_path(self, msg_id: str, filename: str) -> Path:
        """Get path for saving an attachment."""
        folder = self.attachments_dir / msg_id
        folder.mkdir(parents=True, exist_ok=True)
        return folder / filename

    def save_attachment(self, msg_id: str, filename: str, data: bytes) -> Path:
        """Save attachment to disk."""
        path = self.get_attachment_path(msg_id, filename)
        with open(path, "wb") as f:
            f.write(data)
        logger.debug(f"Saved attachment: {path}")
        return path

    def list_attachments(self, msg_id: str) -> list[Path]:
        """List downloaded attachments for a message."""
        folder = self.attachments_dir / msg_id
        if not folder.exists():
            return []
        return list(folder.iterdir())
