import urllib.parse
from datetime import datetime
from http import HTTPStatus
from typing import List
from unittest.mock import patch
from uuid import uuid4

import pytest
import responses
from flask import current_app

from lighthouse.constants.events import PE_BECKMAN_DESTINATION_CREATED, PE_BECKMAN_DESTINATION_FAILED
from lighthouse.constants.fields import (
    FIELD_BARCODE,
    FIELD_COG_BARCODE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
    FIELD_FILTERED_POSITIVE,
    FIELD_LH_SAMPLE_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_PLATE_BARCODE,
    FIELD_SS_BARCODE,
    FIELD_SS_CONTROL,
    FIELD_SS_CONTROL_TYPE,
    FIELD_SS_COORDINATE,
    FIELD_SS_LAB_ID,
    FIELD_SS_NAME,
    FIELD_SS_PHENOTYPE,
    FIELD_SS_SAMPLE_DESCRIPTION,
    FIELD_SS_SUPPLIER_NAME,
    FIELD_SS_UUID,
)
from lighthouse.constants.general import ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE
from lighthouse.helpers.plates import (
    add_controls_to_samples,
    centre_prefixes_for_samples,
    check_matching_sample_numbers,
    classify_samples_by_centre,
    construct_cherrypicking_plate_failed_message,
    create_cherrypicked_post_body,
    create_post_body,
    destination_plate_field_generators,
    equal_row_and_sample,
    find_sample_matching_row,
    find_samples,
    find_source_plates,
    format_plate,
    get_centre_prefix,
    get_source_plates_for_samples,
    get_unique_plate_barcodes,
    join_rows_with_samples,
    map_to_ss_columns,
    plate_exists_in_ss,
    query_for_cherrypicked_samples,
    query_for_source_plate_uuids,
    row_is_normal_sample,
    row_to_dict,
    rows_with_controls,
    rows_without_controls,
    source_plate_field_generators,
)

# ---------- test helpers ----------


@pytest.fixture
def mock_event_helpers():
    root = "lighthouse.helpers.plates"
    with patch(f"{root}.Beckman.get_robot_uuid") as mock_get_uuid:
        with patch(f"{root}.construct_robot_message_subject") as mock_construct_robot:
            with patch(f"{root}.construct_destination_plate_message_subject") as mock_construct_dest:
                with patch(f"{root}.construct_mongo_sample_message_subject") as mock_construct_sample:
                    with patch(f"{root}.construct_source_plate_message_subject") as mock_construct_source:
                        with patch(f"{root}.get_message_timestamp") as mock_get_timestamp:
                            yield (
                                mock_get_uuid,
                                mock_construct_robot,
                                mock_construct_dest,
                                mock_construct_sample,
                                mock_construct_source,
                                mock_get_timestamp,
                            )


def any_failure_type(app):
    return list(app.config["ROBOT_FAILURE_TYPES"].keys())[0]


# ---------- tests ----------


def test_classify_samples_by_centre(app, samples, mocked_responses):
    samples, _ = samples
    assert list(classify_samples_by_centre(samples).keys()) == ["centre_1", "centre_2"]
    assert len(classify_samples_by_centre(samples)["centre_1"]) == 11
    assert len(classify_samples_by_centre(samples)["centre_2"]) == 1


def test_centre_prefixes_for_samples(samples):
    samples, _ = samples
    actual = centre_prefixes_for_samples(samples)

    assert actual == ["centre_1", "centre_2"]


def test_centre_prefix(app, centres, mocked_responses):
    with app.app_context():
        assert get_centre_prefix("CENTRE_1") == "TC1"
        assert get_centre_prefix("centre_2") == "TC2"
        assert get_centre_prefix("CeNtRe_3") == "TC3"


def test_create_post_body(app, samples):
    with app.app_context():
        samples, _ = samples
        barcode = "12345"

        filtered_positive_samples = list(
            filter(
                lambda sample: sample.get(FIELD_FILTERED_POSITIVE, False)
                and sample[FIELD_PLATE_BARCODE] == "plate_123",
                samples,
            )
        )
        correct_body = {
            "data": {
                "type": "plates",
                "attributes": {
                    "barcode": "12345",
                    "purpose_uuid": current_app.config["SS_UUID_PLATE_PURPOSE"],
                    "study_uuid": current_app.config["SS_UUID_STUDY"],
                    "wells": {
                        "A01": {
                            "content": {
                                FIELD_SS_PHENOTYPE: "positive",
                                FIELD_SS_SUPPLIER_NAME: "abc",
                                FIELD_SS_SAMPLE_DESCRIPTION: "sample_001",
                                FIELD_SS_UUID: "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
                            }
                        },
                        "A02": {
                            "content": {
                                FIELD_SS_PHENOTYPE: "positive",
                                FIELD_SS_SUPPLIER_NAME: "def",
                                FIELD_SS_SAMPLE_DESCRIPTION: "sample_002",
                                FIELD_SS_UUID: "1a53e7b6-7ce8-4ebc-95c3-02dd64942531",
                            }
                        },
                        "E01": {
                            "content": {
                                FIELD_SS_PHENOTYPE: "positive",
                                FIELD_SS_SUPPLIER_NAME: "pqr",
                                FIELD_SS_SAMPLE_DESCRIPTION: "sample_101",
                                FIELD_SS_UUID: "2a53e7b6-7ce8-4ebc-95c3-02dd64942532",
                            }
                        },
                    },
                },
            }
        }

        assert create_post_body(barcode, filtered_positive_samples) == correct_body


