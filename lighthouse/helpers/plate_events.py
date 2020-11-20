from typing import Optional, Dict, Tuple, List
from lighthouse.messages.message import Message  # type: ignore


def construct_event_message(
    event_type: str, params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Delegates to the appropriate event construction method;
    otherwise returns with errors for unknown event type

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    if event_type == "lh_beckman_cp_source_completed":
        return construct_source_plate_complete_message(params)
    elif event_type == "lh_beckman_cp_source_plate_unrecognised":
        return construct_source_plate_not_recognised_message(params)
    elif event_type == "lh_beckman_cp_source_no_plate_map_data":
        return construct_source_plate_no_map_data_message(params)
    elif event_type == "lh_beckman_cp_source_all_negatives":
        return construct_source_plate_all_negatives_message(params)
    else:
        return [f"Unrecognised event type '{event_type}'"], None


def construct_source_plate_complete_message(
    params: Dict[str, str]
) -> Tuple[List[str], Optional[Message]]:
    """Constructs a message representing a source plate complete event;
    otherwise returns appropriate errors.

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

    Returns:
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
        {Message} -- The constructed message; otherwise None if there are any errors.
    """
    return ["Not implemented"], None
