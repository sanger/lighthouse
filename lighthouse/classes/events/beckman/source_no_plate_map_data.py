import logging
from typing import Any, Dict

from lighthouse.classes.event_properties.definitions import (
    PlateBarcode, 
    UserID, 
    RobotSerialNumber,
    BarcodeNoPlateMapData,
)
from lighthouse.classes.event_properties.definitions.beckman import RobotUUID
from lighthouse.classes.events import PlateEvent

logger = logging.getLogger(__name__)


class SourceNoPlateMapData(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)

        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)

        for property_name in ["plate_barcode"]:
            self.properties[property_name].is_valid()

        self.properties["user_id"] = UserID(params)
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])
        self.properties["barcode_no_plate_map_data"] = BarcodeNoPlateMapData(params)

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in ["user_id", "robot_uuid", "barcode_no_plate_map_data"]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()
