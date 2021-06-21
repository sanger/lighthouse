import logging
from typing import Dict, Any

from lighthouse.classes.plate_event import PlateEvent

from lighthouse.classes.event_properties.definitions import (  # type: ignore
    RobotUUID,
    RunInfo,
    SourcePlateUUID,
    UserID,
    PlateBarcode,
    RunID,
    RobotSerialNumber,
    AllSamplesFromSource,
)

logger = logging.getLogger(__name__)


class SourceAllNegatives(PlateEvent):
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
            self.properties[key].validate()

        self.properties["run_info"] = RunInfo(self.properties["run_id"])
        self.properties["source_plate_uuid"] = SourcePlateUUID(self.properties["plate_barcode"])
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])
        self.properties["all_samples"] = AllSamplesFromSource(self.properties["plate_barcode"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for key in ["all_samples", "source_plate_uuid", "user_id", "robot_uuid", "run_info"]:
            self.properties[key].add_to_warehouse_message(message)

        return message.render()
