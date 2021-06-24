import logging
from typing import Dict, Any

from lighthouse.classes.plate_event import PlateEvent


# TODO: The commented code in this class is one option of doing it
# that will require create:
# - SequencescapeMessage (./messages)
# - DestinationPlateBarcode (./event_properties)
# - Wells (./event_properties)
# - Samples (./event_properties)
# - Controls (./event_properties)
# << BEGIN >>

from lighthouse.classes.event_properties.definitions import (
    RobotUUID,
    RunInfo,
    CherrytrackWellsFromDestination,
    SamplesFromDestination,
    SamplesWithCogUkId,
    ControlsFromDestination,
    SourcePlatesFromDestination,
    UserID,
    PlateBarcode,
    RunID,
    RobotSerialNumber,
)
# << END >>

logger = logging.getLogger(__name__)


class DestinationCreated(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.DESTINATION)
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

        self.properties["destination_plate"] = self.properties["plate_barcode"]
        self.properties["wells"] = CherrytrackWellsFromDestination(self.properties["plate_barcode"])
        self.properties["source_plates"] = SourcePlatesFromDestination(self.properties["wells"])
        self.properties["samples"] = SamplesFromDestination(self.properties["wells"])
        self.properties["samples_with_cog_uk_id"] = SamplesWithCogUkId(self.properties["samples"])
        self.properties["controls"] = ControlsFromDestination(self.properties["wells"])
        self.properties["robot_serial_number"] = RobotSerialNumber(params)
        self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])

    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()
        #ss_message = self.build_new_sequencescape_message()

        for key in ["samples_with_cog_uk_id", "controls", "source_plates", "destination_plate", "user_id", "robot_uuid", "run_info"]:
            self.properties[key].add_to_warehouse_message(message)

        # for key in ["samples", "controls", "destination_plate", "user_id"]:
        #     self.properties[key].add_to_sequencescape_message(ss_message)

        #ss_message.add_warehouse_message(message)
        #return ss_message.render()
        return message.render()
