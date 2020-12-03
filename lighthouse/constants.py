import os
import re

DUPLICATE_SAMPLES = "DuplicateSamples"
NON_EXISTING_SAMPLE = "NonExistingSample"

# MongoDB field names
FIELD_ROOT_SAMPLE_ID = "Root Sample ID"
FIELD_RNA_ID = "RNA ID"
FIELD_RESULT = "Result"
FIELD_COORDINATE = "coordinate"
FIELD_SOURCE = "source"
FIELD_LAB_ID = "Lab ID"
FIELD_PLATE_BARCODE = "plate_barcode"
FIELD_COG_BARCODE = "cog_barcode"
FIELD_DATE_TESTED = "Date Tested"
FIELD_CH1_CQ = "CH1-Cq"
FIELD_CH2_CQ = "CH2-Cq"
FIELD_CH3_CQ = "CH3-Cq"
FIELD_LH_SOURCE_PLATE_UUID = "lh_source_plate_uuid"
FIELD_LH_SAMPLE_UUID = "lh_sample_uuid"
FIELD_BARCODE = "barcode"

# DART specific column names:
FIELD_DART_DESTINATION_BARCODE = os.environ.get("FIELD_DART_DESTINATION_BARCODE", "Labware BarCode")
FIELD_DART_DESTINATION_COORDINATE = os.environ.get(
    "FIELD_DART_DESTINATION_COORDINATE", "Well Location"
)
FIELD_DART_SOURCE_BARCODE = os.environ.get("FIELD_DART_SOURCE_BARCODE", "Well Source Barcode")
FIELD_DART_SOURCE_COORDINATE = os.environ.get("FIELD_DART_SOURCE_COORDINATE", "Well Source Well")
FIELD_DART_CONTROL = os.environ.get("FIELD_DART_CONTROL", "Well control")
FIELD_DART_ROOT_SAMPLE_ID = os.environ.get("FIELD_DART_ROOT_SAMPLE_ID", "Well root_sample_id")
FIELD_DART_RNA_ID = os.environ.get("FIELD_DART_RNA_ID", "Well rna_id")
FIELD_DART_LAB_ID = os.environ.get("FIELD_DART_LAB_ID", "Well lab_id")
FIELD_DART_RUN_ID = os.environ.get("FIELD_DART_RUN_ID", "Run-ID")

#  MLWH lighthouse samples table field names
MLWH_LH_SAMPLE_ROOT_SAMPLE_ID = "root_sample_id"
MLWH_LH_SAMPLE_COG_UK_ID = "cog_uk_id"
MLWH_LH_SAMPLE_RNA_ID = "rna_id"
MLWH_LH_SAMPLE_RESULT = "result"

# Used for filtering positive results
CT_VALUE_LIMIT = 30

# Stage for mongo aggregation pipeline
STAGE_MATCH_POSITIVE = {
    "$match": {
        #  1. We are only interested in positive samples
        FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
        # 2. We are not interested in controls
        FIELD_ROOT_SAMPLE_ID: {"$not": {"$regex": "^CBIQA_"}},
        # 3. Further filter the positive samples
        # TODO: needs to align with the crawler changes
        "$or": [
            {
                "$and": [
                    {FIELD_CH1_CQ: {"$exists": False}},
                    {FIELD_CH2_CQ: {"$exists": False}},
                    {FIELD_CH3_CQ: {"$exists": False}},
                ],
            },
            {
                "$or": [
                    {FIELD_CH1_CQ: {"$lte": CT_VALUE_LIMIT}},
                    {FIELD_CH2_CQ: {"$lte": CT_VALUE_LIMIT}},
                    {FIELD_CH3_CQ: {"$lte": CT_VALUE_LIMIT}},
                ],
            },
        ],
        # 4. We are only interested in documents which have a valid date
        FIELD_DATE_TESTED: {"$exists": True, "$nin": [None, ""]},
    }
}

# TODO: use the stage above and an aggregate intead
POSITIVE_SAMPLES_MONGODB_FILTER = {
    FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
    FIELD_ROOT_SAMPLE_ID: {"$not": re.compile("^CBIQA_")},
    "$or": [
        {"$and": [{FIELD_CH1_CQ: None}, {FIELD_CH2_CQ: None}, {FIELD_CH3_CQ: None}]},
        {
            "$or": [
                {FIELD_CH1_CQ: {"$lte": CT_VALUE_LIMIT}},
                {FIELD_CH2_CQ: {"$lte": CT_VALUE_LIMIT}},
                {FIELD_CH3_CQ: {"$lte": CT_VALUE_LIMIT}},
            ]
        },
    ],
}

# Cherrypicking source and destination plate events
PLATE_EVENT_SOURCE_COMPLETED = "lh_beckman_cp_source_completed"
PLATE_EVENT_SOURCE_NOT_RECOGNISED = "lh_beckman_cp_source_plate_unrecognised"
PLATE_EVENT_SOURCE_NO_MAP_DATA = "lh_beckman_cp_source_no_plate_map_data"
PLATE_EVENT_SOURCE_ALL_NEGATIVES = "lh_beckman_cp_source_all_negatives"
PLATE_EVENT_DESTINATION_CREATED = "lh_beckman_cp_destination_created"
PLATE_EVENT_DESTINATION_FAILED = "lh_beckman_cp_destination_failed"

# SequenceScape sampel field names
FIELD_SS_SAMPLE_DESCRIPTION = "sample_description"
FIELD_SS_NAME = "name"
FIELD_SS_LAB_ID = "lab_id"
FIELD_SS_RESULT = "result"
FIELD_SS_SUPPLIER_NAME = "supplier_name"
FIELD_SS_PHENOTYPE = "phenotype"
FIELD_SS_CONTROL = "control"
FIELD_SS_CONTROL_TYPE = "control_type"
FIELD_SS_UUID = "uuid"
