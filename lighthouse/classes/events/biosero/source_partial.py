import logging
from typing import Dict

from lighthouse.classes.plate_event import PlateEvent
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage

from lighthouse.classes.messages.event_properties import (
    PickedSamplesFromSource,
    RobotUUID,
    RunInfo,
    SourcePlateUUID,
    UserID,
    PlateBarcode,
    RunID,
    RobotSerialNumber,
)

logger = logging.getLogger(__name__)


class SourcePartial(PlateEvent):
    def __init__(self, name: str) -> None:
        super().__init__(name=name, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties = {}

    def process_event(self) -> None:
        message = self._create_message()

        self._send_warehouse_message(message)

    def initialize_event(self, params: Dict[str, str]) -> None:
        self.event_type = params['event_type']

        self.properties['plate_barcode'] = PlateBarcode(params)
        self.properties['user_id'] = UserID(params)
        self.properties['run_id'] = RunID(params)

        for key in ['plate_barcode', 'user_id', 'run_id']:
            self.properties[key].valid()

        self.properties['run_info'] = RunInfo(self.properties['run_id'])
        self.properties['picked_samples_from_source'] = PickedSamplesFromSource(
             self.properties['plate_barcode'], self.properties['run_info']
        )
        self.properties['source_plate_uuid'] = SourcePlateUUID(self.properties['plate_barcode'])
        self.properties['robot_serial_number'] = RobotSerialNumber(params)
        self.properties['robot_uuid'] = RobotUUID(self.properties['robot_serial_number'])

    def _create_message(self):
        message = WarehouseMessage(self.event_type)

        for key in ['picked_samples_from_source', 'source_plate_uuid', 'user_id', 'robot_uuid']:
            self.properties[key].add_to_warehouse_message(message)

        return message.render()

