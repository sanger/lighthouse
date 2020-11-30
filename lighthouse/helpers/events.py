from flask import current_app as app
from typing import Dict
from uuid import uuid4


def get_routing_key(event_type: str) -> str:
    """Determines the routing key for a plate event message.

    Arguments:
        event_type {str} -- The event type for which to determine a routing key

    Returns:
        {str} -- The message routing key.
    """
    return app.config["RMQ_ROUTING_KEY"].replace("#", event_type)


def construct_destination_plate_message_subject(barcode: str) -> Dict[str, str]:
    """Constructs a message subject for a cherrypicking destination plate.

    Arguments:
        barcode {str} -- The destination plate's barcode.

    Returns:
        {Dict[str, str]} -- The destination plate message subject.
    """
    return {
        "role_type": "cherrypicking_destination_labware",
        "subject_type": "plate",
        "friendly_name": barcode,
        "uuid": str(uuid4()),
    }
