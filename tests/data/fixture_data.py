from typing import Dict, List

from lighthouse.constants import FIELD_COG_BARCODE

CENTRES: List[Dict[str, str]] = [
    {"name": "test1", "prefix": "TS1"},
    {"name": "test2", "prefix": "TS2"},
    {"name": "test3", "prefix": "TS3"},
]

SAMPLES_DECLARATIONS: List[Dict[str, str]] = [
    {
        "root_sample_id": "MCM001",
        "value_in_sequencing": "Yes",
        "declared_at": "2013-04-04T10:29:13",
    },
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": "2013-04-04T10:29:13"},
    {"root_sample_id": "MCM003", "value_in_sequencing": "No", "declared_at": "2013-04-05T10:29:13"},
    {
        "root_sample_id": "MCM003",
        "value_in_sequencing": "Yes",
        "declared_at": "2013-04-06T10:29:13",
    },
]

MAX_SAMPLES = 100
LOTS_OF_SAMPLES: List[Dict[str, str]] = [{
        "coordinate": "A01",
        "source": "test1",
        "Result": "Positive",
        "plate_barcode": "123",
        FIELD_COG_BARCODE: "abc",
        "Root Sample ID": f"MCM00{i}",
} for i in range(0, MAX_SAMPLES)]

LOTS_OF_SAMPLES_DECLARATIONS: List[Dict[str, str]] = [{
        "root_sample_id": f"MCM00{i}",
        "value_in_sequencing": "Yes",
        "declared_at": "2013-04-04T10:29:13",
} for i in range(0, MAX_SAMPLES)]


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
