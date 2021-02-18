from copy import copy
from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

from lighthouse.constants import (
    EVENT_CHERRYPICK_LAYOUT_SET,
    FIELD_BARCODE,
    FIELD_COG_BARCODE,
    FIELD_COORDINATE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
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
    MLWH_LH_SAMPLE_RESULT,
    MLWH_LH_SAMPLE_RNA_ID,
    MLWH_LH_SAMPLE_ROOT_SAMPLE_ID,
    PLATE_EVENT_DESTINATION_CREATED,
)

CENTRES: List[Dict[str, str]] = [
    {"name": "test1", "prefix": "TS1"},
    {"name": "test2", "prefix": "TS2"},
    {"name": "test3", "prefix": "TS3"},
]

FIRST_TIMESTAMP = datetime(2013, 4, 4, 10, 29, 13)
SECOND_TIMESTAMP = datetime(2013, 4, 5, 10, 29, 13)
THIRD_TIMESTAMP = datetime(2013, 4, 6, 10, 29, 13)


SAMPLES_DECLARATIONS: List[Dict[str, Any]] = [
    {
        "root_sample_id": "MCM001",
        "value_in_sequencing": "Yes",
        "declared_at": FIRST_TIMESTAMP,
    },
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": FIRST_TIMESTAMP},
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": SECOND_TIMESTAMP},
    {
        "root_sample_id": "MCM003",
        "value_in_sequencing": "Yes",
        "declared_at": THIRD_TIMESTAMP,
    },
]

MULTIPLE_ERRORS_SAMPLES_DECLARATIONS: List[Dict[str, Any]] = [
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020466",
        "value_in_sequencing": "No",
    },
    {"declared_at": "2020-06-26T11:37:45", "value_in_sequencing": "No"},
    {"declared_at": "2020-14-500", "root_sample_id": "YOR10020379", "value_in_sequencing": "No"},
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020240",
        "value_in_sequencing": "Yes",
    },
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020379",
        "value_in_sequencing": "Yes",
    },
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020224",
        "value_in_sequencing": "Yes",
    },
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020217",
        "othertag": "othervalue",
    },
    {
        "declared_at": "2020-06-26T11:37:45",
        "root_sample_id": "YOR10020195",
        "value_in_sequencing": "maybelater",
    },
]

MAX_SAMPLES = 1000

LOTS_OF_SAMPLES: List[Dict[str, str]] = [
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "abc",
        FIELD_ROOT_SAMPLE_ID: f"MCM00{i}",
    }
    for i in range(0, MAX_SAMPLES)
]

LOTS_OF_SAMPLES_DECLARATIONS_PAYLOAD: List[Dict[str, str]] = [
    {
        "root_sample_id": f"MCM00{i}",
        "value_in_sequencing": "Yes",
        "declared_at": "2013-04-04T10:29:13",
    }
    for i in range(0, MAX_SAMPLES)
]

