from http import HTTPStatus
from unittest.mock import patch

import responses  # type: ignore

def test_get_create_plate_event_endpoint_bad_request_no_barcode(client):
    response = client.get("/plate-events/create?event_type=test_type)")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

def test_get_create_plate_event_endpoint_bad_request_no_event_type(client):
    response = client.get("/plate-events/create?barcode=test_barcode)")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1

def test_get_create_plate_event_endpoint_ok(client):
    response = client.get("/plate-events/create?barcode=test_barcode&event_type=test_type)")

    assert response.status_code == HTTPStatus.OK
    assert not response.json
