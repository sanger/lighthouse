import json
import re
from http import HTTPStatus
from typing import List, Optional
from unittest.mock import patch

import pytest
import responses

from lighthouse.config.test import CRAWLER_BASE_URL
from lighthouse.constants.cherrypick_test_data import CPTD_STATUS_PENDING, FIELD_CRAWLER_RUN_ID
from lighthouse.constants.error_messages import ERROR_CRAWLER_HTTP_ERROR

CRAWLER_URL = f"{CRAWLER_BASE_URL}/v1/cherrypick-test-data"
ENDPOINT_PATH = "/cherrypick-test-data"


def valid_json_object(plate_specs: Optional[List[List[int]]] = None) -> dict:
    if plate_specs is None:
        plate_specs = [[1, 96]]

    return {"plate_specs": plate_specs}


@pytest.mark.parametrize("plate_specs", [[[1, 0], [2, 96]], [[100, 48], [100, 96]]])
def test_create_run_successful(client, plate_specs):
    with patch("requests.post"):
        post_response = client.post(ENDPOINT_PATH, json=valid_json_object(plate_specs))

    assert post_response.status_code == HTTPStatus.CREATED

    item_endpoint = post_response.json["_links"]["self"]["href"]
    get_response = client.get(item_endpoint)

    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["status"] == CPTD_STATUS_PENDING
    assert get_response.json["plate_specs"] == plate_specs


def test_plate_spec_validator_called(client):
    json_object = valid_json_object()

    with patch("requests.post"):
        with patch("lighthouse.validator.LighthouseValidator._check_with_validate_cptd_plate_specs") as validate_method:
            client.post(ENDPOINT_PATH, json=json_object)

    validate_method.assert_called_with("plate_specs", json_object["plate_specs"])


def test_request_made_to_crawler(client, mocked_responses):
    mocked_responses.add(responses.POST, CRAWLER_URL, status=200)

    client.post(ENDPOINT_PATH, json=valid_json_object())

    assert len(mocked_responses.calls) == 1
    request = mocked_responses.calls[0].request
    assert request.url == CRAWLER_URL
    assert request.headers["Content-Type"] == "application/json"
    body_json = json.loads(request.body.decode("utf-8"))
    assert list(body_json.keys()) == [FIELD_CRAWLER_RUN_ID]
    assert re.match(r"[0-9a-f]{24}", body_json[FIELD_CRAWLER_RUN_ID])


@pytest.mark.parametrize("status_code", [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED])
def test_success_codes_from_crawler_give_created_response(client, mocked_responses, status_code):
    mocked_responses.add(responses.POST, CRAWLER_URL, status=status_code)

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    "status_code", [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.UNAUTHORIZED]
)
def test_failure_codes_from_crawler_give_correct_response(client, mocked_responses, status_code):
    mocked_responses.add(responses.POST, CRAWLER_URL, json={"errors": ["test-a", "test-b"]}, status=status_code)

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.status_code == status_code
    assert response.json["_error"]["code"] == status_code
    assert ERROR_CRAWLER_HTTP_ERROR in response.json["_error"]["message"]
    assert json.dumps(["test-a", "test-b"]) in response.json["_error"]["message"]


def test_crawler_errors_added_to_response_when_not_a_list(client, mocked_responses):
    mocked_responses.add(responses.POST, CRAWLER_URL, json={"errors": "error message"}, status=500)

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert ERROR_CRAWLER_HTTP_ERROR in response.json["_error"]["message"]
    assert "error message" in response.json["_error"]["message"]


def test_exception_message_added_to_response_when_no_errors_from_crawler(client, mocked_responses):
    mocked_responses.add(responses.POST, CRAWLER_URL, json={"no_errors": "none here"}, status=500)

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert ERROR_CRAWLER_HTTP_ERROR in response.json["_error"]["message"]
    assert "500 Server Error" in response.json["_error"]["message"]


def test_internal_server_error_response_generated_when_not_httperror(client, mocked_responses):
    mocked_responses.add(responses.POST, CRAWLER_URL, body=ConnectionError("A connection error occurred"), status=500)

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json["_error"]["code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "A connection error occurred" in response.json["_error"]["message"]
