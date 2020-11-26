import logging
from typing import Optional, Dict, Tuple, List
from uuid import uuid4
from datetime import datetime
from flask import current_app as app
from lighthouse.messages.message import Message  # type: ignore
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_NOT_RECOGNISED,
    PLATE_EVENT_SOURCE_NO_MAP_DATA,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_RNA_ID,
    FIELD_LAB_ID,
    FIELD_RESULT,
    FIELD_LH_SAMPLE_UUID,
)
from lighthouse.helpers.mongo_db import (
    get_source_plate_uuid,
    get_samples,
)

logger = logging.getLogger(__name__)


def construct_event_message(
    event_type: str, params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Delegates to the appropriate event construction method;
    otherwise returns with errors for unknown event type.

    Arguments:
        event_type {str} -- The event type for which to construct a message.
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    if event_type == PLATE_EVENT_SOURCE_COMPLETED:
        return construct_source_plate_completed_message(params)
    elif event_type == PLATE_EVENT_SOURCE_NOT_RECOGNISED:
        return construct_source_plate_not_recognised_message(params)
    elif event_type == PLATE_EVENT_SOURCE_NO_MAP_DATA:
        return construct_source_plate_no_map_data_message(params)
    elif event_type == PLATE_EVENT_SOURCE_ALL_NEGATIVES:
        return construct_source_plate_all_negatives_message(params)
    else:
        return [f"Unrecognised event type '{event_type}'"], None


def get_routing_key(event_type: str) -> str:
    """Determines the routing key for a plate event message.

    Arguments:
        event_type {str} -- The event type for which to determine a routing key

    Returns:
        {str} -- The message routing key.
    """
    return app.config["RMQ_ROUTING_KEY"].replace("#", event_type)


def construct_source_plate_completed_message(
    params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a message representing a source plate complete event;
    otherwise returns appropriate errors.

    Arguments:
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    try:
        barcode = params.get("barcode", "")
        user_id = params.get("user_id", "")
        robot_serial_number = params.get("robot", "")
        if len(barcode) == 0 or len(user_id) == 0 or len(robot_serial_number) == 0:
            return [
                "'barcode', 'user_id' and 'robot' are required to construct a "
                f"{PLATE_EVENT_SOURCE_COMPLETED} event message"
            ], None

        robot_uuid = get_robot_uuid(robot_serial_number)
        if robot_uuid is None:
            return [f"Unable to determine a uuid for robot '{robot_serial_number}'"], None

        source_plate_uuid = get_source_plate_uuid(barcode)
        if source_plate_uuid is None:
            return [f"Unable to determine a uuid for source plate '{barcode}'"], None

        samples = get_samples(source_plate_uuid)
        if samples is None:
            return [f"Unable to determine samples that belong to source plate '{barcode}'"], None

        event_subjects = [
            construct_robot_message_subject(robot_serial_number, robot_uuid),
            construct_source_plate_message_subject(barcode, source_plate_uuid),
        ]
        event_subjects.extend([construct_sample_message_subject(sample) for sample in samples])
        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": PLATE_EVENT_SOURCE_COMPLETED,
                "occured_at": __get_current_datetime(),
                "user_identifier": user_id,
                "subjects": event_subjects,
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return [], Message(message_content)
    except Exception as e:
        logger.error(f"Failed to construct a {PLATE_EVENT_SOURCE_COMPLETED} message")
        logger.exception(e)
        return [
            "An unexpected error occurred attempting to construct the "
            f"{PLATE_EVENT_SOURCE_COMPLETED} event message"
        ], None


def construct_source_plate_not_recognised_message(
    params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a message representing a source plate not recognised event;
    otherwise returns appropriate errors.

    Arguments:
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    try:
        user_id = params.get("user_id", "")
        robot_serial_number = params.get("robot", "")
        if len(user_id) == 0 or len(robot_serial_number) == 0:
            return [
                "'user_id' and 'robot' are required to construct a "
                f"{PLATE_EVENT_SOURCE_NOT_RECOGNISED} event message"
            ], None

        robot_uuid = get_robot_uuid(robot_serial_number)
        if robot_uuid is None:
            return [f"Unable to determine a uuid for robot '{robot_serial_number}'"], None

        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": PLATE_EVENT_SOURCE_NOT_RECOGNISED,
                "occured_at": __get_current_datetime(),
                "user_identifier": user_id,
                "subjects": [construct_robot_message_subject(robot_serial_number, robot_uuid)],
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return [], Message(message_content)
    except Exception as e:
        logger.error(f"Failed to construct a {PLATE_EVENT_SOURCE_NOT_RECOGNISED} message")
        logger.exception(e)
        return [
            "An unexpected error occurred attempting to construct the "
            f"{PLATE_EVENT_SOURCE_NOT_RECOGNISED} event message"
        ], None


def construct_source_plate_no_map_data_message(
    params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a message representing a source plate without plate map data event;
    otherwise returns appropriate errors.

    Arguments:
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    return __construct_default_source_plate_on_robot_message(PLATE_EVENT_SOURCE_NO_MAP_DATA, params)


def construct_source_plate_all_negatives_message(
    params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a message representing a source plate without positives event;
    otherwise returns appropriate errors.

    Arguments:
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    return __construct_default_source_plate_on_robot_message(
        PLATE_EVENT_SOURCE_ALL_NEGATIVES, params
    )


def get_robot_uuid(serial_number: str) -> Optional[str]:
    """Maps a robot serial number to a uuid.

    Arguments:
        serial_number {str} -- The robot serial number.

    Returns:
        {str} -- The robot uuid; otherwise None if it cannot be determined.
    """
    return app.config.get("BECKMAN_ROBOTS", {}).get(serial_number, {}).get("uuid", None)


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


def construct_sample_message_subject(sample: Dict[str, str]) -> Dict[str, str]:
    """Generates sample subject for a plate event message.

    Arguments:
        samples {Dict[str, str]} -- The sample for which to generate a subject.

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


# Private methods


def __get_current_datetime() -> str:
    """Returns the current datetime in a format compatible with messaging.

    Returns:
        {str} -- The current datetime.
    """
    return datetime.now().isoformat(timespec="seconds")


def __construct_default_source_plate_on_robot_message(
    event_type: str, params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a default message representing a source plate event on a robot, without samples;
    otherwise returns appropriate errors.

    Arguments:
        event_type {str} -- The type of event to create.
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    try:
        barcode = params.get("barcode", "")
        user_id = params.get("user_id", "")
        robot_serial_number = params.get("robot", "")
        if len(barcode) == 0 or len(user_id) == 0 or len(robot_serial_number) == 0:
            return [
                "'barcode', 'user_id' and 'robot' are required to construct a "
                f"{event_type} event message"
            ], None

        robot_uuid = get_robot_uuid(robot_serial_number)
        if robot_uuid is None:
            return [f"Unable to determine a uuid for robot '{robot_serial_number}'"], None

        source_plate_uuid = get_source_plate_uuid(barcode)
        if source_plate_uuid is None:
            return [f"Unable to determine a uuid for source plate '{barcode}'"], None

        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": event_type,
                "occured_at": __get_current_datetime(),
                "user_identifier": user_id,
                "subjects": [
                    construct_robot_message_subject(robot_serial_number, robot_uuid),
                    construct_source_plate_message_subject(barcode, source_plate_uuid),
                ],
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return [], Message(message_content)
    except Exception as e:
        logger.error(f"Failed to construct a {event_type} message")
        logger.exception(e)
        return [
            f"An unexpected error occurred attempting to construct the {event_type} event message"
        ], None
