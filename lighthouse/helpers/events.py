from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from flask import current_app as app

from lighthouse.constants.fields import (
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
)
from lighthouse.types import SampleDoc


def get_routing_key(event_type: str) -> str:
    """Determines the routing key for a plate event message.

    Arguments:
        event_type {str} -- The event type for which to determine the routing key.

    Returns:
        {str} -- The message routing key.
    """
    return str(app.config["RMQ_ROUTING_KEY"].replace("#", event_type))


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


def get_robot_uuid(serial_number: str) -> Optional[str]:
    """Maps a robot serial number to a UUID.

    Arguments:
        serial_number (str): The robot serial number.

    Returns:
        Optional[str]: The robot UUID; otherwise None if it cannot be determined.
    """
    uuid = app.config.get("BECKMAN_ROBOTS", {}).get(serial_number, {}).get("uuid", None)

    if uuid is not None:
        return str(uuid)

    return None


def construct_robot_message_subject(serial_number: str, uuid: str) -> Dict[str, str]:
    """Generates a robot subject for a plate event message.

    Arguments:
        serial_number {str} -- The robot serial number.
        uuid {str} -- The robot uuid.

    Returns:
        {Dict[str, str]} -- The robot message subject.
    """
    return {
        "role_type": "robot",
        "subject_type": "robot",
        "friendly_name": serial_number,
        "uuid": uuid,
    }


def construct_mongo_sample_message_subject(sample: SampleDoc) -> Dict[str, str]:
    """Generates sample subject for a plate event message from a mongo sample.

    Arguments:
        samples {SampleDoc} -- The mongo sample for which to generate a subject.

    Returns:
        {Dict[str, str]} -- The plate message sample subject.
    """
    friendly_name = "__".join(
        [
            sample[FIELD_ROOT_SAMPLE_ID],
            sample[FIELD_RNA_ID],
            sample[FIELD_LAB_ID],
            sample[FIELD_RESULT],
        ]
    )
    return {
        "role_type": "sample",
        "subject_type": "sample",
        "friendly_name": friendly_name,
        "uuid": sample[FIELD_LH_SAMPLE_UUID],
    }


def construct_source_plate_message_subject(barcode: str, uuid: str) -> Dict[str, str]:
    """Generates a source plate subject for a plate event message.

    Arguments:
        barcode {str} -- The source plate barcode.
        uuid {str} -- The robot uuid.

    Returns:
        {Dict[str, str]} -- The source plate message subject.
    """
    return {
        "role_type": "cherrypicking_source_labware",
        "subject_type": "plate",
        "friendly_name": barcode,
        "uuid": uuid,
    }


def get_message_timestamp() -> str:
    """Returns the current datetime in a format compatible with messaging.

    Returns:
        {str} -- The current datetime.
    """
    return datetime.now().isoformat(timespec="seconds")
