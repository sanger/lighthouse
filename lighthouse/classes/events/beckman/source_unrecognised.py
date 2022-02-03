import logging
from typing import Any, Dict

from lighthouse.classes.event_properties.definitions.beckman import RobotUUID
from lighthouse.classes.event_properties.definitions import UserID, RobotSerialNumber
from lighthouse.classes.events import PlateEvent

logger = logging.getLogger(__name__)


class SourceUnrecognised(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        self.properties: Dict[str, Any] = {}


    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)
        self.properties["user_id"] = UserID(params)
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in ["user_id", "robot_uuid"]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()

