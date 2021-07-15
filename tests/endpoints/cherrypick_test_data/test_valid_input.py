import re
from http import HTTPStatus
from typing import List
from unittest.mock import Mock, patch

import pytest
from requests.models import HTTPError, Response

from lighthouse.constants.cherrypick_test_data import (
    CPTD_STATUS_PENDING,
    FIELD_CRAWLER_RUN_ID,
)
from lighthouse.constants.error_messages import (
    ERROR_CRAWLER_INTERNAL_SERVER_ERROR,
)

ENDPOINT_PATH = "/cherrypick-test-data"


@pytest.fixture
def mock_post():
    with patch("requests.post") as mock_post:
        yield mock_post


def mock_response(status_code, json_object, http_error_msg=""):
    mock_response = Mock()
    mock_response.status_code.return_value = status_code
    mock_response.json.return_value = json_object

    def raise_for_status():
        if http_error_msg:
            raise HTTPError(http_error_msg, response=mock_response)

    mock_response.raise_for_status.side_effect = raise_for_status

    return mock_response


def valid_json_object(add_to_dart: bool = True, plate_specs: List[List[int]] = None) -> dict:
    if plate_specs is None:
        plate_specs = [[1, 96]]

    return {"add_to_dart": add_to_dart, "plate_specs": plate_specs}


@pytest.mark.parametrize("add_to_dart, plate_specs", [[True, [[1, 0], [2, 96]]], [False, [[100, 48], [100, 96]]]])
def test_create_run_successful(client, mock_post, add_to_dart, plate_specs):
    post_response = client.post(ENDPOINT_PATH, json=valid_json_object(add_to_dart, plate_specs))

    assert post_response.status_code == HTTPStatus.CREATED

    item_endpoint = post_response.json["_links"]["self"]["href"]
    get_response = client.get(item_endpoint)

    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["status"] == CPTD_STATUS_PENDING
    assert get_response.json["add_to_dart"] == add_to_dart
    assert get_response.json["plate_specs"] == plate_specs


def test_plate_spec_validator_called(client, mock_post):
    json_object = valid_json_object()

    with patch("lighthouse.validator.LighthouseValidator._check_with_validate_cptd_plate_specs") as validate_method:
        client.post(ENDPOINT_PATH, json=json_object)

    validate_method.assert_called_with("plate_specs", json_object["plate_specs"])


def test_request_made_to_crawler(client, mock_post):
    posted_url = ""
    posted_json = {}

    def post_method(url, json):
        nonlocal posted_url, posted_json
        posted_url = url
        posted_json = json

        response = Response()
        response.status_code = HTTPStatus.OK
        return response

    mock_post.side_effect = post_method

    client.post(ENDPOINT_PATH, json=valid_json_object())

    mock_post.assert_called_once()
    assert posted_url.endswith("/cherrypick-test-data")
    assert FIELD_CRAWLER_RUN_ID in posted_json
    assert re.match(r"[0-9a-f]{24}", posted_json[FIELD_CRAWLER_RUN_ID])


@pytest.mark.parametrize("status_code", [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED])
def test_success_codes_from_crawler_give_created_response(client, mock_post, status_code):
    mock_response = Response()
    mock_response.status_code = status_code
    mock_post.return_value = mock_response

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    "status_code", [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.UNAUTHORIZED]
)
def test_failure_codes_from_crawler_give_500_response(client, mock_post, status_code):
    mock_post.return_value = mock_response(status_code, {"errors": ["test-a", "test-b"]}, f"{status_code} HTTP Error")

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json["_issues"] == ["test-a", "test-b"]
    assert response.json["_error"]["code"] == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json["_error"]["message"] == ERROR_CRAWLER_INTERNAL_SERVER_ERROR


def test_crawler_errors_added_to_response_when_not_a_list(client, mock_post):
    mock_post.return_value = mock_response(500, {"errors": "error message"}, "500 HTTP Error")

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert response.json["_issues"] == ["error message"]


def test_exception_message_added_to_response_when_no_errors_from_crawler(client, mock_post):
    mock_post.return_value = mock_response(500, {"no_errors": "none here"}, "500 Server Error")

    response = client.post(ENDPOINT_PATH, json=valid_json_object())

    assert len(response.json["_issues"]) == 1
    assert response.json["_issues"][0] == "500 Server Error"
