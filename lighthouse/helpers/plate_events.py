import logging
from typing import Optional, Dict, Tuple, List
from uuid import uuid4
from flask import current_app as app
from lighthouse.messages.message import Message  # type: ignore
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_NOT_RECOGNISED,
    PLATE_EVENT_SOURCE_NO_MAP_DATA,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
)
from lighthouse.helpers.mongo_db import (
    get_source_plate_uuid,
    get_positive_samples_in_source_plate,
)
from lighthouse.helpers.events import (
    get_robot_uuid,
    construct_robot_message_subject,
    construct_mongo_sample_message_subject,
    construct_source_plate_message_subject,
    get_message_timestamp,
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
    return __construct_source_plate_with_samples_on_robot_message(
        PLATE_EVENT_SOURCE_COMPLETED, params
    )


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
        user_id = params.get("user_id")
        robot_serial_number = params.get("robot")
        if not user_id or not robot_serial_number:
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
                "occured_at": get_message_timestamp(),
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
    try:
        barcode = params.get("barcode")
        user_id = params.get("user_id")
        robot_serial_number = params.get("robot")
        if not barcode or not user_id or not robot_serial_number:
            return [
                "'barcode', 'user_id' and 'robot' are required to construct a "
                f"{PLATE_EVENT_SOURCE_NO_MAP_DATA} event message"
            ], None

        robot_uuid = get_robot_uuid(robot_serial_number)
        if robot_uuid is None:
            return [f"Unable to determine a uuid for robot '{robot_serial_number}'"], None

        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": PLATE_EVENT_SOURCE_NO_MAP_DATA,
                "occured_at": get_message_timestamp(),
                "user_identifier": user_id,
                "subjects": [
                    construct_robot_message_subject(robot_serial_number, robot_uuid),
                ],
                "metadata": {"source_plate_barcode": barcode},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return [], Message(message_content)
    except Exception as e:
        logger.error(f"Failed to construct a {PLATE_EVENT_SOURCE_NO_MAP_DATA} message")
        logger.exception(e)
        return [
            f"An unexpected error occurred attempting to construct the {PLATE_EVENT_SOURCE_NO_MAP_DATA} event message"
        ], None


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
    return __construct_source_plate_with_samples_on_robot_message(
        PLATE_EVENT_SOURCE_ALL_NEGATIVES, params
    )


# Private methods


def __construct_source_plate_with_samples_on_robot_message(
    event_type: str, params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a default message representing a source plate with samples event on a robot;
    otherwise returns appropriate errors.

    Arguments:
        event_type {str} -- The type of event to create.
        params {Dict[str, str]} -- All parameters of the plate event message request.

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    try:
        barcode = params.get("barcode")
        user_id = params.get("user_id")
        robot_serial_number = params.get("robot")
        if not barcode or not user_id or not robot_serial_number:
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

        samples = get_positive_samples_in_source_plate(source_plate_uuid)
        if samples is None:
            return [f"Unable to determine samples that belong to source plate '{barcode}'"], None

        subjects = [
            construct_robot_message_subject(robot_serial_number, robot_uuid),
            construct_source_plate_message_subject(barcode, source_plate_uuid),
        ]
        subjects.extend([construct_mongo_sample_message_subject(sample) for sample in samples])
        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": event_type,
                "occured_at": get_message_timestamp(),
                "user_identifier": user_id,
                "subjects": subjects,
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return [], Message(message_content)
    except Exception as e:
        logger.error(f"Failed to construct a {event_type} message")
        logger.exception(e)
        return [
            "An unexpected error occurred attempting to construct the "
            f"{event_type} event message"
        ], None
