"""Handle callbacks for registered event types

Event callbacks are additional actions that will be triggered following the creation of an event. They are triggered by
passing a Message to fire_callbacks.

Callbacks are registered in the dictionary EVENT_TYPE_CALLBACKS, which should map an event_type to a callback function.
Event types without callbacks registered will invoke _no_callback, which does nothing.

Callbacks should return a Tuple[bool, List[str]] where the boolean indicates success, and the list contains any errors.
Note that success indicates that the callback was processed correctly, not that it necessarily performed an action. For
example the default _no_callback still returns a success, despite not doing anything, as this is the correct action for
event types without callbacks.
"""

import logging
from typing import List, Tuple

from flask import current_app as app

from lighthouse.constants.events import PE_BECKMAN_SOURCE_ALL_NEGATIVES, PE_BECKMAN_SOURCE_COMPLETED
from lighthouse.helpers.labwhere import set_locations_in_labwhere
from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


def fire_callbacks(event: Message) -> Tuple[bool, List[str]]:
    """Fire any callbacks set up for a particular event type.

    Arguments:
        event {Message} -- The event for which to fire a callback

    Returns:
        {bool} -- True if the operation completed successfully.
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
    """
    event_type = event.event_type()

    callback = EVENT_TYPE_CALLBACKS.get(event_type, _no_callback)

    return callback(event)


def _no_callback(event: Message) -> Tuple[bool, List[str]]:
    """Do nothing, but return a success"""
    return True, []


def _labwhere_transfer_to_bin(event: Message) -> Tuple[bool, List[str]]:
    """Record a transfer of the cherrypicking_source_labware to the bin

    Args:
        event (Message): The event for which to fire a callback

    Returns:
        Tuple[bool, List[str]]: True if the operation completed successfully; any errors attempting to construct the
        message, otherwise an empty array.
    """
    try:
        labware_barcodes = _labware_barcodes(event)
        location_barcode = _labwhere_destroyed_barcode()
        robot_barcode = _robot_barcode(event)

        set_locations_in_labwhere(
            labware_barcodes=labware_barcodes,
            location_barcode=location_barcode,
            user_barcode=robot_barcode,
        )

        return True, []
    except Exception as e:
        return False, [f"{type(e).__name__}: {str(e)}"]


def _labwhere_destroyed_barcode() -> str:
    """The barcode associated with the destroyed labware location in LabWhere.

    As this value can vary between environments, it is part of the app context and is configured in `config/defaults.py`
    or the appropriate environment file. You can also specify the barcode in the `LABWHERE_DESTROYED_BARCODE`
    environmental variable, which is useful in development mode.

    Returns:
        str: barcode associated with the destroyed labware location in LabWhere
    """
    return str(app.config["LABWHERE_DESTROYED_BARCODE"])


def _labware_barcodes(event: Message) -> List[str]:
    """Extracts cherrypicking_source_labware barcodes from an event message

    Args:
        event (Message): The event

    Returns:
        List[str]: cherrypicking_source_labware barcodes
    """
    return [
        subject["friendly_name"]  # type: ignore
        for subject in event.message["event"]["subjects"]  # type: ignore
        if subject["role_type"] == "cherrypicking_source_labware"  # type: ignore
    ]


def _robot_barcode(event: Message) -> str:
    """Extracts a robot barcode from an event message.

    Args:
        event (Message): The event

    Returns:
        str: robot barcode
    """
    return str(
        next(
            subject["friendly_name"]  # type: ignore
            for subject in event.message["event"]["subjects"]  # type: ignore
            if subject["role_type"] == "robot"  # type: ignore
        )
    )


# Maps each event_type to a callback function
EVENT_TYPE_CALLBACKS = {
    PE_BECKMAN_SOURCE_ALL_NEGATIVES: _labwhere_transfer_to_bin,
    PE_BECKMAN_SOURCE_COMPLETED: _labwhere_transfer_to_bin,
}
