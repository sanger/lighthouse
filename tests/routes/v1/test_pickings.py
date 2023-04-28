from http import HTTPStatus

# from unittest.mock import patch

import pytest
import responses

ENDPOINT_PREFIXES = ["", "/v1"]
GET_PICKINGS_ENDPOINT = "/pickings"

GET_PICKINGS_ENDPOINTS = [prefix + GET_PICKINGS_ENDPOINT for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_success(app, client, mocked_responses, endpoint, pickings_plate):
    barcode = "ABCD-1234"
    ss_url = (
        f"{app.config['SS_URL']}/api/v2/labware?filter[barcode]={barcode}&include=purpose,receptacles.aliquots.sample"
    )

    body = pickings_plate

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = {"user": "user1", "robot": "robot1", "barcode": barcode}
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"barcode": barcode, "positive_control": "A1", "negative_control": "B1"}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("missing_post_data", ["user", "robot", "barcode"])
def test_get_pickings_endpoint_missing_post_data(client, endpoint, missing_post_data):
    barcode = "ABCD-1234"
    json = {"user": "user1", "robot": "robot1", "barcode": barcode}
    json.pop(missing_post_data)

    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode', 'user' and 'robot' in body"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_ss_unaccessible(app, client, endpoint, monkeypatch):
    ss_url = "http://ss.invalid"  # Simulate Sequencescape down. See RFC 2606
    barcode = "ABCD-1234"

    monkeypatch.setitem(app.config, "SS_URL", ss_url)

    json = {"user": "user1", "robot": "robot1", "barcode": barcode}
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {"errors": ["Unable to access Sequencescape"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("response_body", ["", "<html>"])
def test_get_pickings_endpoint_ss_no_data_in_response(app, client, endpoint, mocked_responses, response_body):
    barcode = "ABCD-1234"
    ss_url = (
        f"{app.config['SS_URL']}/api/v2/labware?filter[barcode]={barcode}&include=purpose,receptacles.aliquots.sample"
    )
    body = response_body

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = {"user": "user1", "robot": "robot1", "barcode": barcode}
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {"errors": [f"Expected 'data' in response: {response_body}"]}


# TODO (DPL-572):
# Test failures:
# stub SS response so that purpose is incorrect
# stub SS reponse so that data has no samples
# stub SS reponse so that data has missing +ve control
# stub SS reponse so that data has missing -ve control
# stub SS reponse so that data has more than one +ve or -ve control
