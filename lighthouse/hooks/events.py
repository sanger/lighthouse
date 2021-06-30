#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from typing import Any, Dict, List
from flask import abort
from http import HTTPStatus

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.biosero import Biosero

from lighthouse.constants.fields import FIELD_EVENT_TYPE, FIELD_EVENT_UUID

from uuid import uuid4

logger = logging.getLogger(__name__)


def insert_events_hook(events: List[Dict[str, Any]]) -> None:
    for event in events:
        event[FIELD_EVENT_UUID] = str(uuid4())


def inserted_events_hook(events: List[Dict[str, Any]]) -> None:
    automation_system = AutomationSystem.AutomationSystemEnum.BIOSERO

    # TODO: Assume we only receive one event
    for event in events:
        try:
            biosero = Biosero()
            event_type = event.get(FIELD_EVENT_TYPE)

            if event_type is None or not isinstance(event_type, str) or not event_type:
                raise Exception("Cannot determine event type in hook")

            logger.info(f"Attempting to publish a '{event_type}' plate event message from {automation_system.name}")

            plate_event = biosero.get_plate_event(event_type)

            plate_event.initialize_event(event)
            if plate_event.is_valid():
                plate_event.process_event()

            plate_event.process_errors()
        except Exception as e:
            plate_event.process_exception(e)
            if event_type == Biosero.EVENT_DESTINATION_COMPLETED:
                abort(HTTPStatus.INTERNAL_SERVER_ERROR, "The plate could not be created because an error has happened.")
