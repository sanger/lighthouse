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
    # try get required params
    return ["Not implemented"], None


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

        robot_uuid = str(uuid4())  # TODO - get robot uuid from config
        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": PLATE_EVENT_SOURCE_NOT_RECOGNISED,
                "occured_at": get_current_datetime(),
                "user_identifier": user_id,
                "subjects": [
                    {
                        "role_type": "robot",
                        "subject_type": "robot",
                        "friendly_name": robot_serial_number,
                        "uuid": robot_uuid,
                    }
                ],
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
    return ["Not implemented"], None


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
    return ["Not implemented"], None


def get_current_datetime() -> str:
    """Returns the current datetime in a format compatible with messaging.

    Returns:
        {str} -- The current datetime.
    """
    return datetime.now().isoformat(timespec="seconds")


def get_robot_uuid(serial_number: str) -> str:
    """Maps a robot serial number to a uuid.

    Arguments:
        params {str} -- The robot serial number.

    Returns:
        {str} -- The robot uuid.
    """
    return str(uuid4())  # TODO - get robot uuid from config


