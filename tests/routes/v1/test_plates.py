import urllib.parse
from http import HTTPStatus
from unittest.mock import patch

import pytest
import responses

from lighthouse.constants.error_messages import (
    ERROR_ADD_COG_BARCODES,
    ERROR_PLATES_CREATE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)
from lighthouse.constants.general import ARG_EXCLUDE, ARG_TYPE, ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE

ENDPOINT_PREFIXES = ["", "/v1"]
NEW_PLATE_ENDPOINT = "/plates/new"
GET_PLATES_ENDPOINT = "/plates"

NEW_PLATE_ENDPOINTS = [prefix + NEW_PLATE_ENDPOINT for prefix in ENDPOINT_PREFIXES]
GET_PLATES_ENDPOINTS = [prefix + GET_PLATES_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_successful(
    app, client, samples, priority_samples, mocked_responses, mlwh_lh_samples, endpoint
):
    with patch("lighthouse.routes.common.plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = {"barcode": "plate_123"}
        mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.CREATED)

        response = client.post(endpoint, json=body)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json == {
            "data": {"plate_barcode": "plate_123", "centre": "TC1", "count_fit_to_pick_samples": 4}
        }


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_no_barcode_in_request(app, client, samples, endpoint):
    response = client.post(endpoint, json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode' in body"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_no_fit_to_pick_samples(app, client, endpoint):
    response = client.post(endpoint, json={"barcode": "qwerty"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["No fit to pick samples for this barcode: qwerty"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_add_cog_barcodes_failed(
    app, client, samples, priority_samples, centres, mocked_responses, endpoint
):
    baracoda_url = f"http://{app.config['BARACODA_URL']}/barcodes_group/TC1/new?count=4"

    mocked_responses.add(responses.POST, baracoda_url, status=HTTPStatus.BAD_REQUEST)

    response = client.post(endpoint, json={"barcode": "plate_123"})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"{ERROR_PLATES_CREATE} {ERROR_ADD_COG_BARCODES} plate_123"]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_endpoint_ss_failure(app, client, samples, mocked_responses, endpoint):
    with patch("lighthouse.routes.common.plates.add_cog_barcodes", return_value="TC1"):
        ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

        body = {"errors": ["The barcode 'plate_123' is not a recognised format."]}
        mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.UNPROCESSABLE_ENTITY)

        response = client.post(endpoint, json={"barcode": "plate_123"})

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.json == {"errors": ["The barcode 'plate_123' is not a recognised format."]}


@pytest.mark.parametrize("endpoint", NEW_PLATE_ENDPOINTS)
def test_post_plates_mlwh_update_failure(app, client, samples, mocked_responses, endpoint):
    with patch("lighthouse.routes.common.plates.add_cog_barcodes", return_value="TC1"):
        with patch("lighthouse.routes.common.plates.update_mlwh_with_cog_uk_ids", side_effect=Exception()):
            ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

            body = {"barcode": "plate_123"}
            mocked_responses.add(responses.POST, ss_url, json=body, status=HTTPStatus.CREATED)

            response = client.post(endpoint, json={"barcode": "plate_123"})

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json == {"errors": [ERROR_UPDATE_MLWH_WITH_COG_UK_IDS]}


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_successful(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_without_samples, endpoint
):
    response = client.get(
        f"{endpoint}?barcodes=plate_123,456&{ ARG_EXCLUDE }=pickable_samples",
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

    response = client.get(f"{endpoint}?barcodes=456&{ ARG_EXCLUDE }=pickable_samples&{ARG_TYPE}={ARG_TYPE_SOURCE}")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "plates": [
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


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_no_barcode_in_request(client, endpoint):
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_barcode_empty(client, endpoint):
    response = client.get(f"{endpoint}?barcodes=")

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_method_calls(app, client, samples, priority_samples, endpoint):
    barcode = "plate_123"
    with patch("lighthouse.helpers.plates.has_plate_map_data", return_value=True) as mock_has_plate_map_data:
        response = client.get(f"{endpoint}?barcodes={barcode}", content_type="application/json")
        assert response.status_code == HTTPStatus.OK
        mock_has_plate_map_data.assert_called_once_with(barcode)


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_fail(app, client, samples, mocked_responses, endpoint):
    with patch("lighthouse.helpers.plates.get_fit_to_pick_samples_and_counts", side_effect=Exception()):
        response = client.get(f"{endpoint}?barcodes=123,456", content_type="application/json")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json == {"errors": ["Failed to lookup plates: Exception"]}


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_endpoint_exclude_props(
    app, client, samples, priority_samples, mocked_responses, plates_lookup_with_samples, endpoint
):
    response = client.get(
        f"{endpoint}?barcodes=plate_123,456&{ ARG_EXCLUDE }=plate_barcode",
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


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_with_type(app, client, mocked_responses, endpoint):
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

    response = client.get(
        f"{endpoint}?barcodes={first_plate_barcode},{second_plate_barcode}&{ ARG_TYPE }={ARG_TYPE_DESTINATION}",
    )

    assert response.status_code == HTTPStatus.OK

    assert response.json == {
        "plates": [
            {
                "plate_barcode": first_plate_barcode,
                "plate_exists": True,
            },
            {
                "plate_barcode": second_plate_barcode,
                "plate_exists": False,
            },
        ]
    }


@pytest.mark.parametrize("endpoint", GET_PLATES_ENDPOINTS)
def test_get_plates_with_invalid_type(app, client, endpoint):
    first_plate_barcode = "plate_123"
    second_plate_barcode = "plate_456"
    response = client.get(
        f"{endpoint}?barcodes={first_plate_barcode},{second_plate_barcode}&{ ARG_TYPE }=invalid_type",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST