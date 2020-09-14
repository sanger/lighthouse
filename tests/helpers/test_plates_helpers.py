import json
from http import HTTPStatus

import responses  # type: ignore
from flask import current_app

from lighthouse.constants import (
    FIELD_COG_BARCODE,
    FIELD_ROOT_SAMPLE_ID
)
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    create_post_body,
    get_centre_prefix,
    get_samples,
    get_positive_samples,
    update_mlwh_with_cog_uk_ids
)


def test_add_cog_barcodes(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = f"http://{current_app.config['BARACODA_URL']}/barcodes_group/TS1/new?count=3"

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789")

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
                    },
                },
            }
        }

        assert create_post_body(barcode, samples) == correct_body

def test_get_samples(app, samples):
    with app.app_context():
        assert len(get_samples("123")) == 3

def test_get_positive_samples(app, samples):
    with app.app_context():
        assert len(get_positive_samples("123")) == 1

def test_update_mlwh_with_cog_uk_ids(app):
    with app.app_context():
        samples = [
            {
                FIELD_ROOT_SAMPLE_ID: 'test1',
                FIELD_COG_BARCODE: 'test2'
            },
            {
                FIELD_ROOT_SAMPLE_ID: 'test3',
                FIELD_COG_BARCODE: 'test4'
            }
        ]
        update_mlwh_with_cog_uk_ids(samples)