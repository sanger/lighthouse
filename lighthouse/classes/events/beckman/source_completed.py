import logging
from typing import Dict

from flask import current_app as app

from lighthouse.classes.services.labwhere import LabWhereMixin  # type: ignore
from lighthouse.classes.plate_event import PlateEvent
from lighthouse.helpers import mongo
from lighthouse.messages.broker import Broker
from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


class SourceCompleted(PlateEvent, LabWhereMixin):
    @property
    def robot_serial_number(self) -> str:
        return self._robot_serial_number

    def __init__(self, event_type: str) -> None:
        super().__init__(event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)

    def initialize_event(self, params: Dict[str, str]) -> None:
        self._plate_barcode = params.get("barcode", "")
        self._user_id = params.get("user_id", "")
        self._robot_serial_number = params.get("robot", "")

        if not self._plate_barcode or not self._user_id or not self._robot_serial_number:
            raise Exception(
                "'barcode', 'user_id' and 'robot' are required to construct a " f"{self._name} event message"
            )

    def _create_message(self) -> Message:
        # Import here is to prevent circular imports
        from lighthouse.classes.beckman import Beckman

        robot_uuid = Beckman.get_robot_uuid(self._robot_serial_number)
        if robot_uuid is None:
            raise Exception(f"Unable to determine a uuid for robot '{self._robot_serial_number}'")

        source_plate_uuid = mongo.get_source_plate_uuid(self._plate_barcode)
        if source_plate_uuid is None:
            raise Exception(f"Unable to determine a uuid for source plate '{self._plate_barcode}'")

        samples = mongo.get_positive_samples_in_source_plate(source_plate_uuid)
        if samples is None:
            raise Exception(f"Unable to determine samples that belong to source plate '{self._plate_barcode}'")

        subjects = [
            self.construct_message_subject(
                role_type=self.ROLE_TYPE_ROBOT,
                subject_type=self.SUBJECT_TYPE_ROBOT,
                friendly_name=self._robot_serial_number,
                uuid=robot_uuid,
            ),
            self.construct_message_subject(
                role_type=self.ROLE_TYPE_CP_SOURCE_LABWARE,
                subject_type=self.SUBJECT_TYPE_PLATE,
                friendly_name=self._plate_barcode,
                uuid=source_plate_uuid,
            ),
        ]
        subjects.extend([self.construct_mongo_sample_message_subject(sample) for sample in samples])
        message_content = self.construct_event_message(user_identifier=self._user_id, subjects=subjects)

        return Message(message_content)

    def _send_warehouse_message(self, message: Message) -> None:
        logger.info("Attempting to publish the constructed plate event message")

        routing_key = self._get_routing_key()
        with Broker() as broker_channel:
            broker_channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=routing_key,
                body=message.payload(),
            )

    def process_event(self) -> None:
        message = self._create_message()

        self._send_warehouse_message(message)

        self.transfer_to_bin()
