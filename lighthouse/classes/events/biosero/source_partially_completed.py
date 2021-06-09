import logging
from typing import Dict

from lighthouse.classes.events.source_plate_event import SourcePlateEvent
from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


class SourcePartiallyCompleted(SourcePlateEvent):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

    def _create_message(self) -> Message:
        logger.debug("_create_message")

        return Message({"test": "me"})

    def process_event(self) -> None:
        message = self._create_message()

        self._send_warehouse_message(message)

    def initialize_event(self, params: Dict[str, str]) -> None:
        self._plate_barcode = params.get("barcode", "")
        self._user_id = params.get("user_id", "")
        self._robot_serial_number = params.get("robot", "")

        if not self._plate_barcode or not self._user_id or not self._robot_serial_number:
            raise Exception(
                "'barcode', 'user_id' and 'robot' are required to construct a " f"{self._name} event message"
            )

    def _send_warehouse_message(self, message: Message) -> None:
        logger.info("Attempting to publish the constructed plate event message")

        routing_key = self._get_routing_key()
        with Broker() as broker_channel:
            broker_channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=routing_key,
                body=message.payload(),
            )