DATE_TESTED_NOW = datetime.utcnow()
SAMPLES: List[Dict[str, Any]] = [
    {  # a positive result, no Ct values
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "abc",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {  # a negative result
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "def",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "8426ba76-e595-4475-92a6-8a60be0eee20",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # a void result
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "hij",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "8d809bc1-2da6-42f2-9fc8-2eb6794f316f",
        FIELD_DATE_TESTED: "2020-05-10 07:30:00 UTC",
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # a 'limit of detection' result
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "limit of detection",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "klm",
        FIELD_ROOT_SAMPLE_ID: "MCM004",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "8e595a92-6798-4c93-8dc8-44f3ffb8bed3",
        FIELD_DATE_TESTED: "2020-05-10 07:30:00 UTC",
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # filtered_positive: True
        FIELD_COORDINATE: "E01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "nop",
        FIELD_ROOT_SAMPLE_ID: "MCM005",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "2184f5df-fdbb-4dcb-8bec-9f86450e0c82",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {  # filtered_positive: False
        FIELD_COORDINATE: "F01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "qrs",
        FIELD_ROOT_SAMPLE_ID: "MCM006",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "16dbdac1-ffe9-4d3d-92be-3a77c1e4c65e",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # filtered_positive: True
        FIELD_COORDINATE: "G01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "tuv",
        FIELD_ROOT_SAMPLE_ID: "MCM007",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "502a44a7-e4b4-4ad6-8e4c-3cfae35193d8",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {  # positive, with disallowed Root Sample ID
        FIELD_COORDINATE: "A02",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "wxy",
        FIELD_ROOT_SAMPLE_ID: "CBIQA_MCM008",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "d38f7f9a-6f17-4ff4-a2f9-b49505317340",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # positive, with disallowed Root Sample ID
        FIELD_COORDINATE: "D02",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "wxy",
        FIELD_ROOT_SAMPLE_ID: "QC0MCM008",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "fa9a36a9-f1de-4924-8a4f-bd72db911960",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # positive, with disallowed Root Sample ID
        FIELD_COORDINATE: "F02",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "wxy",
        FIELD_ROOT_SAMPLE_ID: "ZZA000MCM008",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "247144c3-b43b-489f-ad8d-78fab1417e91",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
]

SAMPLES_DIFFERENT_CENTRES = [
    {  # a positive result, no Ct values
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "abc",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {  # a negative result
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "test2",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "def",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "8426ba76-e595-4475-92a6-8a60be0eee20",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {  # a void result
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "hij",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_RNA_ID: "rna_1",
        FIELD_LH_SAMPLE_UUID: "8d809bc1-2da6-42f2-9fc8-2eb6794f316f",
        FIELD_DATE_TESTED: "2020-05-10 07:30:00 UTC",
        FIELD_FILTERED_POSITIVE: False,
    },
]

SAMPLES_DIFFERENT_PLATES: List[Dict[str, Any]] = [
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "abc",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_RNA_ID: "rna_1",
        FIELD_LAB_ID: "Lab 1",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "456",
        FIELD_COG_BARCODE: "def",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_RNA_ID: "rna_2",
        FIELD_LAB_ID: "Lab 2",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
]

SAMPLES_NO_DECLARATION: List[Dict[str, Any]] = [
    {
        FIELD_COORDINATE: "A01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "abc",
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
    {
        FIELD_COORDINATE: "B01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Negative",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "def",
        FIELD_ROOT_SAMPLE_ID: "MCM002",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {
        FIELD_COORDINATE: "C01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Void",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "hij",
        FIELD_ROOT_SAMPLE_ID: "MCM003",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: False,
    },
    {
        FIELD_COORDINATE: "D01",
        FIELD_SOURCE: "test1",
        FIELD_RESULT: "Positive",
        FIELD_PLATE_BARCODE: "123",
        FIELD_COG_BARCODE: "hij",
        FIELD_ROOT_SAMPLE_ID: "MCM010",
        FIELD_DATE_TESTED: DATE_TESTED_NOW,
        FIELD_FILTERED_POSITIVE: True,
    },
]

COG_UK_IDS: List[str] = ["cog_1", "cog_2", "cog_3"]

SAMPLES_FOR_MLWH_UPDATE: List[Dict[str, str]] = [
    {
        FIELD_ROOT_SAMPLE_ID: "root_1",
        FIELD_RNA_ID: "rna_1",
        FIELD_RESULT: "Positive",
        FIELD_COG_BARCODE: COG_UK_IDS[0],
    },
    {
        FIELD_ROOT_SAMPLE_ID: "root_2",
        FIELD_RNA_ID: "rna_2",
        FIELD_RESULT: "Positive",
        FIELD_COG_BARCODE: COG_UK_IDS[1],
    },
    {
        FIELD_ROOT_SAMPLE_ID: "root_1",
        FIELD_RNA_ID: "rna_3",
        FIELD_RESULT: "Positive",
        FIELD_COG_BARCODE: COG_UK_IDS[2],
    },
]

# this matches the positive sample in SAMPLES
MLWH_LH_SAMPLES: List[Dict[str, str]] = [
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "MCM001",
        MLWH_LH_SAMPLE_RNA_ID: "rna_1",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "MCM005",
        MLWH_LH_SAMPLE_RNA_ID: "rna_1",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "MCM006",
        MLWH_LH_SAMPLE_RNA_ID: "rna_1",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "MCM007",
        MLWH_LH_SAMPLE_RNA_ID: "rna_1",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
]

# more complex scenario for the mlwh-related tests
# two of the samples share a root sample id and result
MLWH_LH_SAMPLES_MULTIPLE: List[Dict[str, str]] = [
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "root_1",
        MLWH_LH_SAMPLE_RNA_ID: "rna_1",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "root_2",
        MLWH_LH_SAMPLE_RNA_ID: "rna_2",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
    {
        MLWH_LH_SAMPLE_ROOT_SAMPLE_ID: "root_1",
        MLWH_LH_SAMPLE_RNA_ID: "rna_3",
        MLWH_LH_SAMPLE_RESULT: "Positive",
    },
]

DART_MONGO_MERGED_SAMPLES: List[Dict[str, Any]] = [
    {  # Control sample
        "sample": None,
        "row": {
            FIELD_DART_DESTINATION_COORDINATE: "B01",
            FIELD_DART_DESTINATION_BARCODE: "d123",
            FIELD_DART_CONTROL: "positive",
            FIELD_DART_SOURCE_BARCODE: "123",
            FIELD_DART_SOURCE_COORDINATE: "A01",
            FIELD_DART_ROOT_SAMPLE_ID: "",
            FIELD_DART_RNA_ID: "",
            FIELD_DART_LAB_ID: "",
        },
    },
    {  # Non-control sample
        "sample": {
            FIELD_LH_SAMPLE_UUID: "8000a18d-43c6-44ff-9adb-257cb812ac77",
            FIELD_COORDINATE: "A02",
            FIELD_SOURCE: "test2",
            FIELD_RESULT: "Positive",
            FIELD_PLATE_BARCODE: "1234",
            FIELD_COG_BARCODE: "abcd",
            FIELD_ROOT_SAMPLE_ID: "MCM002",
            FIELD_RNA_ID: "rna_2",
            FIELD_LAB_ID: "AP",
        },
        "row": {
            FIELD_DART_DESTINATION_COORDINATE: "B02",
            FIELD_DART_DESTINATION_BARCODE: "d123",
            FIELD_DART_CONTROL: "",
            FIELD_DART_SOURCE_BARCODE: "1234",
            FIELD_DART_SOURCE_COORDINATE: "A02",
            FIELD_DART_ROOT_SAMPLE_ID: "MCM002",
            FIELD_DART_RNA_ID: "rna_2",
            FIELD_DART_LAB_ID: "AB",
        },
    },
]


def inject_lab_id(sample, lab_id):
    sample_copy = copy(sample)
    sample_copy[FIELD_LAB_ID] = lab_id
    return sample_copy


SAMPLES_WITH_LAB_ID = [inject_lab_id(sample, "Lab 1") for sample in SAMPLES]

MLWH_SAMPLE_STOCK_RESOURCE: Dict[str, Any] = {
    "sample": [
        {
            "id_sample_tmp": "1",
            "id_sample_lims": "1",
            "description": "root_1",
            "supplier_name": "cog_uk_id_1",
            "phenotype": "positive",
            "sanger_sample_id": "ss1",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "1",
        },
        {
            "id_sample_tmp": "2",
            "id_sample_lims": "2",
            "description": "root_2",
            "supplier_name": "cog_uk_id_2",
            "phenotype": "positive",
            "sanger_sample_id": "ss2",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "2",
        },
        {
            "id_sample_tmp": "3",
            "id_sample_lims": "3",
            "description": "root_1",
            "supplier_name": "cog_uk_id_3",
            "phenotype": "positive",
            "sanger_sample_id": "ss3",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "3",
        },
        {
            "id_sample_tmp": "4",
            "id_sample_lims": "4",
            "description": "root_3",
            "supplier_name": "cog_uk_id_4",
            "phenotype": "positive",
            "sanger_sample_id": "ss4",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "4",
        },
    ],
    "stock_resource": [
        {
            "id_stock_resource_tmp": "1",
            "id_sample_tmp": "1",
            "labware_human_barcode": "pb_1",
            "labware_machine_barcode": "pb_1",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "1",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "2",
            "id_sample_tmp": "2",
            "labware_human_barcode": "pb_2",
            "labware_machine_barcode": "pb_2",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "2",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "3",
            "id_sample_tmp": "3",
            "labware_human_barcode": "pb_3",
            "labware_machine_barcode": "pb_3",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "3",
            "labware_type": "well",
        },
        {
            "id_stock_resource_tmp": "4",
            "id_sample_tmp": "4",
            "labware_human_barcode": "pb_3",
            "labware_machine_barcode": "pb_3",
            "labware_coordinate": "A1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "id_study_tmp": "1",
            "id_lims": "SQSCP",
            "id_stock_resource_lims": "4",
            "labware_type": "well",
        },
    ],
    "study": [
        {
            "id_study_tmp": "1",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "id_study_lims": "1",
            "id_lims": "SQSCP",
        }
    ],
}

MLWH_SAMPLE_LIGHTHOUSE_SAMPLE: Dict[str, Any] = {
    "sample": [
        {
            "id_sample_tmp": "5",
            "id_sample_lims": "5",
            "description": "root_4",
            "supplier_name": "cog_uk_id_5",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss1",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "35000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "6",
            "id_sample_lims": "6",
            "description": "root_5",
            "supplier_name": "cog_uk_id_6",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss2",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "36000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "7",
            "id_sample_lims": "7",
            "description": "root_4",
            "supplier_name": "cog_uk_id_7",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss3",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "37000000000000000000000000000000",
        },
        {
            "id_sample_tmp": "8",
            "id_sample_lims": "8",
            "description": "root_3",
            "supplier_name": "cog_uk_id_8",
            "phenotype": "positive",
            "sanger_sample_id": "beck-ss4",
            "id_lims": "SQSCP",
            "last_updated": "2015-11-25 11:35:30",
            "recorded_at": "2015-11-25 11:35:30",
            "created": "2015-11-25 11:35:30",
            "uuid_sample_lims": "38000000000000000000000000000000",
        },
    ],
    "lighthouse_sample": [
        {
            "mongodb_id": "1",
            "root_sample_id": "root_4",
            "rna_id": "pb_4_A01",
            "plate_barcode": "pb_4",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "35000000000000000000000000000000",
        },
        {
            "mongodb_id": "2",
            "root_sample_id": "root_5",
            "rna_id": "pb_5_A01",
            "plate_barcode": "pb_5",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "36000000000000000000000000000000",
        },
        {
            "mongodb_id": "3",
            "root_sample_id": "root_4",
            "rna_id": "pb_6_A01",
            "plate_barcode": "pb_6",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "37000000000000000000000000000000",
        },
        {
            "mongodb_id": "4",
            "root_sample_id": "root_3",
            "rna_id": "pb_3_A01",
            "plate_barcode": "pb_3",
            "coordinate": "A1",
            "result": "Positive",
            "date_tested_string": "2020-10-24 22:30:22",
            "date_tested": datetime(2020, 10, 24, 22, 30, 22),
            "source": "test centre",
            "lab_id": "TC",
            "lh_sample_uuid": "38000000000000000000000000000000",
        },
    ],
}

EVENT_WH_DATA: Dict[str, Any] = {
    "subjects": [
        {"id": 1, "uuid": "1".encode("utf-8"), "friendly_name": "ss1", "subject_type_id": 1},
        {"id": 2, "uuid": "2".encode("utf-8"), "friendly_name": "ss2", "subject_type_id": 1},
        {"id": 3, "uuid": "5".encode("utf-8"), "friendly_name": "ss1-beck", "subject_type_id": 1},
        {"id": 4, "uuid": "6".encode("utf-8"), "friendly_name": "ss2-beck", "subject_type_id": 1},
    ],
    "roles": [
        {"id": 1, "event_id": 1, "subject_id": 1, "role_type_id": 1},
        {"id": 2, "event_id": 2, "subject_id": 2, "role_type_id": 1},
        {"id": 3, "event_id": 3, "subject_id": 3, "role_type_id": 1},
        {"id": 4, "event_id": 4, "subject_id": 4, "role_type_id": 1},
    ],
    "events": [
        {
            "id": 1,
            "lims_id": "SQSCP",
            "uuid": "1".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 2,
            "lims_id": "SQSCP",
            "uuid": "2".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 3,
            "lims_id": "SQSCP",
            "uuid": "3".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 4,
            "lims_id": "SQSCP",
            "uuid": "4".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
    ],
    "event_types": [
        {"id": 1, "key": EVENT_CHERRYPICK_LAYOUT_SET, "description": "stuff"},
        {"id": 2, "key": PLATE_EVENT_DESTINATION_CREATED, "description": "stuff"},
    ],
    "subject_types": [{"id": 1, "key": "sample", "description": "stuff"}],
    "role_types": [{"id": 1, "key": "sample", "description": "stuff"}],
}

SOURCE_PLATES: List[Dict[str, Any]] = [
    {
        FIELD_LH_SOURCE_PLATE_UUID: "a17c38cd-b2df-43a7-9896-582e7855b4cc",
        FIELD_BARCODE: "123",
        FIELD_LAB_ID: "Lab 1",
    },
    {
        FIELD_LH_SOURCE_PLATE_UUID: "785a87bd-6f5a-4340-b753-b05c0603fa5e",
        FIELD_BARCODE: "456",
        FIELD_LAB_ID: "Lab 2",
    },
    {
        FIELD_LH_SOURCE_PLATE_UUID: "2745095c-73da-4824-8af0-4c9d06055090",
        FIELD_BARCODE: "A123",
        FIELD_LAB_ID: "Lab 2",
    },
    {
        FIELD_LH_SOURCE_PLATE_UUID: "bba490a1-9858-49e5-a096-ee386f99fc38",
        FIELD_BARCODE: "A456",
        FIELD_LAB_ID: "Lab 3",
    },
]


def inject_uuids(sample):
    sample_copy = copy(sample)
    sample_copy[FIELD_LH_SOURCE_PLATE_UUID] = next(
        x[FIELD_LH_SOURCE_PLATE_UUID]
        for x in SOURCE_PLATES
        if x[FIELD_BARCODE] == sample_copy[FIELD_PLATE_BARCODE]
    )
    sample_copy[FIELD_LH_SAMPLE_UUID] = str(uuid4())
    return sample_copy


SAMPLES_WITH_UUIDS = [inject_uuids(sample) for sample in SAMPLES_WITH_LAB_ID]
