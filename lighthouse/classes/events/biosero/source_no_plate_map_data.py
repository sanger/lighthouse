import logging
from typing import Dict, Any

from lighthouse.classes.plate_event import PlateEvent

from lighthouse.classes.event_properties.definitions import (
    RobotUUID,
    RunInfo,
    UserID,
    PlateBarcode,
    RunID,
    RobotSerialNumber,
    BarcodeNoPlateMapData,
)

logger = logging.getLogger(__name__)


class SourceNoPlateMapData(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)

        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)
        self.properties["user_id"] = UserID(params)
        self.properties["run_id"] = RunID(params)

        for key in ["plate_barcode", "user_id", "run_id"]:
            self.properties[key].is_valid()

        self.properties["run_info"] = RunInfo(self.properties["run_id"])
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])
        self.properties["barcode_no_plate_map_data"] = BarcodeNoPlateMapData(params)

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for key in ["user_id", "robot_uuid", "barcode_no_plate_map_data", "run_info"]:
            self.properties[key].add_to_warehouse_message(message)

        return message.render()
