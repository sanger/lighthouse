import json

from lighthouse.types import EventMessage


class Message:
    """Creates a message with the correct payload structure to send to the warehouse."""

    def __init__(self, message: EventMessage):
        self._message = message

    @property
    def message(self) -> EventMessage:
        return self._message

    def payload(self) -> str:
        """Generates the JSON payload of the message.

        Returns:
            {str} -- The message JSON payload.
        """
        return json.dumps(self._message)

    def event_type(self) -> str:
        """Return the event type.

        Returns a string representing the event type. Throws a KeyError if
        either event is not present in the root of the message, or if the
        event type key is missing. This will usually indicate that we are
        attempting to process a non event message.
        """
        return self._message.get("event", {}).get("event_type")  # type: ignore
