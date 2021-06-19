import logging
import logging.config
from abc import ABC
from enum import Enum, auto
from typing import List, Set

from lighthouse.classes.plate_event import PlateEvent

logger = logging.getLogger(__name__)


class AutomationSystem(ABC):
    class AutomationSystemEnum(Enum):
        BECKMAN = auto()
        BIOSERO = auto()

    def __init__(self):
        self._name = ""
        self._plate_events: Set[PlateEvent] = set()

    @property
    def plate_events(self) -> Set[PlateEvent]:
        return self._plate_events

    def get_plate_event_types(self) -> List[str]:
        return [event.event_type for event in self.plate_events]

    def is_valid_plate_event(self, event_type: str) -> bool:
        if event_type in self.get_plate_event_types():
            return True

        return False

    def get_plate_event(self, event_type: str) -> PlateEvent:
        if self.is_valid_plate_event(event_type):
            for event in self.plate_events:
                if event.event_type == event_type:
                    return event

        raise Exception("Event type invalid or not found")
