from typing import Optional, Dict, Tuple, List
from lighthouse.messages.message import Message  # type: ignore
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_NOT_RECOGNISED,
    PLATE_EVENT_SOURCE_NO_MAP_DATA,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
)


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
    return ["Not implemented"], None


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
