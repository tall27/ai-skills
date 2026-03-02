#!/usr/bin/env python3
"""
Mailtm CLI helper script for OpenCode skill.
Usage:
    python mailtm.py address   - show current email address
    python mailtm.py list      - list recent emails
    python mailtm.py wait      - wait for new email (90s timeout)
    python mailtm.py read <id> - read specific email
    python mailtm.py new       - create new inbox
"""

import sys
import io
import os
import time

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add skill directory to path for local mailtm_agent module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from mailtm_agent import MailAgent


def get_agent() -> MailAgent:
    """Create and start agent with credentials in skill directory."""
    creds_path = os.path.join(SCRIPT_DIR, "credentials.json")
    attachments_dir = os.path.join(SCRIPT_DIR, "attachments")

    agent = MailAgent(
        credentials_path=creds_path,
        attachments_dir=attachments_dir,
        debug=False,
        verbose=False,
    )
    agent.start()
    return agent


def cmd_address():
    """Show current email address."""
    agent = get_agent()
    print(agent.get_address())


def cmd_list():
    """List recent emails."""
    agent = get_agent()
    msgs = agent.get_messages(limit=5)

    if not msgs:
        print("(no emails)")
        return

    for i, m in enumerate(msgs, 1):
        subj = m.get("subject", "(no subject)")[:50]
        sender = m.get("from", "unknown")
        print(f"#{i}: {subj} <- {sender}")


def cmd_wait():
    """Wait for new email (90s timeout)."""
    agent = get_agent()

    # Get current message IDs
    initial = agent.get_messages(limit=10)
    initial_ids = {m["id"] for m in initial}

    for _ in range(18):  # 18 * 5s = 90s
        time.sleep(5)
        msgs = agent.get_messages(limit=10)

        for m in msgs:
            if m["id"] not in initial_ids:
                subj = m.get("subject", "(no subject)")[:60]
                sender = m.get("from", "unknown")
                body = m.get("body_text", "")[:200]
                print(f"NEW: {subj}")
                print(f"From: {sender}")
                if body:
                    print(f"Preview: {body}")
                return

    print("(no new email after 90s)")


def cmd_read(msg_id: str):
    """Read specific email by ID."""
    agent = get_agent()

    # If numeric, get from list
    if msg_id.isdigit():
        idx = int(msg_id) - 1
        msgs = agent.get_messages(limit=10)
        if idx < 0 or idx >= len(msgs):
            print(f"Error: invalid index {msg_id}")
            return
        msg_id = msgs[idx]["id"]

    msg = agent.get_message(msg_id)
    print(f"Subject: {msg.get('subject', '(no subject)')}")
    print(f"From: {msg.get('from', 'unknown')}")
    print()
    print(msg.get("body_text", "(no body)"))


def cmd_new():
    """Create new inbox."""
    creds_path = os.path.join(SCRIPT_DIR, "credentials.json")

    # Remove old credentials
    if os.path.exists(creds_path):
        os.remove(creds_path)

    agent = get_agent()
    print(agent.get_address())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "address":
            cmd_address()
        elif cmd == "list":
            cmd_list()
        elif cmd == "wait":
            cmd_wait()
        elif cmd == "read":
            if len(sys.argv) < 3:
                print("Usage: mailtm.py read <id|number>")
                sys.exit(1)
            cmd_read(sys.argv[2])
        elif cmd == "new":
            cmd_new()
        else:
            print(f"Unknown command: {cmd}")
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
