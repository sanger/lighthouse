import logging
from typing import Dict, Any

from lighthouse.classes.events import PlateEvent

from lighthouse.classes.event_properties.definitions import (
    SourcePlateUUID,
    PlateBarcode,
    RunID,
    SamplesFromSource,
)
from lighthouse.classes.event_properties.definitions.biosero import (
    AutomationSystemName,
    RobotUUID,
    RunInfo,
    UserID,
)


logger = logging.getLogger(__name__)


class SourceNoPickableSamples(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)

        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)
        self.properties["run_id"] = RunID(params)

        for property_name in ["plate_barcode", "run_id"]:
            self.properties[property_name].is_valid()

        self.properties["run_info"] = RunInfo(self.properties["run_id"])
        self.properties["source_plate_uuid"] = SourcePlateUUID(self.properties["plate_barcode"])
        self.properties["user_id"] = UserID(self.properties["run_info"])
        self.properties["automation_system_name"] = AutomationSystemName(self.properties["run_info"])
        self.properties["robot_uuid"] = RobotUUID(self.properties["automation_system_name"])
        self.properties["all_samples"] = SamplesFromSource(self.properties["plate_barcode"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in ["all_samples", "source_plate_uuid", "user_id", "robot_uuid", "run_info"]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()
