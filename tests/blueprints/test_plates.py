from http import HTTPStatus
from unittest.mock import patch
import json
import responses  # type: ignore


def test_post_plates_endpoint_successful(app, client, samples, mocked_responses):
    with patch(
        "lighthouse.blueprints.plates.add_cog_barcodes", return_value="TS1",
    ):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = json.dumps({"barcode": "123"})
        mocked_responses.add(
            responses.POST, ss_url, body=body, status=HTTPStatus.OK,
        )

        response = client.post(
            "/plates/new", data=json.dumps({"barcode": "123"}), content_type="application/json",
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json == {
            "data": {"plate_barcode": "123", "centre": "TS1", "number_of_positives": 1}
        }


def test_post_plates_endpoint_no_barcode_in_request(app, client, samples):
    response = client.post("/plates/new", data=json.dumps({}), content_type="application/json",)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode' in body"]}


def test_post_plates_endpoint_no_positive_samples(app, client):
    response = client.post(
        "/plates/new", data=json.dumps({"barcode": "123"}), content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["No samples for this barcode: 123"]}


def test_post_plates_endpoint_add_cog_barcodes_failed(
    app, client, samples, centres, mocked_responses
):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TS1/new?count=1"

    mocked_responses.add(
        responses.POST, baracoda_url, status=HTTPStatus.BAD_REQUEST,
    )

    response = client.post(
        "/plates/new", data=json.dumps({"barcode": "123"}), content_type="application/json",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["Failed to add COG barcodes to plate: 123"]}


def test_post_plates_endpoint_ss_failure(app, client, samples, mocked_responses):
    with patch(
        "lighthouse.blueprints.plates.add_cog_barcodes", return_value="TS1",
    ):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = json.dumps({"errors": ["The barcode '123' is not a recognised format."]})
        mocked_responses.add(
            responses.POST, ss_url, body=body, status=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

        response = client.post(
            "/plates/new", data=json.dumps({"barcode": "123"}), content_type="application/json",
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == {"errors": ["The barcode '123' is not a recognised format."]}
