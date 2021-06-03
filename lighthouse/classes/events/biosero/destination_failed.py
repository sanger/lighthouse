import logging
from typing import Dict

from lighthouse.classes.events.destination_plate_event import DestinationPlateEvent
from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


class Failed(DestinationPlateEvent):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    def initialize_event(self, params: Dict[str, str]) -> None:
        logger.debug("initialize_event")
        pass

    def _create_message(self) -> Message:
        logger.debug("_create_message")

        return Message({"test": "me"})

    def process_event(self) -> None:
        logger.debug("process_event")
        pass

    def _send_warehouse_message(self, message: Message) -> None:
        logger.debug("_send_warehouse_message")
        pass
