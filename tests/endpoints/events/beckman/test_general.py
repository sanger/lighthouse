from http import HTTPStatus
from unittest.mock import patch

import pytest
from uuid import uuid4

from lighthouse.messages.message import Message

from lighthouse.classes.beckman_v3 import Beckman

ENDPOINT_PREFIXES = ["", "/v1"]
CREATE_PLATE_EVENTS_URL = "/plate-events/create"
CREATE_PLATE_EVENTS_URLS = [prefix + CREATE_PLATE_EVENTS_URL for prefix in ENDPOINT_PREFIXES]

EVENT_TYPES = [
    Beckman.EVENT_SOURCE_UNRECOGNISED,
    Beckman.EVENT_SOURCE_COMPLETED,
    Beckman.EVENT_SOURCE_ALL_NEGATIVES,
    Beckman.EVENT_SOURCE_NO_PLATE_MAP_DATA,
]

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_bad_request_no_event_type(client, url):
    response = client.get(f"{url}")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_bad_request_empty_event_type(client, url):
    response = client.get(f"{url}?event_type=")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1



@pytest.mark.parametrize("endpoint_url", EVENT_TYPES, indirect=True)
def test_event_source_missing_user_id(app, client, clear_events, endpoint_url):
    with app.app_context():
        response = client.get(
            f"{endpoint_url}&robot=BKRB0001&user_id="
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert "GET request needs 'user_id' in URL" in str(response.json['_issues'])


@pytest.mark.parametrize("endpoint_url", EVENT_TYPES, indirect=True)
def test_event_source_missing_robot(app, client, clear_events, endpoint_url):
    with app.app_context():
        response = client.get(
            f"{endpoint_url}&user_id=user_id"
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert "GET request needs 'robot' in URL" in str(response.json['_issues'])


@pytest.mark.parametrize("endpoint_url", EVENT_TYPES, indirect=True)
def test_event_source_wrong_robot(app, client, clear_events, endpoint_url):
    with app.app_context():
        with patch(
                    "lighthouse.classes.services.mongo.MongoServiceMixin.get_source_plate_uuid",
                    side_effect=[int_to_uuid(1)],
        ):
            response = client.get(
                f"{endpoint_url}&robot=wrong&user_id=user_id"
            )

        response_errors = response.json.get("_issues")
        assert "Exception during retrieval: Robot with barcode wrong not found" in response_errors.get("robot_uuid")
