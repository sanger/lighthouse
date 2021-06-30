import logging
from typing import Dict, Any

from lighthouse.classes.events import PlateEvent
from lighthouse.classes.event_properties.definitions import (
    SamplesFromDestination,
    SamplesWithCogUkId,
    ControlsFromDestination,
    SourcePlatesFromDestination,
    UserID,
    PlateBarcode,
    RunID,
    RobotSerialNumber,
)

from lighthouse.classes.event_properties.definitions.biosero import (
    RobotUUID,
    RunInfo,
    WellsFromDestination,
)

logger = logging.getLogger(__name__)


class DestinationCompleted(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.DESTINATION)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)
        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)
        self.properties["user_id"] = UserID(params)
        self.properties["run_id"] = RunID(params)

        for property_name in ["plate_barcode", "user_id", "run_id"]:
            self.properties[property_name].is_valid()

        self.properties["run_info"] = RunInfo(self.properties["run_id"])

        self.properties["destination_plate"] = self.properties["plate_barcode"]
        self.properties["wells"] = WellsFromDestination(self.properties["plate_barcode"])
        self.properties["source_plates"] = SourcePlatesFromDestination(self.properties["wells"])
        self.properties["samples"] = SamplesFromDestination(self.properties["wells"])
        self.properties["samples_with_cog_uk_id"] = SamplesWithCogUkId(self.properties["samples"])
        self.properties["controls"] = ControlsFromDestination(self.properties["wells"])
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in [
            "samples_with_cog_uk_id",
            "controls",
            "source_plates",
            "destination_plate",
            "user_id",
            "robot_uuid",
            "run_info",
        ]:
            self.properties[property_name].add_to_warehouse_message(message)

        return message.render()

    def _create_sequencescape_message(self) -> Any:
        ss_message = self.build_new_sequencescape_message()

        for property_name in ["samples_with_cog_uk_id", "controls", "destination_plate"]:
            self.properties[property_name].add_to_sequencescape_message(ss_message)

        return ss_message

    def process_event(self) -> None:
        super().process_event()

        message = self._create_sequencescape_message()
        body = message.render()
        response = message.send_to_ss()

        if not response.ok:
            raise Exception(f"There was some problem when sending message to Sequencescape: { body }")
