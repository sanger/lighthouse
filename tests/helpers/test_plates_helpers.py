import json
from functools import partial
from http import HTTPStatus

import pytest
from unittest.mock import patch
import responses  # type: ignore
from flask import current_app
from datetime import datetime
from uuid import uuid4
from lighthouse.constants import (
    FIELD_COG_BARCODE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
    FIELD_LAB_ID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_BARCODE,
    FIELD_LH_SOURCE_PLATE_UUID,
    MLWH_LH_SAMPLE_COG_UK_ID,
    MLWH_LH_SAMPLE_ROOT_SAMPLE_ID,
    PLATE_EVENT_DESTINATION_CREATED,
    PLATE_EVENT_DESTINATION_FAILED,
    FIELD_SS_LAB_ID,
    FIELD_SS_NAME,
    FIELD_SS_RESULT,
    FIELD_SS_SAMPLE_DESCRIPTION,
)
from lighthouse.helpers.plates import (
    UnmatchedSampleError,
    add_cog_barcodes,
    add_controls_to_samples,
    check_matching_sample_numbers,
    create_cherrypicked_post_body,
    create_post_body,
    equal_row_and_sample,
    find_sample_matching_row,
    find_samples,
    get_centre_prefix,
    get_positive_samples,
    count_positive_samples,
    join_rows_with_samples,
    map_to_ss_columns,
    query_for_cherrypicked_samples,
    row_is_normal_sample,
    row_to_dict,
    rows_with_controls,
    rows_without_controls,
    update_mlwh_with_cog_uk_ids,
    get_unique_plate_barcodes,
    query_for_source_plate_uuids,
    get_source_plates_for_samples,
    construct_cherrypicking_plate_failed_message,
    find_source_plates,
)
from requests import ConnectionError
from sqlalchemy.exc import OperationalError


# ---------- test helpers ----------


@pytest.fixture
def mock_event_helpers():
    root = "lighthouse.helpers.plates"
    with patch(f"{root}.get_robot_uuid") as mock_get_uuid:
        with patch(f"{root}.construct_robot_message_subject") as mock_construct_robot:
            with patch(
                f"{root}.construct_destination_plate_message_subject"
            ) as mock_construct_dest:
                with patch(
                    f"{root}.construct_mongo_sample_message_subject"
                ) as mock_construct_sample:
                    with patch(
                        f"{root}.construct_source_plate_message_subject"
                    ) as mock_construct_source:
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
    return list(app.config["BECKMAN_FAILURE_TYPES"].keys())[0]


# ---------- tests ----------


def test_add_cog_barcodes(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_URL']}"
            f"/barcodes_group/TS1/new?count={len(samples)}"
        )

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789", "101", "131", "161", "192", "222")

        # update the 'cog_barcode' tuple when adding more samples to the fixture data
        assert len(cog_barcodes) == len(samples)

        mocked_responses.add(
            responses.POST,
            baracoda_url,
            body=json.dumps({"barcodes_group": {"barcodes": cog_barcodes}}),
            status=HTTPStatus.CREATED,
        )

        add_cog_barcodes(samples)

        for idx, sample in enumerate(samples):
            assert FIELD_COG_BARCODE in sample.keys()
            assert sample[FIELD_COG_BARCODE] == cog_barcodes[idx]


