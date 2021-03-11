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
# NOTE: Remember that the samples of 'plate_123' are joined to the priority samples
#   There should be 7 fit to pick samples from all the plates below
SAMPLES = [
    {
        # a positive result, no Ct values and filtered_positive = True
        # joined to a priority samples with processed = False
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
    {
        # another positive result, no Ct values and filtered_positive = True
        # joined to a priority samples with processed = True
        FIELD_COORDINATE: "A02",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_002",
        FIELD_RNA_ID: "rna_2",
        FIELD_COG_BARCODE: "def",
        FIELD_LH_SAMPLE_UUID: "1a53e7b6-7ce8-4ebc-95c3-02dd64942531",
        FIELD_LH_SOURCE_PLATE_UUID: SOURCE_PLATES[0][FIELD_LH_SOURCE_PLATE_UUID],
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_1",
    },
    {
        # a negative result and filtered_positive = False
        # joined to a priority samples with processed = True
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_a",
        FIELD_RNA_ID: "rna_a",
        FIELD_COG_BARCODE: "stu",
        FIELD_LH_SAMPLE_UUID: "8426ba76-e595-4475-92a6-8a60be0eee20",
        FIELD_LH_SOURCE_PLATE_UUID: SOURCE_PLATES[0][FIELD_LH_SOURCE_PLATE_UUID],
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
        FIELD_LAB_ID: "lab_1",
    },
    {
        # a void result
        # joined to a (non) priority samples with processed = True
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_b",
        FIELD_RNA_ID: "rna_b",
        FIELD_LH_SAMPLE_UUID: "8d809bc1-2da6-42f2-9fc8-2eb6794f316f",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
        FIELD_LAB_ID: "lab_1",
    },
    {  # a 'limit of detection' result
        # joined to a (non) priority samples with processed = False
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "limit of detection",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_c",
        FIELD_RNA_ID: "rna_c",
        FIELD_LH_SAMPLE_UUID: "8e595a92-6798-4c93-8dc8-44f3ffb8bed3",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
        FIELD_LAB_ID: "lab_1",
    },
    {
        # another positive result and filtered_positive = True
        # NOT joined to a priority sample
        FIELD_COORDINATE: "E01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_123",
        FIELD_ROOT_SAMPLE_ID: "sample_101",
        FIELD_RNA_ID: "rna_6",
        FIELD_COG_BARCODE: "pqr",
        FIELD_LH_SAMPLE_UUID: "2a53e7b6-7ce8-4ebc-95c3-02dd64942532",
        FIELD_LH_SOURCE_PLATE_UUID: SOURCE_PLATES[0][FIELD_LH_SOURCE_PLATE_UUID],
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_1",
    },
    {
        # positive sample on a different plate
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_456",
        FIELD_ROOT_SAMPLE_ID: "sample_003",
        FIELD_RNA_ID: "rna_3",
        FIELD_COG_BARCODE: "ghi",
        FIELD_LH_SAMPLE_UUID: "243910d9-74bc-4da0-8f55-8606ed97b33a",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_2",
    },
    {
        # positive sample on a different plate
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_789",
        FIELD_ROOT_SAMPLE_ID: "sample_004",
        FIELD_RNA_ID: "rna_4",
        FIELD_COG_BARCODE: "jkl",
        FIELD_LH_SAMPLE_UUID: "243910d9-74bc-4da0-8f55-8606ed97b33a",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_2",
    },
    {
        # positive sample on a different plate
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "centre_1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "plate_abc",
        FIELD_ROOT_SAMPLE_ID: "sample_005",
        FIELD_RNA_ID: "rna_5",
        FIELD_COG_BARCODE: "mno",
        FIELD_LH_SAMPLE_UUID: "243910d9-74bc-4da0-8f55-8606ed97b33a",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
        FIELD_LAB_ID: "lab_3",
    },
]
