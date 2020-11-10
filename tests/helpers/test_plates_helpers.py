import json
from http import HTTPStatus

import responses  # type: ignore
from flask import current_app

import pytest

import sqlalchemy  # type: ignore
from sqlalchemy.exc import OperationalError

from lighthouse.constants import (
    FIELD_COG_BARCODE,
    FIELD_ROOT_SAMPLE_ID,
    MLWH_LH_SAMPLE_ROOT_SAMPLE_ID,
    MLWH_LH_SAMPLE_COG_UK_ID,
    FIELD_RNA_ID,
    FIELD_RESULT,
)
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    create_post_body,
    get_centre_prefix,
    get_samples,
    get_positive_samples,
    update_mlwh_with_cog_uk_ids,
    UnmatchedSampleError,
)


def test_add_cog_barcodes(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = f"http://{current_app.config['BARACODA_URL']}/barcodes_group/TS1/new?count={len(samples)}"

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
                                "sample_description": "MCM001",
                            }
                        },
                        "B01": {
                            "content": {
                                "phenotype": "negative",
                                "supplier_name": "def",
                                "sample_description": "MCM002",
                            }
                        },
                        "C01": {
                            "content": {
                                "phenotype": "void",
                                "supplier_name": "hij",
                                "sample_description": "MCM003",
                            }
                        },
                        "D01": {
                            "content": {
                                "phenotype": "limit of detection",
                                "supplier_name": "klm",
                                "sample_description": "MCM004",
                            }
                        },
                        "E01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "nop",
                                "sample_description": "MCM005",
                            }
                        },
                        "F01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "qrs",
                                "sample_description": "MCM006",
                            }
                        },
                        "G01": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "tuv",
                                "sample_description": "MCM007",
                            }
                        },
                        "A02": {
                            "content": {
                                "phenotype": "positive",
                                "supplier_name": "wxy",
                                "sample_description": "CBIQA_MCM008",
                            }
                        },
                    },
                },
            }
        }

        assert create_post_body(barcode, samples) == correct_body


def test_get_samples(app, samples):
    with app.app_context():
        assert len(get_samples("123")) == 8


def test_get_positive_samples(app, samples):
    with app.app_context():
        assert len(get_positive_samples("123")) == 3


def test_get_positive_samples_different_plates(app, samples_different_plates):
    with app.app_context():
        assert len(get_positive_samples("123")) == 1


def test_update_mlwh_with_cog_uk_ids(
    app, mlwh_lh_samples_multiple, samples_for_mlwh_update, cog_uk_ids, sql_engine
):
    with app.app_context():
        # check that the samples already exist in the MLWH db but do not have cog uk ids
        before = retrieve_samples_cursor(app.config, sql_engine)
        before_count = 0
        for row in before:
            before_count += 1
            assert row[MLWH_LH_SAMPLE_COG_UK_ID] is None

        assert before_count == 3

        # run the function we're testing
        update_mlwh_with_cog_uk_ids(samples_for_mlwh_update)

        # check that the same samples in the MLWH now have the correct cog uk ids
        after = retrieve_samples_cursor(app.config, sql_engine)
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
        app.config["MLWH_RW_CONN_STRING"] = "notarealconnectionstring"

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
    app, mlwh_lh_samples_multiple, samples_for_mlwh_update, cog_uk_ids, sql_engine
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
        before = retrieve_samples_cursor(app.config, sql_engine)
        before_count = 0
        for row in before:
            before_count += 1
            assert row[MLWH_LH_SAMPLE_COG_UK_ID] is None

        assert before_count == 3

        # check the function raises an exception due to the unmatched sample
        with pytest.raises(UnmatchedSampleError):
            update_mlwh_with_cog_uk_ids(samples_for_mlwh_update)

        # check that the matched samples in the MLWH now have the correct cog uk ids
        after = retrieve_samples_cursor(app.config, sql_engine)
        after_count = 0
        after_cog_uk_ids = set()
        for row in after:
            after_count += 1
            after_cog_uk_ids.add(row[MLWH_LH_SAMPLE_COG_UK_ID])

        assert after_count == before_count
        assert after_cog_uk_ids == set(cog_uk_ids)


def retrieve_samples_cursor(config, sql_engine):
    with sql_engine.connect() as connection:
        results = connection.execute(
            f"SELECT {MLWH_LH_SAMPLE_ROOT_SAMPLE_ID}, {MLWH_LH_SAMPLE_COG_UK_ID} from lighthouse_sample"
        )

    return results
