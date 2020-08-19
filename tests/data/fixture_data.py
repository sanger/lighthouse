from typing import Dict, List, Any
from datetime import datetime
from lighthouse.constants import FIELD_COG_BARCODE

CENTRES: List[Dict[str, str]] = [
    {"name": "test1", "prefix": "TS1"},
    {"name": "test2", "prefix": "TS2"},
    {"name": "test3", "prefix": "TS3"},
]

FIRST_TIMESTAMP = datetime(2013, 4, 4, 10, 29, 13)
SECOND_TIMESTAMP = datetime(2013, 4, 5, 10, 29, 13)
THIRD_TIMESTAMP = datetime(2013, 4, 6, 10, 29, 13)


SAMPLES_DECLARATIONS: List[Dict[str, Any]] = [
    {"root_sample_id": "MCM001", "value_in_sequencing": "Yes", "declared_at": FIRST_TIMESTAMP,},
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": FIRST_TIMESTAMP},
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": SECOND_TIMESTAMP},
    {"root_sample_id": "MCM003", "value_in_sequencing": "Yes", "declared_at": THIRD_TIMESTAMP,},
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
        "coordinate": "A01",
        "source": "test1",
        "Result": "Positive",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "abc",
        "Root Sample ID": f"MCM00{i}",
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

SAMPLES: List[Dict[str, str]] = [
    {
        "coordinate": "A01",
        "source": "test1",
        "Result": "Positive",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "abc",
        "Root Sample ID": "MCM001",
    },
    {
        "coordinate": "B01",
        "source": "test1",
        "Result": "Negative",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "def",
        "Root Sample ID": "MCM002",
    },
    {
        "coordinate": "C01",
        "source": "test1",
        "Result": "Void",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "hij",
        "Root Sample ID": "MCM003",
    },
]

SAMPLES_NO_DECLARATION: List[Dict[str, str]] = [
    {
        "coordinate": "A01",
        "source": "test1",
        "Result": "Positive",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "abc",
        "Root Sample ID": "MCM001",
    },
    {
        "coordinate": "B01",
        "source": "test1",
        "Result": "Negative",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "def",
        "Root Sample ID": "MCM002",
    },
    {
        "coordinate": "C01",
        "source": "test1",
        "Result": "Void",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "hij",
        "Root Sample ID": "MCM003",
    },
    {
        "coordinate": "D01",
        "source": "test1",
        "Result": "Positive",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "hij",
        "Root Sample ID": "MCM010",
    },
]
