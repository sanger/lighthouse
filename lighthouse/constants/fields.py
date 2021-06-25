# Fields for baracoda
FIELD_COG_BARCODE = "cog_barcode"

###
# MongoDB field names
###
# samples collection
# general fields
FIELD_ROOT_SAMPLE_ID = "Root Sample ID"
FIELD_RNA_ID = "RNA ID"
FIELD_RESULT = "Result"
FIELD_COORDINATE = "coordinate"
FIELD_SOURCE = "source"
FIELD_LAB_ID = "Lab ID"
FIELD_PLATE_BARCODE = "plate_barcode"
FIELD_DATE_TESTED = "Date Tested"
FIELD_LH_SOURCE_PLATE_UUID = "lh_source_plate_uuid"
FIELD_LH_SAMPLE_UUID = "lh_sample_uuid"
FIELD_FILTERED_POSITIVE = "filtered_positive"

# priority_samples collection
FIELD_SAMPLE_ID = "sample_id"
FIELD_MUST_SEQUENCE = "must_sequence"
FIELD_PREFERENTIALLY_SEQUENCE = "preferentially_sequence"
FIELD_PROCESSED = "processed"

# source_plates collection
FIELD_BARCODE = "barcode"

# events collection
FIELD_EVENT_RUN_ID = "automation_system_run_id"
FIELD_EVENT_BARCODE = "barcode"
FIELD_EVENT_TYPE = "event_type"
FIELD_EVENT_USER_ID = "user_id"
FIELD_EVENT_ROBOT = "robot"
FIELD_EVENT_UUID = "event_wh_uuid"
FIELD_EVENT_ERRORS = "errors"

###
# DART specific column names:
###
FIELD_DART_DESTINATION_BARCODE = "destination_barcode"
FIELD_DART_DESTINATION_COORDINATE = "destination_coordinate"
FIELD_DART_SOURCE_BARCODE = "source_barcode"
FIELD_DART_SOURCE_COORDINATE = "source_coordinate"
FIELD_DART_CONTROL = "control"
FIELD_DART_ROOT_SAMPLE_ID = "root_sample_id"
FIELD_DART_RNA_ID = "rna_id"
FIELD_DART_LAB_ID = "lab_id"
FIELD_DART_RUN_ID = "dart_run_id"

###
# PLATE LOOKUP specific column names:
###
FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_PADDED = "source_coordinate_padded"
FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_UNPADDED = "source_coordinate_unpadded"
FIELD_PLATE_LOOKUP_RNA_ID = "rna_id"
FIELD_PLATE_LOOKUP_LAB_ID = "lab_id"
FIELD_PLATE_LOOKUP_SAMPLE_ID = "sample_id"


###
# MLWH lighthouse_samples table field names
###
MLWH_LH_SAMPLE_ROOT_SAMPLE_ID = "root_sample_id"
MLWH_LH_SAMPLE_COG_UK_ID = "cog_uk_id"
MLWH_LH_SAMPLE_RNA_ID = "rna_id"
MLWH_LH_SAMPLE_RESULT = "result"

###
# Sequencescape sample field names
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

###
# Cherrytrack fields
FIELD_CHERRYTRACK_ROOT_SAMPLE_ID = "root_sample_id"
FIELD_CHERRYTRACK_RNA_ID = "rna_id"
FIELD_CHERRYTRACK_LAB_ID = "lab_id"
FIELD_CHERRYTRACK_RESULT = "result"
FIELD_CHERRYTRACK_SAMPLE_ID = "sample_id"
FIELD_CHERRYTRACK_CONTROL = "control"
FIELD_CHERRYTRACK_CONTROL_BARCODE = "control_barcode"
FIELD_CHERRYTRACK_CONTROL_COORDINATE = "control_coordinate"

###
