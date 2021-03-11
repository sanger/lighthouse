import json


class Message:
    """Creates a message with the correct payload structure to send to the warehouse."""

    def __init__(self, message=None):
        self.message = message

    def payload(self) -> str:
        """Generates the JSON payload of the message.

        Returns:
            {str} -- The message JSON payload.
        """
        return json.dumps(self.message)

    def event_type(self):
        """Return the event type.

        Returns a string representing the event type. Throws a KeyError if
        either event is not present in the root of the message, or if the
        event type key is missing. This will usually indicate that we are
        attempting to process a non event message.
        """

        return self.message["event"]["event_type"]