def test_create_post_body_raises_without_cog_uk_id(app, samples):
    with app.app_context():
        samples, _ = samples
        barcode = "12345"

        filtered_positive_samples = list(
            filter(
                lambda sample: sample.get(FIELD_FILTERED_POSITIVE, False)
                and sample[FIELD_PLATE_BARCODE] == "plate_123",
                samples,
            )
        )

        # Remove a COG UK ID
        del filtered_positive_samples[0][FIELD_COG_BARCODE]

        with pytest.raises(KeyError):
            create_post_body(barcode, filtered_positive_samples)


class DartRow:
    def __init__(
        self,
        destination_barcode,
        destination_coordinate,
        source_barcode,
        source_coordinate,
        control,
        root_sample_id,
        rna_id,
        lab_id,
        lh_sample_uuid,
    ):
        setattr(self, FIELD_DART_DESTINATION_BARCODE, destination_barcode)
        setattr(self, FIELD_DART_DESTINATION_COORDINATE, destination_coordinate)
        setattr(self, FIELD_DART_SOURCE_BARCODE, source_barcode)
        setattr(self, FIELD_DART_SOURCE_COORDINATE, source_coordinate)
        setattr(self, FIELD_DART_CONTROL, control)
        setattr(self, FIELD_DART_ROOT_SAMPLE_ID, root_sample_id)
        setattr(self, FIELD_DART_RNA_ID, rna_id)
        setattr(self, FIELD_DART_LAB_ID, lab_id)
        setattr(self, FIELD_LH_SAMPLE_UUID, lh_sample_uuid)

    @classmethod
    def with_id_fields(
        self,
        destination_barcode,
        destination_coordinate,
        source_barcode,
        source_coordinate,
        control,
        root_sample_id,
        rna_id,
        lab_id,
    ):
        return self(
            destination_barcode,
            destination_coordinate,
            source_barcode,
            source_coordinate,
            control,
            root_sample_id,
            rna_id,
            lab_id,
            None,
        )

    @classmethod
    def with_sample_uuid(
        self, destination_barcode, destination_coordinate, source_barcode, source_coordinate, control, sample_uuid
    ):
        return self(
            destination_barcode,
            destination_coordinate,
            source_barcode,
            source_coordinate,
            control,
            None,
            None,
            None,
            sample_uuid,
        )


def test_query_for_cherrypicked_samples_generates_list():
    test = [
        DartRow.with_sample_uuid("DN1111", "A01", "DN2222", "C03", None, "UUID001"),
        DartRow.with_sample_uuid("DN3333", "A02", "DN2222", "C01", "positive", "UUID002"),
        DartRow.with_sample_uuid("DN1111", "A02", "DN2222", "C04", None, "UUID003"),
        DartRow.with_sample_uuid("DN3333", "A03", "DN2222", "C05", "negative", "UUID004"),
        DartRow.with_sample_uuid("DN1111", "A03", "DN2222", "C06", None, "UUID005"),
    ]

    assert query_for_cherrypicked_samples(test) == {
        "$or": [
            {FIELD_LH_SAMPLE_UUID: "UUID001"},
            {FIELD_LH_SAMPLE_UUID: "UUID003"},
            {FIELD_LH_SAMPLE_UUID: "UUID005"},
        ]
    }


def test_query_for_cherrypicked_samples_returns_empty_if_none():
    assert query_for_cherrypicked_samples([]) is None
    assert query_for_cherrypicked_samples(None) is None


def test_row_is_normal_sample_detects_if_sample_is_control():
    assert not row_is_normal_sample(
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", "positive", "sample_1", "plate1:A01", "ABC")
    )
    assert not row_is_normal_sample(
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", "negative", "sample_1", "plate1:A01", "ABC")
    )
    assert not row_is_normal_sample(
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", "control", "sample_1", "plate1:A01", "ABC")
    )
    assert row_is_normal_sample(
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", "", "sample_1", "plate1:A01", "ABC")
    )
    assert row_is_normal_sample(
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC")
    )


def test_rows_without_controls_filters_out_controls():
    test = [
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow.with_id_fields("DN3333", "A02", "DN2222", "C01", "positive", None, None, None),
        DartRow.with_id_fields("DN3333", "A03", "DN2222", "C05", "negative", None, None, None),
    ]

    assert rows_without_controls(test) == [test[0], test[1], test[2]]


