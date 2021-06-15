#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from typing import Any, Dict, List

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.biosero import Biosero

from uuid import uuid4

logger = logging.getLogger(__name__)


def insert_events_hook(events: List[Dict[str, Any]]) -> None:
    for event in events:
        event["event_wh_uuid"] = str(uuid4())


def inserted_events_hook(events: List[Dict[str, Any]]) -> None:
    automation_system = AutomationSystem.AutomationSystemEnum.BIOSERO

    # TODO: Assume we only receive one event
    for event in events:
        biosero = Biosero()
        event_type = event.get("event_type")

        if event_type is None or not isinstance(event_type, str) or not event_type:
            raise Exception("Cannot determine event type in hook")

        logger.info(f"Attempting to publish a '{event_type}' plate event message from {automation_system.name}")

        plate_event = biosero.get_plate_event(event_type)

        plate_event.initialize_event(event)

        plate_event.process_event()
