from http import HTTPStatus
from unittest.mock import patch

import responses
from lighthouse.constants.general import ARG_EXCLUDE_FIELDS
from lighthouse.constants.error_messages import (
    ERROR_ADD_COG_BARCODES,
    ERROR_PLATES_CREATE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)


def test_post_plates_endpoint_successful(app, client, samples, priority_samples, mocked_responses, mlwh_lh_samples):
    with patch("lighthouse.blueprints.plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = {"barcode": "plate_123"}
        mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.CREATED)

        response = client.post("/plates/new", json=body)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json == {
            "data": {"plate_barcode": "plate_123", "centre": "TC1", "count_fit_to_pick_samples": 4}
        }


def test_post_plates_endpoint_no_barcode_in_request(app, client, samples):
    response = client.post("/plates/new", json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode' in body"]}


def test_post_plates_endpoint_no_fit_to_pick_samples(app, client):
    response = client.post("/plates/new", json={"barcode": "qwerty"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["No fit to pick samples for this barcode: qwerty"]}


def test_post_plates_endpoint_add_cog_barcodes_failed(
    app, client, samples, priority_samples, centres, mocked_responses
):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TC1/new?count=4"

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
            mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.CREATED)

            response = client.post("/plates/new", json={"barcode": "plate_123"})

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [ERROR_UPDATE_MLWH_WITH_COG_UK_IDS]}


def test_get_plates_endpoint_successful(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_without_samples
):
    response = client.get(
        f"/plates?barcodes=plate_123,456&{ ARG_EXCLUDE_FIELDS }=pickable_samples",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "plates": [
            plates_lookup_without_samples["plate_123"],
            {
                "plate_barcode": "456",
                "has_plate_map": False,
                "count_fit_to_pick_samples": 0,
                "count_filtered_positive": 0,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
            },
        ]
    }


def test_get_plates_endpoint_method_calls(app, client, samples, priority_samples):
    barcode = "plate_123"
    with patch("lighthouse.helpers.plates.has_plate_map_data", return_value=True) as mock_has_plate_map_data:
        response = client.get(f"/plates?barcodes={barcode}", content_type="application/json")
        assert response.status_code == HTTPStatus.OK
        mock_has_plate_map_data.assert_called_once_with(barcode)


def test_get_plates_endpoint_fail(app, client, samples, mocked_responses):
    with patch("lighthouse.helpers.plates.get_fit_to_pick_samples_and_counts", side_effect=Exception()):
        response = client.get("/plates?barcodes=123,456", content_type="application/json")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to lookup plates: Exception"]}


def test_get_plates_endpoint_exclude_props(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_with_samples
):
    response = client.get(
        f"/plates?barcodes=plate_123,456&{ ARG_EXCLUDE_FIELDS }=plate_barcode",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK

    # shallow copy of plate
    first_plate = plates_lookup_with_samples["plate_123"].copy()
    # we remove the barcode attr
    first_plate.pop("plate_barcode")

    assert response.json == {
        "plates": [
            first_plate,
            {
                "has_plate_map": False,
                "count_fit_to_pick_samples": 0,
                "count_filtered_positive": 0,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
                "pickable_samples": [],
            },
        ]
    }