def test_rows_with_controls_returns_controls():
    test = [
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow.with_id_fields("DN3333", "A02", "DN2222", "C01", "positive", None, None, None),
        DartRow.with_id_fields("DN3333", "A03", "DN2222", "C05", "negative", None, None, None),
    ]

    assert rows_with_controls(test) == [test[3], test[4]]


def test_equal_row_and_sample_compares_row_and_sample(samples):
    samples, _ = samples
    # Different UUID
    row = DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "not-the-uuid-you-are-looking-for")
    assert not equal_row_and_sample(row, samples[0])

    # Matching UUID
    row = DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "0a53e7b6-7ce8-4ebc-95c3-02dd64942531")
    assert equal_row_and_sample(row, samples[0])


def test_find_sample_matching_row(samples):
    samples, _ = samples
    row = DartRow.with_sample_uuid(
        "DN1111",
        "A01",
        "plate_123",
        "A01",
        None,
        "1a53e7b6-7ce8-4ebc-95c3-02dd64942531",
    )

    assert find_sample_matching_row(row, samples) == samples[1]


def test_find_sample_matching_row_returns_none_if_not_found(app, samples):
    samples, _ = samples
    row = DartRow.with_id_fields("DN1111", "A01", "plate_123", "A01", None, "MCM002", "rna_2", "Lab 3")

    assert find_sample_matching_row(row, samples) is None


def test_join_rows_with_samples(samples):
    samples, _ = samples
    rows = [
        DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "0a53e7b6-7ce8-4ebc-95c3-02dd64942531"),
        DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "1a53e7b6-7ce8-4ebc-95c3-02dd64942531"),
    ]

    assert join_rows_with_samples(rows, samples) == [
        {"row": row_to_dict(rows[0]), "sample": samples[0]},
        {"row": row_to_dict(rows[1]), "sample": samples[1]},
    ]


def test_join_rows_with_samples_joins_with_empty_sample_if_not_found(samples):
    samples, _ = samples
    rows = [
        DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "0a53e7b6-7ce8-4ebc-95c3-02dd64942531"),
        DartRow.with_sample_uuid("DN1111", "A01", "plate_123", "A01", None, "NOT-FOUND-UUID"),
    ]

    assert join_rows_with_samples(rows, samples) == [
        {"row": row_to_dict(rows[0]), "sample": samples[0]},
        {"row": row_to_dict(rows[1]), "sample": None},
    ]


def test_join_rows_with_samples_filters_out_controls(samples):
    samples, _ = samples
    rows = [
        DartRow.with_sample_uuid(
            "DN1111", "A01", "plate_123", "A01", "positive", "0a53e7b6-7ce8-4ebc-95c3-02dd64942531"
        ),
        DartRow.with_sample_uuid("DN1111", "A01", "plate_456", "A01", None, "243910d9-74bc-4da0-8f55-8606ed97b33a"),
    ]

    assert join_rows_with_samples(rows, samples) == [
        {"row": row_to_dict(rows[1]), "sample": samples[7]},
    ]


def test_add_controls_to_samples(samples):
    samples, _ = samples
    rows = [
        DartRow.with_id_fields("DN1111", "A01", "plate_123", "A01", "positive", "MCM001", "rna_1", "lab_1"),
        DartRow.with_id_fields("DN1111", "A01", "plate_123", "A01", "negative", "MCM002", "rna_2", "Lab 2"),
    ]

    samples_without_controls = [
        {"row": row_to_dict(rows[0]), "sample": samples[0]},
        {"row": row_to_dict(rows[1]), "sample": samples[1]},
    ]

    assert add_controls_to_samples(rows, samples_without_controls) == [
        {"row": row_to_dict(rows[0]), "sample": samples[0]},
        {"row": row_to_dict(rows[1]), "sample": samples[1]},
        {"row": row_to_dict(rows[0]), "sample": None},
        {"row": row_to_dict(rows[1]), "sample": None},
    ]


def test_check_matching_sample_numbers_returns_false_mismatch(samples):
    samples, _ = samples
    rows = [
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow.with_id_fields("DN1111", "A04", "DN2222", "C07", None, "sample_2", "plate1:A03", "ABC"),
        DartRow.with_id_fields("DN1111", "A05", "DN2222", "C08", None, "sample_2", "plate1:A03", "ABC"),
        DartRow.with_id_fields("DN3333", "A04", "DN2222", "C01", "positive", None, None, None),
        DartRow.with_id_fields("DN3333", "A04", "DN2222", "C01", "negative", None, None, None),
    ]

    result = check_matching_sample_numbers(rows, samples)
    assert result is False


