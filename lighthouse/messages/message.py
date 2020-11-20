import json
from typing import Any


class Message:
    """Creates a message with the correct payload structure to send to the warehouse."""

    def __init__(self, message: Any = None):
        self.message = message

    def payload(self) -> str:
        """Generates the JSON payload of the message.

        Returns:
            {str} -- The message JSON payload.
        """
        return json.dumps(self.message)
