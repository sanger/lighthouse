from datetime import datetime

from lighthouse.constants.fields import (
    FIELD_COG_BARCODE,
    FIELD_COORDINATE,
    FIELD_DATE_TESTED,
    FIELD_FILTERED_POSITIVE,
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
)
from tests.fixtures.data.source_plates import SOURCE_PLATES

DATE_TESTED_NOW = datetime.utcnow()

POSITIVE_SAMPLES = [
    {
        # a positive result with source plate uuid
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_001",
        FIELD_RNA_ID: "rna_1",
        FIELD_COG_BARCODE: "abc",
        FIELD_LH_SAMPLE_UUID: "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
        FIELD_LH_SOURCE_PLATE_UUID: SOURCE_PLATES[0][FIELD_LH_SOURCE_PLATE_UUID],
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_1",
    },
]