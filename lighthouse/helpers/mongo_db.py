from flask import current_app as app
import logging
from typing import List, Dict, Any, Optional
from lighthouse.constants import FIELD_LH_SOURCE_PLATE_UUID, FIELD_BARCODE

logger = logging.getLogger(__name__)


def get_source_plate_uuid(barcode: str) -> Optional[str]:
    """Attempt to get a uuid for a source plate barcode.

    Arguments:
        barcode {str} -- The source plate barcode.

    Returns:
        {str} -- The source plate uuid; otherwise None if it cannot be determined.
    """
    try:
        source_plates_collection = app.data.driver.db.source_plates
        source_plate = source_plates_collection.find_one({FIELD_BARCODE: barcode})
        if source_plate is None:
            return None

        return source_plate.get(FIELD_LH_SOURCE_PLATE_UUID, None)
    except Exception as e:
        logger.error(
            f"An error occurred attempting to determine the uuid of source plate '{barcode}'"
        )
        logger.exception(e)
        return None


def get_samples(source_plate_uuid: str) -> Optional[List[Dict[str, Any]]]:
    """Attempt to get a source plate's samples.

    Arguments:
        source_plate_uuid {str} -- The source plate uuid for which to get samples.

    Returns:
        {List[Dict[str, str]]} -- A list of all samples on the source plate;
        otherwise None if they cannot be determined
    """
    try:
        samples_collection = app.data.driver.db.samples
        return list(samples_collection.find({FIELD_LH_SOURCE_PLATE_UUID: source_plate_uuid}))
    except Exception as e:
        logger.error(
            f"An error occurred attempting to fetch samples on source plate '{source_plate_uuid}'"
        )
        logger.exception(e)
        return None
