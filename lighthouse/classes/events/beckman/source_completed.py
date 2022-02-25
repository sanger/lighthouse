import logging
from typing import Any, Dict

from lighthouse.classes.event_properties.definitions import (
    PlateBarcode,
    SourcePlateUUID,
    UserID,
    RobotSerialNumber,
)
from lighthouse.classes.event_properties.definitions.beckman import RobotUUID, PositiveSamplesFromSource

from lighthouse.classes.events import PlateEvent
from lighthouse.classes.services.labwhere import LabwhereServiceMixin

logger = logging.getLogger(__name__)


class SourceCompleted(PlateEvent, LabwhereServiceMixin):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)

        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)
        self.properties["user_id"] = UserID(params)
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])

        for property_name in ["plate_barcode", "user_id", "robot_serial_number"]:
            self.properties[property_name].is_valid()

        self.properties["source_plate_uuid"] = SourcePlateUUID(self.properties["plate_barcode"])
        self.properties["positive_samples_from_source"] = PositiveSamplesFromSource(
            self.properties["source_plate_uuid"]
        )

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in ["positive_samples_from_source", "source_plate_uuid", "user_id", "robot_uuid"]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()

    def process_event(self) -> None:
        super().process_event()

        self.transfer_to_bin()
