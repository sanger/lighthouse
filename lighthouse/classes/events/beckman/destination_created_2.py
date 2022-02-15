import logging
from typing import Any, Dict

from lighthouse.classes.event_properties.definitions import (
    PlateBarcode,
    DartSamplesFromSource,
    CherrypickedSamplesFromSource,
    ClassifiedSamplesByCentre,
    SamplesWithCogUkIdBarcodes,
    CombinedDartAndMongoSamples,
    SamplesWithControls,
    SamplesMappedWithSequencescape,
    SourcePlatesForSamples,
    # PlateBarcode, 
    #SourcePlateUUID, 
    #UserID, 
    #RobotSerialNumber,
)
from lighthouse.classes.event_properties.definitions.beckman import RobotUUID
from lighthouse.classes.events import PlateEvent

logger = logging.getLogger(__name__)


class DestinationCompleted(PlateEvent):
    def __init__(self, event_type: str) -> None:
        super().__init__(event_type=event_type, plate_type=PlateEvent.PlateTypeEnum.DESTINATION)
        self.properties: Dict[str, Any] = {}

    def initialize_event(self, params: Dict[str, str]) -> None:
        super().initialize_event(params=params)
        self._event_type = params["event_type"]

        self.properties["plate_barcode"] = PlateBarcode(params)

        for property_name in ["plate_barcode"]:
            self.properties[property_name].is_valid()

        self.properties["destination_plate"] = self.properties["plate_barcode"]

        self.properties["dart_samples_from_source"] = WellsFromDestination(self.properties["plate_barcode"])
        self.properties["cherrypicked_samples_from_source"] = SamplesFromDestination(self.properties["dart_samples_from_source"])
        self.properties["classified_samples_by_centre"] = ClassifiedSamplesByCentre(self.properties["cherrypicked_samples_from_source"])
        self.properties["samples_with_cog_uk_id"] = SamplesWithCogUkId(self.properties["classified_samples_by_centre"])
        self.properties["combined_dart_mongo_samples"] =  CombinedDartAndMongoSamples(self.properties["dart_samples_from_source"], self.properties["cherrypicked_samples_from_source"])
        self.properties["samples_with_controls"] = SamplesWithControls(self.properties["dart_samples_from_source"], self.properties["combined_dart_mongo_samples"])
        self.properties["samples_mapped_with_ss"] = SamplesMappedWithSequencescape(self.properties["samples_with_controls"])
        self.properties["source_plates_for_samples"] SourcePlatesForSamples(self.properties["cherrypicked_samples_from_source"])
        #self.properties["user_id"] = UserID(params)
        #self.properties["robot_serial_number"] = RobotSerialNumber(params)
        #self.properties["robot_uuid"] = RobotUUID(self.properties["robot_serial_number"])


    def _create_message(self) -> Any:
        message = self.build_new_warehouse_message()

        for property_name in [
            "samples_with_cog_uk_id",
            "controls",
            "source_plates",
            "destination_plate",
            "user_id",
            "robot_uuid",
            #"run_info",
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
        response = message.send_to_ss()

        if not response.ok:
            raise Exception(f"There was some problem when sending message to Sequencescape: { response.text }")
