import os

DUPLICATE_SAMPLES = "DuplicateSamples"
NON_EXISTING_SAMPLE = "NonExistingSample"

# Plate barcode in the source_plates collection
FIELD_BARCODE = "barcode"

# Fields for baracoda
FIELD_COG_BARCODE = "cog_barcode"

###
# MongoDB field names
###
# general fields
FIELD_ROOT_SAMPLE_ID = "Root Sample ID"
FIELD_RNA_ID = "RNA ID"
FIELD_RESULT = "Result"
FIELD_COORDINATE = "coordinate"
FIELD_SOURCE = "source"
FIELD_LAB_ID = "Lab ID"
FIELD_PLATE_BARCODE = "plate_barcode"
FIELD_DATE_TESTED = "Date Tested"

# UUID fields
FIELD_LH_SOURCE_PLATE_UUID = "lh_source_plate_uuid"
FIELD_LH_SAMPLE_UUID = "lh_sample_uuid"

# Filtered positive fields
FIELD_FILTERED_POSITIVE = "filtered_positive"

###
# DART specific column names:
###
FIELD_DART_DESTINATION_BARCODE = os.environ.get(
    "FIELD_DART_DESTINATION_BARCODE", "destination_barcode"
)
FIELD_DART_DESTINATION_COORDINATE = os.environ.get(
    "FIELD_DART_DESTINATION_COORDINATE", "destination_coordinate"
)
FIELD_DART_SOURCE_BARCODE = os.environ.get("FIELD_DART_SOURCE_BARCODE", "source_barcode")
FIELD_DART_SOURCE_COORDINATE = os.environ.get("FIELD_DART_SOURCE_COORDINATE", "source_coordinate")
FIELD_DART_CONTROL = os.environ.get("FIELD_DART_CONTROL", "control")
FIELD_DART_ROOT_SAMPLE_ID = os.environ.get("FIELD_DART_ROOT_SAMPLE_ID", "root_sample_id")
FIELD_DART_RNA_ID = os.environ.get("FIELD_DART_RNA_ID", "rna_id")
FIELD_DART_LAB_ID = os.environ.get("FIELD_DART_LAB_ID", "lab_id")
FIELD_DART_RUN_ID = os.environ.get("FIELD_DART_RUN_ID", "dart_run_id")

###
# MLWH lighthouse samples table field names
###
MLWH_LH_SAMPLE_ROOT_SAMPLE_ID = "root_sample_id"
MLWH_LH_SAMPLE_COG_UK_ID = "cog_uk_id"
MLWH_LH_SAMPLE_RNA_ID = "rna_id"
MLWH_LH_SAMPLE_RESULT = "result"

# Stage for mongo aggregation pipeline
STAGE_MATCH_FILTERED_POSITIVE = {
    "$match": {
        # 1. We are only interested filtered positive samples
        FIELD_FILTERED_POSITIVE: True,
        # 2. We are only interested in documents which have a valid date
        FIELD_DATE_TESTED: {"$exists": True, "$nin": [None, ""]},
    }
}

# Sentinel workflow event to help determine sample cherrypicked status
EVENT_CHERRYPICK_LAYOUT_SET = "cherrypick_layout_set"

###
# Events detailed: https://ssg-confluence.internal.sanger.ac.uk/display/PSDPUB/Cherrypicking+Events
# Source plate has had all pickable wells cherrypicked into destination plates, and the plate is
# put into the output stacks.
# Cherrypicking source and destination plate events
###
PLATE_EVENT_SOURCE_COMPLETED = "lh_beckman_cp_source_completed"
# Source plate barcode cannot be read (damaged or missing), and the plate is put into the output
# stacks.
PLATE_EVENT_SOURCE_NOT_RECOGNISED = "lh_beckman_cp_source_plate_unrecognised"
# Source plate has no related plate map data, cannot be cherrypicked (yet), and the plate is
# returned to the input
# stacks.
PLATE_EVENT_SOURCE_NO_MAP_DATA = "lh_beckman_cp_source_no_plate_map_data"
# Source plate only contains negatives, nothing to cherrypick, and the plate is put into the output
# stacks.
PLATE_EVENT_SOURCE_ALL_NEGATIVES = "lh_beckman_cp_source_all_negatives"
# Destination plate has been created successfully
PLATE_EVENT_DESTINATION_CREATED = "lh_beckman_cp_destination_created"
# Destination plate has failed to be created successfully
PLATE_EVENT_DESTINATION_FAILED = "lh_beckman_cp_destination_failed"

###
# SequenceScape sample field names
###
FIELD_SS_SAMPLE_DESCRIPTION = "sample_description"
FIELD_SS_NAME = "name"
FIELD_SS_LAB_ID = "lab_id"
FIELD_SS_RESULT = "result"
FIELD_SS_SUPPLIER_NAME = "supplier_name"
FIELD_SS_PHENOTYPE = "phenotype"
FIELD_SS_CONTROL = "control"
FIELD_SS_CONTROL_TYPE = "control_type"
FIELD_SS_UUID = "uuid"
FIELD_SS_COORDINATE = "coordinate"
FIELD_SS_BARCODE = "barcode"

# Columns that should appear in the filtered positive samples report and the order in which they
# will appear
REPORT_COLUMNS = [
    "Date Tested",
    "Root Sample ID",
    "Result",
    "source",
    "plate_barcode",
    "coordinate",
    "plate and well",
    "location_barcode",
    "LIMS submission",
]
