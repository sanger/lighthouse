from http import HTTPStatus
import responses
from unittest.mock import patch, MagicMock


def test_post_unauthenticated(app, client):
    with app.app_context():
        response = client.post("/events", data={})

        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_post_unrecognised_event_type(app, client, biosero_auth_headers):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "barcode": "plate_barcode_123",
                "event_type": "COFFEE_MACHINE_BROKEN",
                "user_id": "user1",
                "robot": "roboto",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Event source partially completed


def test_post_event_partially_completed_missing_barcode(app, client, biosero_auth_headers):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "event_type": "lh_biosero_cp_source_partial",
                "user_id": "user1",
                "robot": "roboto",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_post_event_partially_completed(app, client, biosero_auth_headers):

def test_post_event_partially_completed_missing_barcode(app, client, biosero_auth_headers):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "event_type": "lh_biosero_cp_source_partial",
                "user_id": "user1",
                "robot": "roboto",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_post_event_partially_completed(app, client, biosero_auth_headers, mocked_responses):

    with app.app_context():
        mocked_broker = MagicMock()
        with patch("lighthouse.classes.plate_event.Broker", return_value=mocked_broker):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[1, 2, 3, 4]):
                with patch(
                    "lighthouse.classes.messages.warehouse_messages.WarehouseMessage.get_message_timestamp",
                    return_value="mytime",
                ):

                    mocked_channel = MagicMock()
                    mocked_broker.__enter__.return_value = mocked_channel

                    run_id = 2
                    url = f"{app.config['CHERRY_TRACK_URL']}/automation-system-runs/{run_id}"

                    expected_response = {
                        "data": {
                            "id": run_id,
                            "user_id": "ab1",
                            "liquid_handler_serial_number": "aLiquidHandlerSerialNumber",
                        }
                    }

                    mocked_responses.add(
                        responses.GET,
                        url,
                        json=expected_response,
                        status=HTTPStatus.OK,
                    )

                    response = client.post(
                        "/events",
                        data={
                            "automation_system_run_id": run_id,
                            "barcode": "plate_barcode_123",
                            "event_type": "lh_biosero_cp_source_partial",
                            "user_id": "user1",
                            "robot": "BHRB0001",
                        },
                        headers=biosero_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    mocked_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key="test.event.lh_biosero_cp_source_partial",
                        body=(
                            '{"event": {"uuid": "1", "event_type": "lh_biosero_cp_source_partial", '
                            '"occured_at": "mytime", "user_identifier": "user1", '
                            '"subjects": [{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                            '"friendly_name": "plate_barcode_123", "uuid": "1234"}, {"role_type": "robot", '
                            '"subject_type": "robot", "friendly_name": "BHRB0001", '
                            '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}], "metadata": {}}, "lims": "LH_TEST"}'
                        ),
                    )
