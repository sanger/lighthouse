from http import HTTPStatus

import responses
from flask import current_app

from lighthouse.helpers import add_cog_barcodes, create_post_body, get_centre_prefix, get_samples


def test_add_cog_barcodes(app, centres, samples, mocked_responses):
    with app.app_context():
        baracoda_url = (
            f"http://{current_app.config['BARACODA_HOST']}:{current_app.config['BARACODA_PORT']}"
            "/barcodes/TS1/new"
        )

        cog_barcodes = ("123", "456")
        for cog_barcode in cog_barcodes:
            mocked_responses.add(
                responses.POST,
                baracoda_url,
                body=f'{{"barcode": "{cog_barcode}"}}',
                status=HTTPStatus.CREATED,
            )

        add_cog_barcodes(samples)

        for idx, sample in enumerate(samples):
            assert "cog_barcode" in sample.keys()
            assert sample["cog_barcode"] == cog_barcodes[idx]


def test_centre_prefix(app, centres, mocked_responses):
    with app.app_context():
        assert get_centre_prefix("TEST1") == "TS1"
        assert get_centre_prefix("test2") == "TS2"
        assert get_centre_prefix("TeSt3") == "TS3"


def test_create_post_body(samples):
    barcode = "12345"
    correct_body = {
        "data": {
            "type": "plates",
            "attributes": {
                "barcode": "12345",
                "plate_purpose_uuid": "11111",
                "study_uuid": "11111",
                "wells_content": {
                    "A01": {"phenotype": "A phenotype"},
                    "B01": {"phenotype": "A phenotype"},
                },
            },
        }
    }

    assert create_post_body(barcode, samples) == correct_body


def test_get_samples(app, samples):
    with app.app_context():
        assert len(get_samples("123")) == 2
