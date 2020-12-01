"""Handle callbacks for registered event types

Event callbacks are additional actions that will be triggered following the
creation of an event. They are triggered by passing a Message to
fire_callbacks.

Callbacks are registered in the dictionary EVENT_TYPE_CALLBACKS, which should
map an event_type to a callback function. Event types without callbacks
registered will invoke _no_callback, which does nothing.

Callbacks should return a Tuple[bool, List[str]] where the boolean indicates
success, and the list contains any errors. Note that success indicates that
the callback was processed correctly, not that it necessarily performed an
action. For example the default _no_callback still returns a success,
despite not doing anything, as this is the correct action for event types
without callbacks.

This file contains the following functions:

  * fire_callbacks - fires the callbacks for the passed message
"""

import logging
from lighthouse.messages.message import Message
from typing import Tuple, List
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
)
from lighthouse.helpers.labwhere import set_locations_in_labwhere
from flask import current_app as app

logger = logging.getLogger(__name__)


def fire_callbacks(event: Message) -> Tuple[bool, List[str]]:
    """Fire any callbacks set up for a particular event type

    Arguments:
        event {Message} -- The event for which to fire a callback

    Returns:
        {bool} -- True if the operation completed successfully
        {[str]} -- Any errors attempting to construct the message, otherwise an empty array.
    """
    event_type = event.event_type()
    callback = EVENT_TYPE_CALLBACKS.get(event_type, _no_callback)
    return callback(event)


def _no_callback(event: Message) -> Tuple[bool, List]:
    """Do nothing, but return a success"""
    logger.debug("_no_callback")
    return True, []


def _labwhere_transfer_to_bin(event: Message) -> Tuple[bool, List]:
    """Record a transfer of the cherrypicking_source_labware to the bin"""
    logger.debug("_labwhere_transfer_to_bin")
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
    """The barcode associated with the detroyed labware location in labwhere

    As this value can vary between environments, it is part of the app context
    and is configures in config/defaults.py or the appropriate environment file.
    You can also specify the barcode in the LABWHERE_DESTROYED_BARCODE
    environmental variable, which is useful in development mode.
    """
    return app.config["LABWHERE_DESTROYED_BARCODE"]


def _labware_barcodes(event: Message) -> List[str]:
    """Extracts cherrypicking_source_labware barcodes from an event message"""
    return [
        subject["friendly_name"]
        for subject in event.message["event"]["subjects"]
        if subject["role_type"] == "cherrypicking_source_labware"
    ]


def _robot_barcode(event: Message) -> str:
    """Extracts a robot barcode from an event message"""
    return next(
        subject["friendly_name"]
        for subject in event.message["event"]["subjects"]
        if subject["role_type"] == "robot"
    )


# Maps each event_type to a callback function
EVENT_TYPE_CALLBACKS = {
    PLATE_EVENT_SOURCE_ALL_NEGATIVES: _labwhere_transfer_to_bin,
    PLATE_EVENT_SOURCE_COMPLETED: _labwhere_transfer_to_bin,
}