def test_add_cog_barcodes_will_retry_if_fail(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_URL']}/"
            f"barcodes_group/TS1/new?count={len(samples)}"
        )

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789", "101", "131", "161", "192", "222")

        # update the 'cog_barcode' tuple when adding more samples to the fixture data
        assert len(cog_barcodes) == len(samples)

        mocked_responses.add(
            responses.POST,
            baracoda_url,
            json={"errors": ["Some error from baracoda"]},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        with pytest.raises(Exception):
            add_cog_barcodes(samples)

        assert len(mocked_responses.calls) == app.config["BARACODA_RETRY_ATTEMPTS"]


def test_add_cog_barcodes_will_retry_if_exception(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_URL']}/"
            f"barcodes_group/TS1/new?count={len(samples)}"
        )

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789", "101", "131", "161", "192", "222")

        # update the 'cog_barcode' tuple when adding more samples to the fixture data
        assert len(cog_barcodes) == len(samples)

        mocked_responses.add(
            responses.POST,
            baracoda_url,
            body=ConnectionError("Some error"),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        with pytest.raises(ConnectionError):
            add_cog_barcodes(samples)

        assert len(mocked_responses.calls) == app.config["BARACODA_RETRY_ATTEMPTS"]


def test_add_cog_barcodes_will_not_raise_error_if_success_after_retry(
    app, centres, samples, mocked_responses
):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_URL']}/"
            f"barcodes_group/TS1/new?count={len(samples)}"
        )

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789", "101", "131", "161", "192", "222")

        # update the 'cog_barcode' tuple when adding more samples to the fixture data
        assert len(cog_barcodes) == len(samples)

        def request_callback(request, data):
            data["calls"] = data["calls"] + 1

            if data["calls"] == app.config["BARACODA_RETRY_ATTEMPTS"]:
                return (
                    HTTPStatus.CREATED,
                    {},
                    json.dumps({"barcodes_group": {"barcodes": cog_barcodes}}),
                )
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {},
                json.dumps({"errors": ["Some error from baracoda"]}),
            )

        mocked_responses.add_callback(
            responses.POST,
            baracoda_url,
            callback=partial(request_callback, data={"calls": 0}),
            content_type="application/json",
        )

        # This should not raise any error
        add_cog_barcodes(samples)

        assert len(mocked_responses.calls) == app.config["BARACODA_RETRY_ATTEMPTS"]


def test_centre_prefix(app, centres, mocked_responses):
    with app.app_context():
        assert get_centre_prefix("TEST1") == "TS1"
        assert get_centre_prefix("test2") == "TS2"
        assert get_centre_prefix("TeSt3") == "TS3"


def test_create_post_body(app, samples):
    with app.app_context():
        barcode = "12345"

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
                                "phenotype": "positive",
                                "supplier_name": "abc",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM001",
                            }
                        },
                        "B01": {
                            "content": {
                                "phenotype": "negative",
                                "supplier_name": "def",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                            }
                        },
                        "C01": {
                            "content": {
                                "phenotype": "void",
                                "supplier_name": "hij",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM003",
                            }
                        },
                        "D01": {
                            "content": {
                                "phenotype": "limit of detection",
                                "supplier_name": "klm",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM004",
                            }
                        },
                        "E01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "nop",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM005",
                            }
                        },
                        "F01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "qrs",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM006",
                            }
                        },
                        "G01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "tuv",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM007",
                            }
                        },
                        "A02": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "wxy",
                                FIELD_SS_SAMPLE_DESCRIPTION: "CBIQA_MCM008",
                            }
                        },
                    },
                },
            }
        }

        assert create_post_body(barcode, samples) == correct_body


def test_get_positive_samples(app, samples):
    with app.app_context():
        assert len(get_positive_samples("123")) == 3


def test_get_positive_samples_different_plates(app, samples_different_plates):
    with app.app_context():
        assert len(get_positive_samples("123")) == 1


def test_count_positive_samples(app, samples):
    with app.app_context():
        assert count_positive_samples("123") == 3


def test_count_positive_samples_different_plates(app, samples_different_plates):
    with app.app_context():
        assert count_positive_samples("123") == 1


def test_update_mlwh_with_cog_uk_ids(
    app, mlwh_lh_samples_multiple, samples_for_mlwh_update, cog_uk_ids, mlwh_sql_engine
):
    with app.app_context():
        # check that the samples already exist in the MLWH db but do not have cog uk ids
        before = retrieve_samples_cursor(app.config, mlwh_sql_engine)
        before_count = 0
        for row in before:
            before_count += 1
            assert row[MLWH_LH_SAMPLE_COG_UK_ID] is None

        assert before_count == 3

        # run the function we're testing
        update_mlwh_with_cog_uk_ids(samples_for_mlwh_update)

        # check that the same samples in the MLWH now have the correct cog uk ids
        after = retrieve_samples_cursor(app.config, mlwh_sql_engine)
        after_count = 0
        after_cog_uk_ids = set()
        for row in after:
            after_count += 1
            after_cog_uk_ids.add(row[MLWH_LH_SAMPLE_COG_UK_ID])

        assert after_count == before_count
        assert after_cog_uk_ids == set(cog_uk_ids)


