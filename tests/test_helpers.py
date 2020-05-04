from http import HTTPStatus

import responses  # type: ignore
from flask import current_app

from lighthouse.constants import FIELD_COG_BARCODE
from lighthouse.helpers import add_cog_barcodes, create_post_body, get_centre_prefix, get_samples


def test_add_cog_barcodes(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_HOST']}:{current_app.config['BARACODA_PORT']}"
            "/barcodes/TS1/new"
        )

        # remove the cog_barcode key and value from the samples fixture before testing
        map(lambda sample: sample.pop(FIELD_COG_BARCODE), samples)

        cog_barcodes = ("123", "456", "789")

        # update the 'cog_barcode' tuple when adding more samples to the fixture data
        assert len(cog_barcodes) == len(samples)

        for cog_barcode in cog_barcodes:
            mocked_responses.add(
                responses.POST,
                baracoda_url,
                body=f'{{"barcode": "{cog_barcode}"}}',
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
                    "plate_purpose_uuid": current_app.config["SS_UUID_PLATE_PURPOSE"],
                    "study_uuid": current_app.config["SS_UUID_STUDY"],
                    "wells_content": {
                        "A01": {
                            "phenotype": "positive",
                            "supplier_name": "abc",
                            "sample_description": "MCM001",
                        },
                        "B01": {
                            "phenotype": "negative",
                            "supplier_name": "def",
                            "sample_description": "MCM002",
                        },
                        "C01": {
                            "phenotype": "void",
                            "supplier_name": "hij",
                            "sample_description": "MCM003",
                        },
                    },
                },
            }
        }

        assert create_post_body(barcode, samples) == correct_body


def test_get_samples(app, samples):
    with app.app_context():
        assert len(get_samples("123")) == 3
