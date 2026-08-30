"""Mock email service - simulates sending emails."""
import json
import os
from datetime import datetime, timezone


class MockEmailService:
    """Mock email service that saves messages to a JSON file instead of sending real emails."""

    SENT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mock_sent_emails.json')

    @classmethod
    def send(cls, to_email, subject, body, invoice_number=None):
        """Simulate sending an email."""
        message = {
            'to': to_email or 'no-email@placeholder.local',
            'subject': subject,
            'body': body,
            'invoice_number': invoice_number,
            'sent_at': datetime.now(timezone.utc).isoformat(),
            'status': 'delivered',
            'provider': 'mock',
        }

        # Append to mock sent file
        sent_messages = []
        if os.path.exists(cls.SENT_FILE):
            try:
                with open(cls.SENT_FILE, 'r') as f:
                    sent_messages = json.load(f)
            except (json.JSONDecodeError, IOError):
                sent_messages = []

        sent_messages.append(message)

        with open(cls.SENT_FILE, 'w') as f:
            json.dump(sent_messages, f, indent=2)

        return {
            'success': True,
            'message_id': f'mock-{invoice_number}-{len(sent_messages)}',
            'provider': 'mock',
        }
