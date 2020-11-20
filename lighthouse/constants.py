import re

DUPLICATE_SAMPLES = "DuplicateSamples"
NON_EXISTING_SAMPLE = "NonExistingSample"

# MongoDB field names
FIELD_ROOT_SAMPLE_ID = "Root Sample ID"
FIELD_RNA_ID = "RNA ID"
FIELD_RESULT = "Result"
FIELD_COORDINATE = "coordinate"
FIELD_SOURCE = "source"
FIELD_PLATE_BARCODE = "plate_barcode"
FIELD_COG_BARCODE = "cog_barcode"
FIELD_DATE_TESTED = "Date Tested"
FIELD_CH1_CQ = "CH1-Cq"
FIELD_CH2_CQ = "CH2-Cq"
FIELD_CH3_CQ = "CH3-Cq"

#  MLWH lighthouse samples table field names
MLWH_LH_SAMPLE_ROOT_SAMPLE_ID = "root_sample_id"
MLWH_LH_SAMPLE_COG_UK_ID = "cog_uk_id"
MLWH_LH_SAMPLE_RNA_ID = "rna_id"
MLWH_LH_SAMPLE_RESULT = "result"

CT_VALUE_LIMIT = 30

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

# Stage for mongo aggregation pipeline
STAGE_MATCH_POSITIVE = {
    "$match": {
        #  1. We are only interested in positive samples
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
