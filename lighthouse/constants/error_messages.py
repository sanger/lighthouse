from typing import Final

# general
ERROR_UNEXPECTED: Final[str] = "An unexpected error occurred"
ERROR_MISSING_PARAMETERS: Final[str] = "missing required parameters"
ERROR_UPDATE_MLWH_WITH_COG_UK_IDS: Final[
    str
] = "Failed to update MLWH with COG UK ids. The samples should have been successfully inserted into Sequencescape."

# /beckman endpoints
ERROR_ROBOT_CONFIG: Final[str] = "Failed fetching Beckman robot information: "
ERROR_FAILURE_TYPE_CONFIG: Final[str] = "Failed fetching Beckman failure type information: "

# /cherrypicked-plates endpoints
ERROR_CHERRYPICKED_FAILURE_RECORD: Final[str] = "Failed recording cherrypicking plate failure:"
ERROR_CHERRYPICKED_CREATE: Final[str] = "Failed to create a cherrypicked plate in Sequencescape:"


ERROR_UNEXPECTED_CHERRYPICKING_CREATE: Final[
    str
] = f"{ERROR_UNEXPECTED} attempting to create a cherrypicked plate in Sequencescape:"
ERROR_UNEXPECTED_CHERRYPICKING_FAILURE: Final[
    str
] = f"{ERROR_UNEXPECTED} attempting to record cherrypicking plate failure"

ERROR_SAMPLE_DATA_MISMATCH: Final[str] = "Mismatch in destination and source sample data for plate: "
ERROR_SAMPLE_DATA_MISSING: Final[str] = "Failed to find sample data in DART for plate barcode: "
ERROR_SAMPLES_MISSING_UUIDS: Final[str] = "No source plate UUIDs for samples of destination plate: "


# /plate-events endpoints
ERROR_PLATE_EVENT_PUBLISH: Final[str] = "Failed publishing plate event message:"
ERROR_UNEXPECTED_PLATE_EVENT_PUBLISH: Final[str] = f"{ERROR_UNEXPECTED} attempting to publish a plate event message"

# /plates endpoints
ERROR_PLATES_CREATE: Final[str] = "Failed to create a plate in Sequencescape:"
ERROR_ADD_COG_BARCODES: Final[str] = "Failed to add COG barcodes to plate:"
ERROR_UNEXPECTED_PLATES_CREATE: Final[str] = f"{ERROR_UNEXPECTED} attempting to create a plate in Sequencescape:"

# /cherrypick_test_data endpoints
ERROR_PLATE_SPECS_EMPTY_LIST: Final[str] = "should not be an empty list."
ERROR_PLATE_SPECS_INVALID_FORMAT: Final[str] = "should only contain lists of 2 integers each."
ERROR_CRAWLER_INTERNAL_SERVER_ERROR: Final[
    str
] = "There was an unexpected error while processing the run through Crawler."
