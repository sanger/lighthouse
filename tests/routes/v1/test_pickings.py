from http import HTTPStatus

# from unittest.mock import patch

import json
import os
import pytest
import responses

ENDPOINT_PREFIXES = ["", "/v1"]
GET_PICKINGS_ENDPOINT = "/pickings"

GET_PICKINGS_ENDPOINTS = [prefix + GET_PICKINGS_ENDPOINT for prefix in ENDPOINT_PREFIXES]


def ss_request_url(app, barcode):
    """Returns SS URL for the specified barcode using app config."""
    ss_url = (
        f"{app.config['SS_URL']}/api/v2/labware?filter[barcode]={barcode}"
        f"&include=purpose,receptacles.aliquots.sample"
    )
    return ss_url


def endpoint_request_json(barcode):
    """Returns enpoint request json for the specified barcode."""
    json = {"user": "user1", "robot": "robot1", "barcode": barcode}
    return json


def ss_response_json(name):
    """Returns SS response json for the specified name."""
    root = "tests/data/pickings"
    path = os.path.join(root, name + ".json")
    with open(path) as fp:
        return json.loads(fp.read())


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_success(
    app,
    client,
    mocked_responses,
    endpoint,
):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)

    body = ss_response_json("plate")

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"barcode": barcode, "positive_control": "A1", "negative_control": "B1"}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("missing_post_data", ["user", "robot", "barcode"])
def test_get_pickings_endpoint_missing_post_data(client, endpoint, missing_post_data):
    barcode = "ABCD-1234"
    json = endpoint_request_json(barcode)
    json.pop(missing_post_data)

    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": ["POST request needs 'barcode', 'user' and 'robot' in body"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_ss_unaccessible(app, client, endpoint, monkeypatch):
    ss_url = "http://ss.invalid"  # Simulate Sequencescape down. See RFC 2606
    barcode = "ABCD-1234"

    monkeypatch.setitem(app.config, "SS_URL", ss_url)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {"errors": ["Unable to access Sequencescape"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("response_body", ["", "<html>"])
def test_get_pickings_endpoint_ss_no_data_in_response(app, client, endpoint, mocked_responses, response_body):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)
    body = response_body

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == {"errors": [f"Expected 'data' in response: {response_body}"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_ss_incorrect_purpose(app, client, endpoint, mocked_responses):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)

    body = ss_response_json("incorrect_purpose")
    purpose = "INCORRECT PURPOSE"

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"Incorrect purpose '{purpose}' for barcode '{barcode}'"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
def test_get_pickings_endpoint_ss_missing_samples(app, client, endpoint, mocked_responses):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)

    body = ss_response_json("missing_samples")

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"There are no samples for barcode '{barcode}'"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("missing_control_type", ["positive", "negative"])
def test_get_pickings_endpoint_ss_missing_control(app, client, endpoint, mocked_responses, missing_control_type):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)

    body = ss_response_json("missing_" + missing_control_type + "_control")

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"errors": [f"Missing positive or negative control for barcode '{barcode}'"]}


@pytest.mark.parametrize("endpoint", GET_PICKINGS_ENDPOINTS)
@pytest.mark.parametrize("extra_control_type", ["positive", "negative"])
def test_get_pickings_endpoint_ss_extra_control(app, client, endpoint, mocked_responses, extra_control_type):
    barcode = "ABCD-1234"
    ss_url = ss_request_url(app, barcode)

    body = ss_response_json("extra_" + extra_control_type + "_control")

    mocked_responses.add(responses.GET, ss_url, json=body, status=HTTPStatus.OK)

    json = endpoint_request_json(barcode)
    response = client.post(endpoint, json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        "errors": [f"There should be only one positive and one negative control for barcode '{barcode}'"]
    }
