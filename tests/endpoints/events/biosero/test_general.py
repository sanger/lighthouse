from http import HTTPStatus


def test_post_unauthenticated(app, client, clear_events):
    with app.app_context():
        response = client.post("/events", data={})

        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_post_unrecognised_event_type(app, client, biosero_auth_headers, clear_events):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "barcode": "plate_barcode_123",
                "event_type": "COFFEE_MACHINE_BROKEN",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
