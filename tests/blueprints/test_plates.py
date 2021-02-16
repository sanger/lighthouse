from http import HTTPStatus
from unittest.mock import patch

import responses

from lighthouse.constants.error_messages import (
    ERROR_ADD_COG_BARCODES,
    ERROR_PLATES_CREATE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)


def test_post_plates_endpoint_successful(app, client, samples, mocked_responses, mlwh_lh_samples):
    with patch("lighthouse.blueprints.plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = {"barcode": "plate_123"}
        mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.OK)

        response = client.post("/plates/new", json=body)
        assert response.status_code == HTTPStatus.OK
        assert response.json == {"data": {"plate_barcode": "plate_123", "centre": "TC1", "number_of_positives": 2}}


def test_post_plates_endpoint_no_barcode_in_request(app, client, samples):
    response = client.post("/plates/new", json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode' in body"]}


def test_post_plates_endpoint_no_positive_samples(app, client):
    response = client.post("/plates/new", json={"barcode": "qwerty"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["No samples for this barcode: qwerty"]}


def test_post_plates_endpoint_add_cog_barcodes_failed(app, client, samples, centres, mocked_responses):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TC1/new?count=2"

    mocked_responses.add(responses.POST, baracoda_url, status=HTTPStatus.BAD_REQUEST)

    response = client.post("/plates/new", json={"barcode": "plate_123"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"{ERROR_PLATES_CREATE} {ERROR_ADD_COG_BARCODES} plate_123"]}


def test_post_plates_endpoint_ss_failure(app, client, samples, mocked_responses):
    with patch("lighthouse.blueprints.plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = {"errors": ["The barcode 'plate_123' is not a recognised format."]}
        mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.UNPROCESSABLE_ENTITY)

        response = client.post("/plates/new", json={"barcode": "plate_123"})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == {"errors": ["The barcode 'plate_123' is not a recognised format."]}


def test_post_plates_mlwh_update_failure(app, client, samples, mocked_responses):
    with patch("lighthouse.blueprints.plates.add_cog_barcodes", return_value="TC1"):
        with patch("lighthouse.blueprints.plates.update_mlwh_with_cog_uk_ids", side_effect=Exception()):
            ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

            body = {"barcode": "plate_123"}
            mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.OK)

            response = client.post("/plates/new", json={"barcode": "plate_123"})

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [ERROR_UPDATE_MLWH_WITH_COG_UK_IDS]}


def test_get_plates_endpoint_successful(app, client, samples, mocked_responses):
    response = client.get("/plates?barcodes[]=plate_123&barcodes[]=456", content_type="application/json")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "plates": [
            {"plate_barcode": "plate_123", "plate_map": True, "number_of_positives": 2},
            {"plate_barcode": "456", "plate_map": False, "number_of_positives": None},
        ]
    }


def test_get_plates_endpoint_fail(app, client, samples, mocked_responses):
    with patch("lighthouse.helpers.plates.has_sample_data", side_effect=Exception()):
        response = client.get("/plates?barcodes[]=123&barcodes[]=456", content_type="application/json")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to lookup plates: Exception"]}
