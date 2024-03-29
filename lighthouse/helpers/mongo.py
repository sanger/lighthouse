import logging
from typing import Any, Dict, List, Optional, cast

from eve import Eve
from flask import current_app as app
from pymongo.collection import Collection

from lighthouse.constants.fields import (
    FIELD_BARCODE,
    FIELD_EVENT_ERRORS,
    FIELD_EVENT_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_RESULT,
)
from lighthouse.types import SampleDocs, SourcePlateDoc

logger = logging.getLogger(__name__)


def get_source_plate_uuid(barcode: str) -> Optional[str]:
    """Attempt to get a UUID for a source plate barcode.

    Arguments:
        barcode {str} -- The source plate barcode.

    Returns:
        {str} -- The source plate UUID; otherwise None if it cannot be determined.
    """
    try:
        source_plates_collection: Collection = cast(Eve, app).data.driver.db.source_plates

        source_plate: Optional[SourcePlateDoc] = source_plates_collection.find_one({FIELD_BARCODE: barcode})

        if source_plate is None:
            return None

        return source_plate.get(FIELD_LH_SOURCE_PLATE_UUID)
    except Exception as e:
        logger.error(f"An error occurred attempting to determine the UUID of source plate '{barcode}'")
        logger.exception(e)

        return None


def get_positive_samples_in_source_plate(source_plate_uuid: str) -> Optional[SampleDocs]:
    """Attempt to get a source plate's Result=Positive samples.

    Arguments:
        source_plate_uuid {str} -- The source plate UUID for which to get positive samples.

    Returns:
        {SampleDocs} -- A list of all positive samples on the source plate; otherwise None if they cannot be
        determined.
    """
    try:
        if source_plate_uuid is None:
            raise ValueError("source_plate_uuid cannot be None.")

        samples_collection: Collection = cast(Eve, app).data.driver.db.samples
        query = {
            FIELD_LH_SOURCE_PLATE_UUID: source_plate_uuid,
            FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
        }

        return list(samples_collection.find(query))
    except Exception as e:
        logger.error(f"An error occurred attempting to fetch samples on source plate '{source_plate_uuid}'")
        logger.exception(e)

        return None


def get_all_samples_for_source_plate(source_plate_uuid: str) -> Optional[SampleDocs]:
    """Attempt to get all samples for a source plate.

    Arguments:
        source_plate_uuid {str} -- The source plate UUID for which to get positive samples.

    Returns:
        {SampleDocs} -- A list of all samples on the source plate; otherwise None if they cannot be determined.
    """
    try:
        if source_plate_uuid is None:
            raise ValueError("source_plate_uuid cannot be None.")

        samples_collection: Collection = cast(Eve, app).data.driver.db.samples
        query = {FIELD_LH_SOURCE_PLATE_UUID: source_plate_uuid}

        return list(samples_collection.find(query))
    except Exception as e:
        logger.error(f"An error occurred attempting to fetch samples on source plate '{source_plate_uuid}'")
        logger.exception(e)

        return None


def set_errors_to_event(event_uuid: str, errors: Dict[str, List[str]]) -> bool:
    """Adds the list of errors provided into the event.

    Arguments:
        event_uuid {str} -- The UUID for the event to add errors to.
        errors {List[str]} -- Dict with the error messages for each event property

    Returns:
        {bool} -- True/False indicating the update result.
    """
    try:
        events_collection = cast(Eve, app).data.driver.db.events
        events_collection.update_one({FIELD_EVENT_UUID: event_uuid}, {"$set": {FIELD_EVENT_ERRORS: errors}})
        return True
    except Exception as e:
        logger.error(f"An error occurred attempting to add errors to event '{event_uuid}'")
        logger.exception(e)

        return False


def get_event_with_uuid(event_uuid: str) -> Any:
    """Returns the event with uuid specified

    Arguments:
        event_uuid {str} -- The UUID for the event

    Returns:
        {EventDoc} -- Event with that uuid, or None if not found
    """
    events_collection = cast(Eve, app).data.driver.db.events
    return events_collection.find_one({FIELD_EVENT_UUID: event_uuid})