def test_update_mlwh_with_cog_uk_ids_connection_fails(
    app, mlwh_lh_samples_multiple, samples_for_mlwh_update
):
    with app.app_context():
        # mock this out to cause an exception
        app.config["WAREHOUSES_RW_CONN_STRING"] = "notarealconnectionstring"

        with pytest.raises(OperationalError):
            update_mlwh_with_cog_uk_ids(samples_for_mlwh_update)


def test_update_mlwh_with_cog_uk_ids_field_missing(app, mlwh_lh_samples_multiple):
    with app.app_context():
        samples = [
            {
                FIELD_ROOT_SAMPLE_ID: "root_1",
                FIELD_RNA_ID: "rna_1",
                FIELD_RESULT: "positive"
                # no cog uk id
            }
        ]

        with pytest.raises(KeyError):
            update_mlwh_with_cog_uk_ids(samples)


def test_update_mlwh_with_cog_uk_ids_unmatched_sample(
    app, mlwh_lh_samples_multiple, samples_for_mlwh_update, cog_uk_ids, mlwh_sql_engine
):
    #  Should - update the ones it can, but then log a detailed error, and throw an exception
    with app.app_context():
        # add sample that doesn't match one in the MLWH
        samples_for_mlwh_update.append(
            {
                FIELD_ROOT_SAMPLE_ID: "root_253",
                FIELD_RNA_ID: "rna_253",
                FIELD_RESULT: "positive",
                FIELD_COG_BARCODE: "cog_253",
            }
        )

        # check that the expected number of samples are in the MLWH db but do not have cog uk ids
        before = retrieve_samples_cursor(app.config, mlwh_sql_engine)
        before_count = 0
        for row in before:
            before_count += 1
            assert row[MLWH_LH_SAMPLE_COG_UK_ID] is None

        assert before_count == 3

        # check the function raises an exception due to the unmatched sample
        with pytest.raises(UnmatchedSampleError):
            update_mlwh_with_cog_uk_ids(samples_for_mlwh_update)

        # check that the matched samples in the MLWH now have the correct cog uk ids
        after = retrieve_samples_cursor(app.config, mlwh_sql_engine)
        after_count = 0
        after_cog_uk_ids = set()
        for row in after:
            after_count += 1
            after_cog_uk_ids.add(row[MLWH_LH_SAMPLE_COG_UK_ID])

        assert after_count == before_count
        assert after_cog_uk_ids == set(cog_uk_ids)


def retrieve_samples_cursor(config, mlwh_sql_engine):
    with mlwh_sql_engine.connect() as connection:
        results = connection.execute(
            f"SELECT {MLWH_LH_SAMPLE_ROOT_SAMPLE_ID}, {MLWH_LH_SAMPLE_COG_UK_ID} "
            "FROM lighthouse_sample"
        )

    return results


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
    ):

        setattr(self, FIELD_DART_DESTINATION_BARCODE, destination_barcode)
        setattr(self, FIELD_DART_DESTINATION_COORDINATE, destination_coordinate)
        setattr(self, FIELD_DART_SOURCE_BARCODE, source_barcode)
        setattr(self, FIELD_DART_SOURCE_COORDINATE, source_coordinate)
        setattr(self, FIELD_DART_CONTROL, control)
        setattr(self, FIELD_DART_ROOT_SAMPLE_ID, root_sample_id)
        setattr(self, FIELD_DART_RNA_ID, rna_id)
        setattr(self, FIELD_DART_LAB_ID, lab_id)


def test_query_for_cherrypicked_samples_generates_list(app):
    test = [
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN3333", "A02", "DN2222", "C01", "positive", None, None, None),
        DartRow("DN3333", "A03", "DN2222", "C05", "negative", None, None, None),
    ]

    assert query_for_cherrypicked_samples(test) == {
        "$or": [
            {
                FIELD_ROOT_SAMPLE_ID: "sample_1",
                FIELD_RNA_ID: "plate1:A01",
                FIELD_LAB_ID: "ABC",
                FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
            },
            {
                FIELD_ROOT_SAMPLE_ID: "sample_1",
                FIELD_RNA_ID: "plate1:A02",
                FIELD_LAB_ID: "ABC",
                FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
            },
            {
                FIELD_ROOT_SAMPLE_ID: "sample_2",
                FIELD_RNA_ID: "plate1:A03",
                FIELD_LAB_ID: "ABC",
                FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
            },
        ]
    }