def test_check_matching_sample_numbers_returns_true_match(samples):
    samples, _ = samples
    rows = [
        DartRow.with_id_fields("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A02", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A03", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A04", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A05", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow.with_id_fields("DN1111", "A06", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A07", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A08", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A09", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A10", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A11", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN1111", "A12", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow.with_id_fields("DN3333", "A04", "DN2222", "C01", "positive", None, None, None),
        DartRow.with_id_fields("DN3333", "A04", "DN2222", "C01", "negative", None, None, None),
    ]

    #  here we just need the same number of samples as there are rows without controls
    result = check_matching_sample_numbers(rows, samples)
    assert result is True


def test_map_to_ss_columns(app, dart_mongo_merged_samples):
    with app.app_context():
        correct_mapped_samples = [
            {
                FIELD_SS_CONTROL: True,
                FIELD_SS_CONTROL_TYPE: "positive",
                FIELD_SS_BARCODE: "d123",
                FIELD_SS_COORDINATE: "B01",
                FIELD_SS_SUPPLIER_NAME: "positive control: 123_A01",
            },
            {
                FIELD_SS_NAME: "rna_2",
                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                FIELD_SS_PHENOTYPE: "positive",
                FIELD_SS_SUPPLIER_NAME: "abcd",
                FIELD_SS_BARCODE: "d123",
                FIELD_SS_COORDINATE: "B02",
                FIELD_SS_UUID: "plate_3",
                FIELD_SS_LAB_ID: "AP",
            },
        ]
        result = map_to_ss_columns(dart_mongo_merged_samples)
        del result[0][FIELD_SS_UUID]
        assert result == correct_mapped_samples


def test_map_to_ss_columns_missing_value(app, dart_mongo_merged_samples):
    with app.app_context():
        del dart_mongo_merged_samples[1]["row"][FIELD_DART_DESTINATION_COORDINATE]
        with pytest.raises(KeyError):
            map_to_ss_columns(dart_mongo_merged_samples)


def test_create_cherrypicked_post_body(app):
    with app.app_context():
        barcode = "123"
        user_id = "my_user"
        mapped_samples = [
            {
                FIELD_SS_CONTROL: True,
                FIELD_SS_CONTROL_TYPE: "Positive",
                FIELD_SS_BARCODE: "123",
                FIELD_SS_COORDINATE: "B01",
                FIELD_SS_SUPPLIER_NAME: "Positive control: 123_B01",
                FIELD_SS_UUID: "71c71e3b-5c85-4d5c-831e-bee7bdd06c53",
            },
            {
                FIELD_SS_NAME: "rna_2",
                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                FIELD_SS_PHENOTYPE: "positive",
                FIELD_SS_SUPPLIER_NAME: "abcd",
                FIELD_SS_BARCODE: "123",
                FIELD_SS_COORDINATE: "B02",
                FIELD_SS_UUID: "8000a18d-43c6-44ff-9adb-257cb812ac77",
                FIELD_SS_LAB_ID: "AP",
            },
        ]

        robot_serial_number = "BKRB0001"

        source_plates = [
            {
                FIELD_BARCODE: "123",
                FIELD_LH_SOURCE_PLATE_UUID: "a17c38cd-b2df-43a7-9896-582e7855b4cc",
            },
            {
                FIELD_BARCODE: "456",
                FIELD_LH_SOURCE_PLATE_UUID: "785a87bd-6f5a-4340-b753-b05c0603fa5e",
            },
        ]

        correct_body = {
            "data": {
                "type": "plates",
                "attributes": {
                    "barcode": "123",
                    "purpose_uuid": current_app.config["SS_UUID_PLATE_PURPOSE_CHERRYPICKED"],
                    "study_uuid": current_app.config["SS_UUID_STUDY_CHERRYPICKED"],
                    "wells": {
                        "B01": {
                            "content": {
                                FIELD_SS_CONTROL: True,
                                FIELD_SS_CONTROL_TYPE: "positive",
                                FIELD_SS_SUPPLIER_NAME: "Positive control: 123_B01",
                                FIELD_SS_UUID: "71c71e3b-5c85-4d5c-831e-bee7bdd06c53",
                            }
                        },
                        "B02": {
                            "content": {
                                FIELD_SS_NAME: "rna_2",
                                FIELD_SS_PHENOTYPE: "positive",
                                FIELD_SS_SUPPLIER_NAME: "abcd",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                                FIELD_SS_UUID: "8000a18d-43c6-44ff-9adb-257cb812ac77",
                            }
                        },
                    },
                    "events": [
                        {
                            "event": {
                                "user_identifier": "my_user",
                                "event_type": PE_BECKMAN_DESTINATION_CREATED,
                                "subjects": [
                                    {
                                        "role_type": "robot",
                                        "subject_type": "robot",
                                        "friendly_name": "BKRB0001",
                                        "uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b",
                                    },
                                    {
                                        "role_type": "cherrypicking_source_labware",
                                        "subject_type": "plate",
                                        "friendly_name": "123",
                                        "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc",
                                    },
                                    {
                                        "role_type": "cherrypicking_source_labware",
                                        "subject_type": "plate",
                                        "friendly_name": "456",
                                        "uuid": "785a87bd-6f5a-4340-b753-b05c0603fa5e",
                                    },
                                    {
                                        "role_type": "control",
                                        "subject_type": "sample",
                                        "friendly_name": "Positive control: 123_B01",
                                        "uuid": "71c71e3b-5c85-4d5c-831e-bee7bdd06c53",
                                    },
                                    {
                                        "role_type": "sample",
                                        "subject_type": "sample",
                                        "friendly_name": "MCM002__rna_2__AP__positive",
                                        "uuid": "8000a18d-43c6-44ff-9adb-257cb812ac77",
                                    },
                                ],
                                "metadata": {},
                                "lims": app.config["RMQ_LIMS_ID"],
                            },
                        },
                    ],
                },
            },
        }

        assert (
            create_cherrypicked_post_body(user_id, barcode, mapped_samples, robot_serial_number, source_plates)
            == correct_body
        )


def test_find_samples_returns_none_if_no_query_provided(app):
    with app.app_context():
        assert find_samples(None) is None


def test_get_unique_plate_barcodes(app, samples):
    samples, _ = samples
    correct_barcodes = ["plate_123", "plate_456"]

    samples = [
        samples[0],
        samples[0],
        samples[7],
        samples[7],
    ]

    result = get_unique_plate_barcodes(samples)
    assert len(result) == len(correct_barcodes)
    for barcode in correct_barcodes:
        assert barcode in result


def test_query_for_source_plate_uuids(app):
    correct_query = {
        "$or": [
            {FIELD_BARCODE: "plate_123"},
            {FIELD_BARCODE: "plate_456"},
        ]
    }
    barcodes = ["plate_123", "plate_456"]

    assert query_for_source_plate_uuids(barcodes) == correct_query


def test_query_for_source_plate_uuids_returns_none(app):
    barcodes: List[str] = []

    assert query_for_source_plate_uuids(barcodes) is None
    assert query_for_source_plate_uuids(None) is None


def test_find_source_plates_returns_none(app):
    assert find_source_plates(None) is None


def test_get_source_plates_for_samples(app, samples, source_plates):
    samples, _ = samples
    with app.app_context():
        samples = [
            samples[0],
            samples[0],
            samples[7],
            samples[7],
        ]

        results = get_source_plates_for_samples(samples)
        if results:
            assert len(results) == 2
            for result in results:
                source_plate = next(plate for plate in source_plates if result[FIELD_BARCODE] == plate[FIELD_BARCODE])
                assert source_plate is not None
                assert source_plate[FIELD_LH_SOURCE_PLATE_UUID] == result[FIELD_LH_SOURCE_PLATE_UUID]
        else:
            raise AssertionError()


# ---------- construct_cherrypicking_plate_failed_message tests ----------


def test_construct_cherrypicking_plate_failed_message_unknown_robot_fails(mock_event_helpers):
    mock_get_uuid, _, _, _, _, _ = mock_event_helpers
    mock_get_uuid.return_value = None
    errors, message = construct_cherrypicking_plate_failed_message("plate_1", "test_user", "BKRB0001", "robot_crashed")

    assert message is None
    assert len(errors) == 1
    msg = "An unexpected error occurred attempting to construct the cherrypicking plate failed " "event message"
    assert msg in errors[0]


def test_construct_cherrypicking_plate_failed_message_dart_fetch_failure(app, mock_event_helpers):
    (
        mock_get_uuid,
        mock_robot_subject,
        mock_dest_subject,
        _,
        _,
        mock_get_timestamp,
    ) = mock_event_helpers
    test_robot_uuid = "test robot uuid"
    mock_get_uuid.return_value = test_robot_uuid
    test_robot_subject = {"test robot": "this is a robot"}
    mock_robot_subject.return_value = test_robot_subject
    test_dest_subject = {"test dest plate": "this is a destination plate"}
    mock_dest_subject.return_value = test_dest_subject
    test_timestamp = datetime.now()
    mock_get_timestamp.return_value = test_timestamp
    with app.app_context():
        test_uuid = uuid4()
        with patch("lighthouse.helpers.plates.uuid4", return_value=test_uuid):
            with patch(
                "lighthouse.helpers.plates.find_dart_source_samples_rows",
                side_effect=Exception(),
            ):
                with patch("lighthouse.helpers.plates.Message") as mock_message:
                    test_barcode = "plate_1"
                    test_user = "test_user_id"
                    test_robot_serial_number = "12345"
                    test_failure_type = any_failure_type(app)
                    errors, _ = construct_cherrypicking_plate_failed_message(
                        test_barcode, test_user, test_robot_serial_number, test_failure_type
                    )

                    # assert expected calls
                    mock_robot_subject.assert_called_with(test_robot_serial_number, test_robot_uuid)
                    mock_dest_subject.assert_called_with(test_barcode)

                    # assert expected return values
                    assert len(errors) == 1
                    assert (
                        "There was an error connecting to DART for destination plate "
                        f"'{test_barcode}'. As this may be due to the failure you are reporting, "
                        "a destination plate failure has still been recorded, but without sample "
                        "and source plate information"
                    ) in errors[0]
                    args, _ = mock_message.call_args
                    message_content = args[0]

                    assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                    event = message_content["event"]
                    assert event["uuid"] == str(test_uuid)
                    assert event["event_type"] == PE_BECKMAN_DESTINATION_FAILED
                    assert event["occured_at"] == test_timestamp
                    assert event["user_identifier"] == test_user

                    subjects = event["subjects"]
                    assert len(subjects) == 2
                    assert test_robot_subject in subjects  # robot subject
                    assert test_dest_subject in subjects  # destination plate subject

                    metadata = event["metadata"]
                    assert metadata == {"failure_type": test_failure_type}


def test_construct_cherrypicking_plate_failed_message_none_dart_samples(app, mock_event_helpers):
    (
        mock_get_uuid,
        mock_robot_subject,
        mock_dest_subject,
        _,
        _,
        mock_get_timestamp,
    ) = mock_event_helpers
    test_robot_uuid = "test robot uuid"
    mock_get_uuid.return_value = test_robot_uuid
    test_robot_subject = {"test robot": "this is a robot"}
    mock_robot_subject.return_value = test_robot_subject
    test_dest_subject = {"test dest plate": "this is a destination plate"}
    mock_dest_subject.return_value = test_dest_subject
    test_timestamp = datetime.now()
    mock_get_timestamp.return_value = test_timestamp
    with app.app_context():
        test_uuid = uuid4()
        with patch("lighthouse.helpers.plates.uuid4", return_value=test_uuid):
            with patch("lighthouse.helpers.plates.find_dart_source_samples_rows", return_value=None):
                with patch("lighthouse.helpers.plates.Message") as mock_message:
                    test_barcode = "plate_1"
                    test_user = "test_user_id"
                    test_robot_serial_number = "12345"
                    test_failure_type = any_failure_type(app)
                    errors, _ = construct_cherrypicking_plate_failed_message(
                        test_barcode, test_user, test_robot_serial_number, test_failure_type
                    )

                    # assert expected calls
                    mock_robot_subject.assert_called_with(test_robot_serial_number, test_robot_uuid)
                    mock_dest_subject.assert_called_with(test_barcode)

                    # assert expected return values
                    assert len(errors) == 1
                    assert (
                        "There was an error connecting to DART for destination plate "
                        f"'{test_barcode}'. As this may be due to the failure you are reporting, "
                        "a destination plate failure has still been recorded, but without sample "
                        "and source plate information"
                    ) in errors[0]
                    args, _ = mock_message.call_args
                    message_content = args[0]

                    assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                    event = message_content["event"]
                    assert event["uuid"] == str(test_uuid)
                    assert event["event_type"] == PE_BECKMAN_DESTINATION_FAILED
                    assert event["occured_at"] == test_timestamp
                    assert event["user_identifier"] == test_user

                    subjects = event["subjects"]
                    assert len(subjects) == 2
                    assert test_robot_subject in subjects  # robot subject
                    assert test_dest_subject in subjects  # destination plate subject

                    metadata = event["metadata"]
                    assert metadata == {"failure_type": test_failure_type}


def test_construct_cherrypicking_plate_failed_message_empty_dart_samples(app, mock_event_helpers):
    (
        mock_get_uuid,
        mock_robot_subject,
        mock_dest_subject,
        _,
        _,
        mock_get_timestamp,
    ) = mock_event_helpers
    test_robot_uuid = "test robot uuid"
    mock_get_uuid.return_value = test_robot_uuid
    test_robot_subject = {"test robot": "this is a robot"}
    mock_robot_subject.return_value = test_robot_subject
    test_dest_subject = {"test dest plate": "this is a destination plate"}
    mock_dest_subject.return_value = test_dest_subject
    test_timestamp = datetime.now()
    mock_get_timestamp.return_value = test_timestamp
    with app.app_context():
        test_uuid = uuid4()
        with patch("lighthouse.helpers.plates.uuid4", return_value=test_uuid):
            with patch("lighthouse.helpers.plates.find_dart_source_samples_rows", return_value=[]):
                with patch("lighthouse.helpers.plates.Message") as mock_message:
                    test_barcode = "plate_1"
                    test_user = "test_user_id"
                    test_robot_serial_number = "12345"
                    test_failure_type = any_failure_type(app)
                    errors, _ = construct_cherrypicking_plate_failed_message(
                        test_barcode, test_user, test_robot_serial_number, test_failure_type
                    )

                    # assert expected calls
                    mock_robot_subject.assert_called_with(test_robot_serial_number, test_robot_uuid)
                    mock_dest_subject.assert_called_with(test_barcode)

                    # assert expected return values
                    assert len(errors) == 1
                    assert (
                        f"No samples were found in DART for destination plate '{test_barcode}'. "
                        "As this may be due to the failure you are reporting, a destination plate "
                        "failure has still been recorded, but without sample and source plate "
                        "information"
                    ) in errors[0]
                    args, _ = mock_message.call_args
                    message_content = args[0]

                    assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                    event = message_content["event"]
                    assert event["uuid"] == str(test_uuid)
                    assert event["event_type"] == PE_BECKMAN_DESTINATION_FAILED
                    assert event["occured_at"] == test_timestamp
                    assert event["user_identifier"] == test_user

                    subjects = event["subjects"]
                    assert len(subjects) == 2
                    assert test_robot_subject in subjects  # robot subject
                    assert test_dest_subject in subjects  # destination plate subject

                    metadata = event["metadata"]
                    assert metadata == {"failure_type": test_failure_type}


def test_construct_cherrypicking_plate_failed_message_mongo_samples_fetch_failure(
    app, dart_samples, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.samples") as samples_collection:
            samples_collection.find.side_effect = Exception()
            errors, message = construct_cherrypicking_plate_failed_message(
                "des_plate_1", "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            msg = "An unexpected error occurred attempting to construct the cherrypicking plate " "failed event message"
            assert msg in errors[0]


def test_construct_cherrypicking_plate_failed_message_none_mongo_samples(app, dart_samples, mock_event_helpers):
    with app.app_context():
        with patch("lighthouse.helpers.plates.query_for_cherrypicked_samples", return_value=None):
            barcode = "des_plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert f"No sample data found in Mongo matching DART samples in plate '{barcode}'" in errors


def test_construct_cherrypicking_plate_failed_message_samples_not_in_mongo(app, dart_samples, mock_event_helpers):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.samples") as samples_collection:
            samples_collection.find.return_value = []
            barcode = "des_plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert f"Mismatch in destination and source sample data for plate '{barcode}'" in errors


def test_construct_cherrypicking_plate_failed_message_mongo_source_plates_fetch_failure(
    app, dart_samples, samples, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.source_plates") as source_plates_collection:
            source_plates_collection.find.side_effect = Exception()
            errors, message = construct_cherrypicking_plate_failed_message(
                "des_plate_1", "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            msg = "An unexpected error occurred attempting to construct the cherrypicking plate " "failed event message"
            assert msg in errors[0]


def test_construct_cherrypicking_plate_failed_message_none_mongo_source_plates(
    app, dart_samples, samples, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.query_for_source_plate_uuids", return_value=None):
            barcode = "des_plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert f"No source plate data found in Mongo for DART samples in plate '{barcode}'" in errors


def test_construct_cherrypicking_plate_failed_message_source_plates_not_in_mongo(
    app, dart_samples, samples, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.source_plates") as source_plates_collection:
            source_plates_collection.find.return_value = []
            barcode = "des_plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert f"No source plate data found in Mongo for DART samples in plate '{barcode}'" in errors


def test_format_plate_source(app, plates_lookup_without_samples, plates_lookup_with_samples):
    with app.app_context():
        assert (
            format_plate("plate_123", exclude_props=["pickable_samples"]) == plates_lookup_without_samples["plate_123"]
        )
        assert format_plate("plate_123") == plates_lookup_with_samples["plate_123"]
        assert format_plate(barcode="plate_123", plate_type=ARG_TYPE_SOURCE) == plates_lookup_with_samples["plate_123"]


def test_format_plate_destination(app, mocked_responses):
    plate_barcode = "dest_123"

    with app.app_context():
        ss_url = f"{app.config['SS_URL']}/api/v2/labware"
        mocked_responses.add(
            responses.GET,
            f"{ss_url}?{urllib.parse.quote('filter[barcode]')}={plate_barcode}",
            json={"data": ["barcode exists!"]},
            status=HTTPStatus.OK,
        )
        response = {
            "plate_barcode": "dest_123",
            "plate_exists": True,
        }
        assert format_plate(barcode=plate_barcode, plate_type=ARG_TYPE_DESTINATION) == response


def test_source_plate_field_generators(app, plates_lookup_with_samples):
    with app.app_context():
        assert source_plate_field_generators("plate_123")["plate_barcode"] is not None
        plate = plates_lookup_with_samples["plate_123"]
        assert source_plate_field_generators("plate_123")["plate_barcode"]() == plate["plate_barcode"]


def test_destination_plate_field_generators(app):
    plate_barcode = "dest_123"
    with app.app_context():
        assert ("plate_barcode", "plate_exists") == tuple(
            destination_plate_field_generators(barcode=plate_barcode).keys()
        )
        assert destination_plate_field_generators(barcode=plate_barcode)["plate_barcode"]() == plate_barcode
        with patch("lighthouse.helpers.plates.plate_exists_in_ss", side_effect=(True, False)):
            assert destination_plate_field_generators(barcode=plate_barcode)["plate_exists"]() is True
            assert destination_plate_field_generators(barcode=plate_barcode)["plate_exists"]() is False


def test_plate_exists_in_ss(app, mocked_responses):
    with app.app_context():
        ss_url = f"{app.config['SS_URL']}/api/v2/labware"
        first_plate_barcode = "plate_123"
        second_plate_barcode = "plate_456"

        mocked_responses.add(
            responses.GET,
            f"{ss_url}?{urllib.parse.quote('filter[barcode]')}={first_plate_barcode}",
            json={"data": ["barcode exists!"]},
            status=HTTPStatus.OK,
        )
        mocked_responses.add(
            responses.GET,
            f"{ss_url}?{urllib.parse.quote('filter[barcode]')}={second_plate_barcode}",
            json={"data": []},
            status=HTTPStatus.OK,
        )

        assert plate_exists_in_ss(barcode=first_plate_barcode) is True
        assert plate_exists_in_ss(barcode=second_plate_barcode) is False


# def test_construct_cherrypicking_plate_failed_message_success(
#     app, dart_samples, samples, source_plates, mock_event_helpers
# ):
#     (
#         mock_get_uuid,
#         mock_robot_subject,
#         mock_dest_subject,
#         mock_sample_subject,
#         mock_source_subject,
#         mock_get_timestamp,
#     ) = mock_event_helpers
#     test_robot_uuid = "test robot uuid"
#     mock_get_uuid.return_value = test_robot_uuid
#     test_robot_subject = {"test robot": "this is a robot"}
#     mock_robot_subject.return_value = test_robot_subject
#     test_dest_subject = {"test dest plate": "this is a destination plate"}
#     mock_dest_subject.return_value = test_dest_subject
#     test_sample_subject = {"test sample": "this is a sample subject"}
#     mock_sample_subject.return_value = test_sample_subject
#     test_source_subject = {"test source plate": "this is a source plate subject"}
#     mock_source_subject.return_value = test_source_subject
#     test_timestamp = datetime.now()
#     mock_get_timestamp.return_value = test_timestamp
#     with app.app_context():
#         samples, _ = samples
#         test_uuid = uuid4()
#         with patch("lighthouse.helpers.plates.uuid4", return_value=test_uuid):
#             with patch("lighthouse.helpers.plates.Message") as mock_message:
#                 test_barcode = "des_plate_1"
#                 test_user = "test_user_id"
#                 test_robot_serial_number = "12345"
#                 test_failure_type = any_failure_type(app)
#                 errors, _ = construct_cherrypicking_plate_failed_message(
#                     test_barcode, test_user, test_robot_serial_number, test_failure_type
#                 )

#                 # assert expected calls
#                 mock_robot_subject.assert_called_with(test_robot_serial_number, test_robot_uuid)
#                 mock_dest_subject.assert_called_with(test_barcode)
#                 mock_source_subject.assert_called_with("plate_abc", "bba490a1-9858-49e5-a096-ee386f99fc38")

#                 root_sample_ids = ["sample_001", "sample_002"]
#                 expected_samples = list(filter(lambda x: x[FIELD_ROOT_SAMPLE_ID] in root_sample_ids, samples))
#                 # remove the microsecond comparing
#                 for sample in expected_samples:
#                     sample.update({FIELD_DATE_TESTED: sample[FIELD_DATE_TESTED].replace(microsecond=0)})
#                 assert len(root_sample_ids) == len(expected_samples)  # sanity check
#                 for args, _ in mock_sample_subject.call_args_list:
#                     # remove the microsecond before comparing
#                     args[0][FIELD_DATE_TESTED] = args[0][FIELD_DATE_TESTED].replace(microsecond=0)
#                     print(args[0])
#                     print(expected_samples)
#                     assert args[0] in expected_samples

#                 # assert expected return values
#                 assert len(errors) == 0
#                 args, _ = mock_message.call_args
#                 message_content = args[0]

#                 assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

#                 event = message_content["event"]
#                 assert event["uuid"] == str(test_uuid)
#                 assert event["event_type"] == PLATE_EVENT_DESTINATION_FAILED
#                 assert event["occured_at"] == test_timestamp
#                 assert event["user_identifier"] == test_user

#                 subjects = event["subjects"]
#                 assert len(subjects) == 6
#                 assert test_robot_subject in subjects  # robot subject
#                 assert test_dest_subject in subjects  # destination plate subject
#                 assert {  # control sample subject
#                     "role_type": "control",
#                     "subject_type": "sample",
#                     "friendly_name": "positive control: 789_B01",
#                     "uuid": str(test_uuid),
#                 } in subjects
#                 assert subjects.count(test_sample_subject) == 2  # sample subjects
#                 assert test_source_subject in subjects  # source plate subject

#                 metadata = event["metadata"]
#                 assert metadata == {"failure_type": test_failure_type}
