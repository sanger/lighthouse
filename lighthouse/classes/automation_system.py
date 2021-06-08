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

    def get_plate_event_names(self) -> List[str]:
        return [event.name for event in self.plate_events]

    def is_valid_plate_event(self, event_name: str) -> bool:
        if event_name in self.get_plate_event_names():
            return True

        return False

    def get_plate_event(self, event_name: str) -> PlateEvent:
        if self.is_valid_plate_event(event_name):
            for event in self.plate_events:
                if event.name == event_name:
                    return event

        raise Exception("Event name invalid or not found")