def test_query_for_cherrypicked_samples_returns_empty_if_none(app):
    assert query_for_cherrypicked_samples([]) is None
    assert query_for_cherrypicked_samples(None) is None


def test_row_is_normal_sample_detects_if_sample_is_control(app):
    assert not row_is_normal_sample(
        DartRow("DN1111", "A01", "DN2222", "C03", "positive", "sample_1", "plate1:A01", "ABC")
    )
    assert not row_is_normal_sample(
        DartRow("DN1111", "A01", "DN2222", "C03", "negative", "sample_1", "plate1:A01", "ABC")
    )
    assert not row_is_normal_sample(
        DartRow("DN1111", "A01", "DN2222", "C03", "control", "sample_1", "plate1:A01", "ABC")
    )
    assert row_is_normal_sample(
        DartRow("DN1111", "A01", "DN2222", "C03", "", "sample_1", "plate1:A01", "ABC")
    )
    assert row_is_normal_sample(
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC")
    )


def test_rows_without_controls_filters_out_controls(app):
    test = [
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN3333", "A02", "DN2222", "C01", "positive", None, None, None),
        DartRow("DN3333", "A03", "DN2222", "C05", "negative", None, None, None),
    ]

    assert rows_without_controls(test) == [test[0], test[1], test[2]]


def test_rows_with_controls_returns_controls(app):
    test = [
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN3333", "A02", "DN2222", "C01", "positive", None, None, None),
        DartRow("DN3333", "A03", "DN2222", "C05", "negative", None, None, None),
    ]

    assert rows_with_controls(test) == [test[3], test[4]]


def test_equal_row_and_sample_compares_row_and_sample(app, samples_different_plates):
    # Different root sample id
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_1", "Lab 1")
    assert not equal_row_and_sample(row, samples_different_plates[0])

    # Different rna id
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM001", "rna_3", "Lab 1")
    assert not equal_row_and_sample(row, samples_different_plates[0])

    # Different lab id
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM001", "rna_1", "Lab 2")
    assert not equal_row_and_sample(row, samples_different_plates[0])

    # Same 3 values (root sample id, rna id, lab id)
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM001", "rna_1", "Lab 1")
    assert equal_row_and_sample(row, samples_different_plates[0])


def test_find_sample_matching_row(app, samples_different_plates):
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_2", "Lab 2")

    assert find_sample_matching_row(row, samples_different_plates) == samples_different_plates[1]


def test_find_sample_matching_row_returns_none_if_not_found(app, samples_different_plates):
    row = DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_2", "Lab 3")

    assert find_sample_matching_row(row, samples_different_plates) is None


def test_join_rows_with_samples(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "123", "A01", None, "MCM001", "rna_1", "Lab 1"),
        DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_2", "Lab 2"),
    ]

    assert join_rows_with_samples(rows, samples_different_plates) == [
        {"row": row_to_dict(rows[0]), "sample": samples_different_plates[0]},
        {"row": row_to_dict(rows[1]), "sample": samples_different_plates[1]},
    ]


def test_join_rows_with_samples_joins_with_empty_sample_if_not_found(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "123", "A01", None, "MCM001", "rna_1", "Lab 1"),
        DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_3", "Lab 2"),
    ]

    assert join_rows_with_samples(rows, samples_different_plates) == [
        {"row": row_to_dict(rows[0]), "sample": samples_different_plates[0]},
        {"row": row_to_dict(rows[1]), "sample": None},
    ]


def test_join_rows_with_samples_filters_out_controls(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "123", "A01", "positive", "MCM001", "rna_1", "Lab 1"),
        DartRow("DN1111", "A01", "123", "A01", None, "MCM002", "rna_2", "Lab 2"),
    ]

    assert join_rows_with_samples(rows, samples_different_plates) == [
        {"row": row_to_dict(rows[1]), "sample": samples_different_plates[1]},
    ]


