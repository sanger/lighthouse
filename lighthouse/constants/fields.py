# Fields for baracoda
from typing import Final

FIELD_COG_BARCODE: Final[str] = "cog_barcode"

###
# MongoDB field names
###
# samples collection
# general fields
FIELD_COORDINATE: Final[str] = "coordinate"
FIELD_DATE_TESTED: Final[str] = "Date Tested"
FIELD_FILTERED_POSITIVE: Final[str] = "filtered_positive"
FIELD_LAB_ID: Final[str] = "Lab ID"
FIELD_LH_SAMPLE_UUID: Final[str] = "lh_sample_uuid"
FIELD_LH_SOURCE_PLATE_UUID: Final[str] = "lh_source_plate_uuid"
FIELD_MONGO_ID: Final[str] = "_id"
FIELD_PLATE_BARCODE: Final[str] = "plate_barcode"
FIELD_RESULT: Final[str] = "Result"
FIELD_RNA_ID: Final[str] = "RNA ID"
FIELD_ROOT_SAMPLE_ID: Final[str] = "Root Sample ID"
FIELD_SOURCE: Final[str] = "source"

# priority_samples collection
FIELD_MUST_SEQUENCE: Final[str] = "must_sequence"
FIELD_PREFERENTIALLY_SEQUENCE: Final[str] = "preferentially_sequence"
FIELD_PROCESSED: Final[str] = "processed"
FIELD_SAMPLE_ID: Final[str] = "sample_id"

# source_plates collection
FIELD_BARCODE: Final[str] = "barcode"

# events collection
FIELD_EVENT_BARCODE: Final[str] = "barcode"
FIELD_EVENT_ERRORS: Final[str] = "errors"
FIELD_EVENT_ROBOT: Final[str] = "robot"
FIELD_EVENT_RUN_ID: Final[str] = "automation_system_run_id"
FIELD_EVENT_TYPE: Final[str] = "event_type"
FIELD_EVENT_USER_ID: Final[str] = "user_id"
FIELD_EVENT_UUID: Final[str] = "event_wh_uuid"
FIELD_FAILURE_TYPE: Final[str] = "failure_type"

###
# DART specific column names:
###
FIELD_DART_CONTROL: Final[str] = "control"
FIELD_DART_DESTINATION_BARCODE: Final[str] = "destination_barcode"
FIELD_DART_DESTINATION_COORDINATE: Final[str] = "destination_coordinate"
FIELD_DART_LAB_ID: Final[str] = "lab_id"
FIELD_DART_RNA_ID: Final[str] = "rna_id"
FIELD_DART_ROOT_SAMPLE_ID: Final[str] = "root_sample_id"
FIELD_DART_RUN_ID: Final[str] = "dart_run_id"
FIELD_DART_SOURCE_BARCODE: Final[str] = "source_barcode"
FIELD_DART_SOURCE_COORDINATE: Final[str] = "source_coordinate"

###
# PLATE LOOKUP specific column names:
###
FIELD_PLATE_LOOKUP_LAB_ID: Final[str] = "lab_id"
FIELD_PLATE_LOOKUP_RNA_ID: Final[str] = "rna_id"
FIELD_PLATE_LOOKUP_SAMPLE_ID: Final[str] = "sample_id"
FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_PADDED: Final[str] = "source_coordinate_padded"
FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_UNPADDED: Final[str] = "source_coordinate_unpadded"


###
# MLWH lighthouse_samples table field names
###
MLWH_LH_SAMPLE_COG_UK_ID: Final[str] = "cog_uk_id"
MLWH_LH_SAMPLE_RESULT: Final[str] = "result"
MLWH_LH_SAMPLE_RNA_ID: Final[str] = "rna_id"
MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: Final[str] = "root_sample_id"

###
# Sequencescape sample field names
###
FIELD_SS_BARCODE: Final[str] = "barcode"
FIELD_SS_CONTROL_TYPE: Final[str] = "control_type"
FIELD_SS_CONTROL: Final[str] = "control"
FIELD_SS_COORDINATE: Final[str] = "coordinate"
FIELD_SS_LAB_ID: Final[str] = "lab_id"
FIELD_SS_NAME: Final[str] = "name"
FIELD_SS_PHENOTYPE: Final[str] = "phenotype"
FIELD_SS_SAMPLE_DESCRIPTION: Final[str] = "sample_description"
FIELD_SS_SUPPLIER_NAME: Final[str] = "supplier_name"
FIELD_SS_UUID: Final[str] = "uuid"

###
# Cherrytrack fields
###
FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: Final[str] = "automation_system_manufacturer"
FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: Final[str] = "automation_system_name"
FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID: Final[str] = "automation_system_run_id"

FIELD_CHERRYTRACK_CONTROL_BARCODE: Final[str] = "control_barcode"
FIELD_CHERRYTRACK_CONTROL_COORDINATE: Final[str] = "control_coordinate"
FIELD_CHERRYTRACK_CONTROL: Final[str] = "control"

FIELD_CHERRYTRACK_DESTINATION_BARCODE: Final[str] = "destination_barcode"
FIELD_CHERRYTRACK_DESTINATION_COORDINATE: Final[str] = "destination_coordinate"
FIELD_CHERRYTRACK_LAB_ID: Final[str] = "lab_id"
FIELD_CHERRYTRACK_LH_SAMPLE_UUID: Final[str] = "lh_sample_uuid"
FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: Final[str] = "liquid_handler_serial_number"
FIELD_CHERRYTRACK_PICKED: Final[str] = "picked"
FIELD_CHERRYTRACK_RESULT: Final[str] = "result"
FIELD_CHERRYTRACK_RNA_ID: Final[str] = "rna_id"
FIELD_CHERRYTRACK_ROOT_SAMPLE_ID: Final[str] = "root_sample_id"
FIELD_CHERRYTRACK_SOURCE_BARCODE: Final[str] = "source_barcode"
FIELD_CHERRYTRACK_SOURCE_COORDINATE: Final[str] = "source_coordinate"
FIELD_CHERRYTRACK_TYPE: Final[str] = "type"
FIELD_CHERRYTRACK_USER_ID: Final[str] = "user_id"
