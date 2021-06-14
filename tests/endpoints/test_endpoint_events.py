from http import HTTPStatus
from unittest.mock import patch


def test_post_unauthenticated(app, client):
    with app.app_context():
        response = client.post("/events", data={})

        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_post_unrecognised_event_type(app, client, biosero_auth_headers):
    with app.app_context():
        response = client.post("/events", data={
            "automation_system_run_id": 123,
            "barcode": "plate_barcode_123",
            "event_type": "COFFEE_MACHINE_BROKEN",
            "user_id": "user1",
            "robot": "roboto",
        }, headers=biosero_auth_headers)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Event source partially completed

def test_post_event_partially_completed_missing_barcode(app, client, biosero_auth_headers):
    with app.app_context():
        response = client.post("/events", data={
            "automation_system_run_id": 123,
            "event_type": "lh_biosero_cp_source_partial",
            "user_id": "user1",
            "robot": "roboto",
        }, headers=biosero_auth_headers)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_post_event_partially_completed(app, client, biosero_auth_headers):

    with app.app_context():
        response = client.post("/events", data={
            "run_id": "123",
            "barcode": "plate_barcode_123",
            "event_type": "lh_biosero_cp_source_partial",
            "user_id": "user1",
            "robot": "BHRB0001",
        }, headers=biosero_auth_headers)

        # Test creates the event
        assert response.status_code == HTTPStatus.CREATED
        # assert mock_send_wh.assert_called()