def test_add_controls_to_samples(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "123", "A01", "positive", "MCM001", "rna_1", "Lab 1"),
        DartRow("DN1111", "A01", "123", "A01", "negative", "MCM002", "rna_2", "Lab 2"),
    ]

    samples_without_controls = [
        {"row": row_to_dict(rows[0]), "sample": samples_different_plates[0]},
        {"row": row_to_dict(rows[1]), "sample": samples_different_plates[1]},
    ]

    assert add_controls_to_samples(rows, samples_without_controls) == [
        {"row": row_to_dict(rows[0]), "sample": samples_different_plates[0]},
        {"row": row_to_dict(rows[1]), "sample": samples_different_plates[1]},
        {"row": row_to_dict(rows[0]), "sample": None},
        {"row": row_to_dict(rows[1]), "sample": None},
    ]


def test_check_matching_sample_numbers_returns_false_mismatch(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow("DN1111", "A03", "DN2222", "C06", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN1111", "A04", "DN2222", "C07", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN1111", "A05", "DN2222", "C08", None, "sample_2", "plate1:A03", "ABC"),
        DartRow("DN3333", "A04", "DN2222", "C01", "positive", None, None, None),
        DartRow("DN3333", "A04", "DN2222", "C01", "negative", None, None, None),
    ]

    result = check_matching_sample_numbers(rows, samples_different_plates)
    assert result is False


def test_check_matching_sample_numbers_returns_true_match(app, samples_different_plates):
    rows = [
        DartRow("DN1111", "A01", "DN2222", "C03", None, "sample_1", "plate1:A01", "ABC"),
        DartRow("DN1111", "A02", "DN2222", "C04", None, "sample_1", "plate1:A02", "ABC"),
        DartRow("DN3333", "A04", "DN2222", "C01", "positive", None, None, None),
        DartRow("DN3333", "A04", "DN2222", "C01", "negative", None, None, None),
    ]

    result = check_matching_sample_numbers(rows, samples_different_plates)
    assert result is True


