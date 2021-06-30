import logging
from typing import Dict, Any

from lighthouse.classes.events import PlateEvent
from lighthouse.classes.event_properties.definitions import (
    UserID,
    RunID,
    RobotSerialNumber,
)
from lighthouse.classes.event_properties.definitions.biosero import (
    RobotUUID,
    RunInfo,
)


logger = logging.getLogger(__name__)


class SourceUnrecognised(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)

        self._event_type = params["event_type"]

        self.properties["user_id"] = UserID(params)
        self.properties["run_id"] = RunID(params)

        for property_name in ["user_id", "run_id"]:
            self.properties[property_name].is_valid()

        self.properties["run_info"] = RunInfo(self.properties["run_id"])
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in ["user_id", "robot_uuid", "run_info"]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()
