#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from http import HTTPStatus
from typing import Any, Dict, List
from uuid import uuid4

from flask import abort, jsonify, make_response

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.biosero import Biosero
from lighthouse.constants.fields import FIELD_EVENT_TYPE, FIELD_EVENT_UUID

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

            logger.info(
                f"Attempting to process a '{event_type}' plate event message received from {automation_system.name}"
            )

            plate_event = biosero.get_plate_event(event_type)

            plate_event.initialize_event(event)
            if plate_event.is_valid():
                plate_event.process_event()

            plate_event.process_errors()
        except Exception as e:
            plate_event.process_exception(e)
            if event_type in [
                Biosero.EVENT_DESTINATION_COMPLETED,
                Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED,
                Biosero.EVENT_ERROR_RECOVERED_DESTINATION_COMPLETED,
                Biosero.EVENT_ERROR_RECOVERED_DESTINATION_PARTIAL_COMPLETED,
            ]:
                abort(
                    make_response(
                        jsonify(
                            {
                                "_status": "ERR",
                                "_issues": plate_event.errors,
                                "_error": {
                                    "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                                    "message": "The plate creation has failed.",
                                },
                            }
                        ),
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                    )
                )
