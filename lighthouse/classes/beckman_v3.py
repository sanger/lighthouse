import logging
from typing import Dict
from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.events.beckman import (
    # DestinationCompleted,
    # DestinationFailed,
    SourceCompleted,
    SourceNoPlateMapData,
    SourceAllNegatives,
    SourceUnrecognised,
)
from lighthouse.constants.error_messages import ERROR_FAILURE_TYPE_CONFIG, ERROR_ROBOT_CONFIG
# from .exceptions import EventNotInitializedError


logger = logging.getLogger(__name__)


class Beckman(AutomationSystem):
    # Destination plate has been created successfully
    EVENT_DESTINATION_CREATED = "lh_beckman_cp_destination_created"
    # Destination plate failed to be created successfully
    EVENT_DESTINATION_FAILED = "lh_beckman_cp_destination_failed"
    # Source plate only contains negatives, nothing to cherrypick, and the plate is put into the output stacks
    EVENT_SOURCE_ALL_NEGATIVES = "lh_beckman_cp_source_all_negatives"
    # Source plate has had all pickable wells cherrypicked into destination plate(s)
    EVENT_SOURCE_COMPLETED = "lh_beckman_cp_source_completed"
    # Source plate has no related plate map data, cannot be cherrypicked (yet)
    EVENT_SOURCE_NO_PLATE_MAP_DATA = "lh_beckman_cp_source_no_plate_map_data"
    # Source plate barcode cannot be read (damaged or missing), and the plate is put into the output stack
    EVENT_SOURCE_UNRECOGNISED = "lh_beckman_cp_source_plate_unrecognised"

    # needs to be an immutable object: https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables
    PLATE_EVENT_NAMES = (
        EVENT_DESTINATION_CREATED,
        EVENT_DESTINATION_FAILED,
        EVENT_SOURCE_ALL_NEGATIVES,
        EVENT_SOURCE_COMPLETED,
        EVENT_SOURCE_NO_PLATE_MAP_DATA,
        EVENT_SOURCE_UNRECOGNISED,
    )

    
    def __init__(self) -> None:
        self._name = AutomationSystem.AutomationSystemEnum.BECKMAN.name

        # self._event_destination_completed = DestinationCompleted(event_type=self.EVENT_DESTINATION_COMPLETED)
        # self._event_destination_failed = DestinationFailed(event_type=self.EVENT_DESTINATION_FAILED)
        self._event_source_completed = SourceCompleted(event_type=self.EVENT_SOURCE_COMPLETED)
        self._event_source_no_plate_map_data = SourceNoPlateMapData(event_type=self.EVENT_SOURCE_NO_PLATE_MAP_DATA)
        self._event_source_unrecognised = SourceUnrecognised(event_type=self.EVENT_SOURCE_UNRECOGNISED)
        self._event_source_all_negatives = SourceAllNegatives(event_type=self.EVENT_SOURCE_ALL_NEGATIVES)

        self._plate_events = {
            # self._event_destination_completed,
            # self._event_destination_failed,
            self._event_source_completed,
            self._event_source_no_plate_map_data,
            self._event_source_unrecognised,
            self._event_source_all_negatives,
        }