def test_map_to_ss_columns(app, dart_mongo_merged_samples):
    with app.app_context():
        correct_mapped_samples = [
            {
                "control": True,
                "control_type": "positive",
                "barcode": "d123",
                "coordinate": "B01",
                "supplier_name": "positive control: 123_A01",
            },
            {
                FIELD_SS_NAME: "rna_2",
                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                "phenotype": "positive",
                "supplier_name": "abcd",
                "barcode": "d123",
                "coordinate": "B02",
                "uuid": "8000a18d-43c6-44ff-9adb-257cb812ac77",
                FIELD_SS_LAB_ID: "AP",
                FIELD_SS_RESULT: "Positive",
            },
        ]
        result = map_to_ss_columns(dart_mongo_merged_samples)
        del result[0]["uuid"]
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
                "control": True,
                "control_type": "Positive",
                "barcode": "123",
                "coordinate": "B01",
                "supplier_name": "Positive control: 123_B01",
                "uuid": "71c71e3b-5c85-4d5c-831e-bee7bdd06c53",
            },
            {
                FIELD_SS_NAME: "rna_2",
                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                "phenotype": "positive",
                "supplier_name": "abcd",
                "barcode": "123",
                "coordinate": "B02",
                "uuid": "8000a18d-43c6-44ff-9adb-257cb812ac77",
                FIELD_SS_LAB_ID: "AP",
                FIELD_SS_RESULT: "Positive",
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
                                "control": True,
                                "control_type": "Positive",
                                "supplier_name": "Positive control: 123_B01",
                                "uuid": "71c71e3b-5c85-4d5c-831e-bee7bdd06c53",
                            }
                        },
                        "B02": {
                            "content": {
                                FIELD_SS_NAME: "rna_2",
                                "phenotype": "positive",
                                "supplier_name": "abcd",
                                FIELD_SS_SAMPLE_DESCRIPTION: "MCM002",
                                "uuid": "8000a18d-43c6-44ff-9adb-257cb812ac77",
                            }
                        },
                    },
                    "events": [
                        {
                            "event": {
                                "user_identifier": "my_user",
                                "event_type": PLATE_EVENT_DESTINATION_CREATED,
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
                                        "friendly_name": "MCM002__rna_2__AP__Positive",
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
            create_cherrypicked_post_body(
                user_id, barcode, mapped_samples, robot_serial_number, source_plates
            )
            == correct_body
        )


def test_find_samples_returns_none_if_no_query_provided(app):
    with app.app_context():
        assert find_samples(None) is None


def test_get_unique_plate_barcodes(app, samples_different_plates):
    correct_barcodes = ["123", "456"]

    samples = [
        samples_different_plates[0],
        samples_different_plates[0],
        samples_different_plates[1],
        samples_different_plates[1],
    ]

    result = get_unique_plate_barcodes(samples)
    assert len(result) == len(correct_barcodes)
    for barcode in correct_barcodes:
        assert barcode in result


def test_query_for_source_plate_uuids(app):
    correct_query = {
        "$or": [
            {FIELD_BARCODE: "123"},
            {FIELD_BARCODE: "456"},
        ]
    }
    barcodes = ["123", "456"]

    assert query_for_source_plate_uuids(barcodes) == correct_query


def test_query_for_source_plate_uuids_returns_none(app):
    barcodes = []

    assert query_for_source_plate_uuids(barcodes) is None
    assert query_for_source_plate_uuids(None) is None


def test_find_source_plates_returns_none(app):
    assert find_source_plates(None) is None


def test_get_source_plates_for_samples(app, samples_different_plates, source_plates):
    with app.app_context():
        samples = [
            samples_different_plates[0],
            samples_different_plates[0],
            samples_different_plates[1],
            samples_different_plates[1],
        ]

        results = get_source_plates_for_samples(samples)
        assert len(results) == 2
        for result in results:
            source_plate = next(
                plate for plate in source_plates if result[FIELD_BARCODE] == plate[FIELD_BARCODE]
            )
            assert source_plate is not None
            assert source_plate[FIELD_LH_SOURCE_PLATE_UUID] == result[FIELD_LH_SOURCE_PLATE_UUID]


# ---------- construct_cherrypicking_plate_failed_message tests ----------


def test_construct_cherrypicking_plate_failed_message_unknown_robot_fails(mock_event_helpers):
    mock_get_uuid, _, _, _, _, _ = mock_event_helpers
    mock_get_uuid.return_value = None
    errors, message = construct_cherrypicking_plate_failed_message(
        "plate_1", "test_user", "BKRB0001", "robot_crashed"
    )

    assert message is None
    assert len(errors) == 1
    assert "An unexpected error occurred attempting to construct the cherrypicking plate "
    "failed event message" in errors


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
                side_effect=Exception("Boom!"),
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
                    assert event["event_type"] == PLATE_EVENT_DESTINATION_FAILED
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
            with patch(
                "lighthouse.helpers.plates.find_dart_source_samples_rows", return_value=None
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
                    assert event["event_type"] == PLATE_EVENT_DESTINATION_FAILED
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
                    assert event["event_type"] == PLATE_EVENT_DESTINATION_FAILED
                    assert event["occured_at"] == test_timestamp
                    assert event["user_identifier"] == test_user

                    subjects = event["subjects"]
                    assert len(subjects) == 2
                    assert test_robot_subject in subjects  # robot subject
                    assert test_dest_subject in subjects  # destination plate subject

                    metadata = event["metadata"]
                    assert metadata == {"failure_type": test_failure_type}


def test_construct_cherrypicking_plate_failed_message_mongo_samples_fetch_failure(
    app, dart_samples_for_bp_test, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.samples") as samples_collection:
            samples_collection.find.side_effect = Exception("Boom!")
            errors, message = construct_cherrypicking_plate_failed_message(
                "plate_1", "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert "An unexpected error occurred attempting to construct the cherrypicking plate "
            "failed event message" in errors


def test_construct_cherrypicking_plate_failed_message_none_mongo_samples(
    app, dart_samples_for_bp_test, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.query_for_cherrypicked_samples", return_value=None):
            barcode = "plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert (
                f"No sample data found in Mongo matching DART samples in plate '{barcode}'"
                in errors
            )


def test_construct_cherrypicking_plate_failed_message_samples_not_in_mongo(
    app, dart_samples_for_bp_test, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.app.data.driver.db.samples") as samples_collection:
            samples_collection.find.return_value = []
            barcode = "plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert f"Mismatch in destination and source sample data for plate '{barcode}'" in errors


def test_construct_cherrypicking_plate_failed_message_mongo_source_plates_fetch_failure(
    app, dart_samples_for_bp_test, samples_with_uuids, mock_event_helpers
):
    with app.app_context():
        with patch(
            "lighthouse.helpers.plates.app.data.driver.db.source_plates"
        ) as source_plates_collection:
            source_plates_collection.find.side_effect = Exception("Boom!")
            errors, message = construct_cherrypicking_plate_failed_message(
                "plate_1", "test_user", "12345", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert "An unexpected error occurred attempting to construct the cherrypicking plate "
            "failed event message" in errors


def test_construct_cherrypicking_plate_failed_message_none_mongo_source_plates(
    app, dart_samples_for_bp_test, samples_with_uuids, mock_event_helpers
):
    with app.app_context():
        with patch("lighthouse.helpers.plates.query_for_source_plate_uuids", return_value=None):
            barcode = "plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert (
                f"No source plate data found in Mongo for DART samples in plate '{barcode}'"
                in errors
            )


def test_construct_cherrypicking_plate_failed_message_source_plates_not_in_mongo(
    app, dart_samples_for_bp_test, samples_with_uuids, mock_event_helpers
):
    with app.app_context():
        with patch(
            "lighthouse.helpers.plates.app.data.driver.db.source_plates"
        ) as source_plates_collection:
            source_plates_collection.find.return_value = []
            barcode = "plate_1"
            errors, message = construct_cherrypicking_plate_failed_message(
                barcode, "test_user", "BKRB0001", "robot_crashed"
            )

            assert message is None
            assert len(errors) == 1
            assert (
                f"No source plate data found in Mongo for DART samples in plate '{barcode}'"
                in errors
            )


def test_construct_cherrypicking_plate_failed_message_success(
    app, dart_samples_for_bp_test, samples_with_uuids, source_plates, mock_event_helpers
):
    (
        mock_get_uuid,
        mock_robot_subject,
        mock_dest_subject,
        mock_sample_subject,
        mock_source_subject,
        mock_get_timestamp,
    ) = mock_event_helpers
    test_robot_uuid = "test robot uuid"
    mock_get_uuid.return_value = test_robot_uuid
    test_robot_subject = {"test robot": "this is a robot"}
    mock_robot_subject.return_value = test_robot_subject
    test_dest_subject = {"test dest plate": "this is a destination plate"}
    mock_dest_subject.return_value = test_dest_subject
    test_sample_subject = {"test sample": "this is a sample subject"}
    mock_sample_subject.return_value = test_sample_subject
    test_source_subject = {"test source plate": "this is a source plate subject"}
    mock_source_subject.return_value = test_source_subject
    test_timestamp = datetime.now()
    mock_get_timestamp.return_value = test_timestamp
    with app.app_context():
        test_uuid = uuid4()
        with patch("lighthouse.helpers.plates.uuid4", return_value=test_uuid):
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
                mock_source_subject.assert_called_with(
                    "123", "a17c38cd-b2df-43a7-9896-582e7855b4cc"
                )

                root_sample_ids = ["MCM001", "MCM006"]
                expected_samples = list(
                    filter(lambda x: x[FIELD_ROOT_SAMPLE_ID] in root_sample_ids, samples_with_uuids)
                )
                assert len(root_sample_ids) == len(expected_samples)  # sanity check
                for args, _ in mock_sample_subject.call_args_list:
                    assert args[0] in expected_samples

                # assert expected return values
                assert len(errors) == 0
                args, _ = mock_message.call_args
                message_content = args[0]

                assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                event = message_content["event"]
                assert event["uuid"] == str(test_uuid)
                assert event["event_type"] == PLATE_EVENT_DESTINATION_FAILED
                assert event["occured_at"] == test_timestamp
                assert event["user_identifier"] == test_user

                subjects = event["subjects"]
                assert len(subjects) == 6
                assert test_robot_subject in subjects  # robot subject
                assert test_dest_subject in subjects  # destination plate subject
                assert {  # control sample subject
                    "role_type": "control",
                    "subject_type": "sample",
                    "friendly_name": "positive control: 789_B01",
                    "uuid": str(test_uuid),
                } in subjects
                assert subjects.count(test_sample_subject) == 2  # sample subjects
                assert test_source_subject in subjects  # source plate subject

                metadata = event["metadata"]
                assert metadata == {"failure_type": test_failure_type}
