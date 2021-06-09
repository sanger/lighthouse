import logging

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.events.biosero import (
    DestinationCreated,
    DestinationFailed,
    DestinationPartial,
    SourceAllNegatives,
    SourceCompleted,
    SourceNoPickableSamples,
    SourceNoPlateMapData,
    SourceUnrecognised,
    SourcePartial,
)
from lighthouse.classes.events.biosero.source_partial import SourcePartial

logger = logging.getLogger(__name__)


class Biosero(AutomationSystem):
    ###
    # Events: https://ssg-confluence.internal.sanger.ac.uk/display/PSDPUB/%5BBiosero%5D+Cherrypicking+Events
    ###
    # Destination plate has been created successfully
    EVENT_DESTINATION_CREATED = "lh_biosero_cp_destination_created"
    # Destination plate failed to be created successfully
    EVENT_DESTINATION_FAILED = "lh_biosero_cp_destination_failed"
    # Destination plate has been partially filled
    EVENT_DESTINATION_PARTIAL = "lh_biosero_cp_destination_partial"
    # Source plate only contains negatives, nothing to cherrypick, and the plate is put into the output stacks
    EVENT_SOURCE_ALL_NEGATIVES = "lh_biosero_cp_source_all_negatives"
    # Source plate has had all pickable wells cherrypicked into destination plate(s)
    EVENT_SOURCE_COMPLETED = "lh_biosero_cp_source_completed"
    # Source plate has no pickable sample wells
    EVENT_SOURCE_NO_PICKABLE_SAMPLES = "lh_biosero_cp_source_no_pickable_samples"
    # Source plate has no related plate map data, cannot be cherrypicked (yet)
    EVENT_SOURCE_NO_PLATE_MAP_DATA = "lh_biosero_cp_source_no_plate_map_data"
    # Source plate has been partially picked
    EVENT_SOURCE_PARTIAL = "lh_biosero_cp_source_partial"
    # Source plate barcode cannot be read (damaged or missing), and the plate is put into the output stack
    EVENT_SOURCE_UNRECOGNISED = "lh_biosero_cp_source_plate_unrecognised"

    # needs to be an immutable object: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
    PLATE_EVENT_NAMES = (
        EVENT_DESTINATION_CREATED,
        EVENT_DESTINATION_FAILED,
        EVENT_DESTINATION_PARTIAL,
        EVENT_SOURCE_ALL_NEGATIVES,
        EVENT_SOURCE_COMPLETED,
        EVENT_SOURCE_PARTIALLY_COMPLETED,
        EVENT_SOURCE_NO_PICKABLE_SAMPLES,
        EVENT_SOURCE_NO_PLATE_MAP_DATA,
        EVENT_SOURCE_PARTIAL,
        EVENT_SOURCE_UNRECOGNISED,
    )

    def __init__(self) -> None:
        self._name = AutomationSystem.AutomationSystemEnum.BIOSERO.name

        self._event_destination_created = DestinationCreated(name=self.EVENT_DESTINATION_CREATED)
        self._event_destination_failed = DestinationFailed(name=self.EVENT_DESTINATION_FAILED)
        self._event_destination_partial = DestinationPartial(name=self.EVENT_DESTINATION_PARTIAL)
        self._event_source_all_negatives = SourceAllNegatives(name=self.EVENT_SOURCE_ALL_NEGATIVES)
        self._event_source_completed = SourceCompleted(name=self.EVENT_SOURCE_COMPLETED)
        self._event_source_no_pickable_samples = SourceNoPickableSamples(name=self.EVENT_SOURCE_NO_PICKABLE_SAMPLES)
        self._event_source_no_plate_map_data = SourceNoPlateMapData(name=self.EVENT_SOURCE_NO_PLATE_MAP_DATA)
        self._event_source_partial = SourcePartial(name=self.EVENT_SOURCE_PARTIAL)
        self._event_source_unrecognised = SourceUnrecognised(name=self.EVENT_SOURCE_UNRECOGNISED)

        self._plate_events = {
            self._event_destination_created,
            self._event_destination_failed,
            self._event_destination_partial,
            self._event_source_all_negatives,
            self._event_source_completed,
            self._event_source_no_pickable_samples,
            self._event_source_no_plate_map_data,
            self._event_source_partial,
            self._event_source_unrecognised,
        }