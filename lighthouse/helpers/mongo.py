import logging
from typing import List, Optional

from flask import current_app as app
from pymongo.collection import Collection

from lighthouse.constants.fields import FIELD_BARCODE, FIELD_LH_SOURCE_PLATE_UUID, FIELD_RESULT
from lighthouse.types import SampleDoc, SourcePlateDoc

logger = logging.getLogger(__name__)


def get_source_plate_uuid(barcode: str) -> Optional[str]:
    """Attempt to get a UUID for a source plate barcode.

    Arguments:
        barcode {str} -- The source plate barcode.

    Returns:
        {str} -- The source plate UUID; otherwise None if it cannot be determined.
    """
    try:
        source_plates_collection: Collection = app.data.driver.db.source_plates

        source_plate: Optional[SourcePlateDoc] = source_plates_collection.find_one({FIELD_BARCODE: barcode})

        if source_plate is None:
            return None

        return source_plate.get(FIELD_LH_SOURCE_PLATE_UUID)
    except Exception as e:
        logger.error(f"An error occurred attempting to determine the UUID of source plate '{barcode}'")
        logger.exception(e)

        return None


def get_positive_samples_in_source_plate(source_plate_uuid: str) -> Optional[List[SampleDoc]]:
    """Attempt to get a source plate's Result=Positive samples.

    Arguments:
        source_plate_uuid {str} -- The source plate UUID for which to get positive samples.

    Returns:
        {List[SampleDoc]} -- A list of all positive samples on the source plate; otherwise None if they cannot be
        determined.
    """
    try:
        samples_collection: Collection = app.data.driver.db.samples
        query = {
            FIELD_LH_SOURCE_PLATE_UUID: source_plate_uuid,
            FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
        }

        return list(samples_collection.find(query))
    except Exception as e:
        logger.error(f"An error occurred attempting to fetch samples on source plate '{source_plate_uuid}'")
        logger.exception(e)

        return None
