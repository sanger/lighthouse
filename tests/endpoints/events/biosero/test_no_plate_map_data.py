from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest

from lighthouse.constants.fields import FIELD_EVENT_ERRORS
from lighthouse.helpers.mongo import get_event_with_uuid
from lighthouse.classes.biosero import Biosero

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


# Event source partially completed


def test_post_event_no_plate_map_data_missing_barcode(app, client, biosero_auth_headers, clear_events):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "event_type": Biosero.EVENT_SOURCE_NO_PLATE_MAP_DATA,
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("run_id", [3])
def test_post_event_no_plate_map_data(
    app,
    client,
    biosero_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    run_id,
    mocked_responses,
    cherrytrack_mock_run_info,
):
    with app.app_context():
        with patch("lighthouse.hooks.events.uuid4", return_value=int_to_uuid(1)):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[int_to_uuid(2)]):
                with patch(
                    "lighthouse.classes.events.PlateEvent.message_timestamp",
                    "mytime",
                ):
                    response = client.post(
                        "/events",
                        data={
                            "automation_system_run_id": 3,
                            "barcode": "plate_123",
                            "event_type": Biosero.EVENT_SOURCE_NO_PLATE_MAP_DATA,
                        },
                        headers=biosero_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key=f"test.event.{ Biosero.EVENT_SOURCE_NO_PLATE_MAP_DATA }",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "' + Biosero.EVENT_SOURCE_NO_PLATE_MAP_DATA + '", '
                            '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                            '[{"role_type": "robot", "subject_type": "robot", "friendly_name": "CPA", '
                            '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}, '
                            '{"role_type": "run", "subject_type": "run", "friendly_name": 3, '
                            '"uuid": "' + int_to_uuid(2) + '"}], '
                            '"metadata": {"source_plate_barcode": "plate_123"}}, "lims": "LH_TEST"}'
                        ),
                    )

                    # The record is there
                    event = get_event_with_uuid(int_to_uuid(1))
                    assert event is not None

                    # And it does not have errors
                    assert event[FIELD_EVENT_ERRORS] is None


def test_post_event_no_plate_map_data_with_validation_error_after_storing_in_mongo(
    app, client, biosero_auth_headers, clear_events, mocked_rabbit_channel
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.events.uuid4",
            side_effect=[int_to_uuid(1), int_to_uuid(2), int_to_uuid(3), int_to_uuid(4)],
        ):
            with patch(
                "lighthouse.classes.events.PlateEvent.message_timestamp",
                return_value="mytime",
            ):
                response = client.post(
                    "/events",
                    data={
                        "automation_system_run_id": 3,
                        "barcode": "a Barcode",
                        "event_type": Biosero.EVENT_SOURCE_NO_PLATE_MAP_DATA,
                    },
                    headers=biosero_auth_headers,
                )

                # Test creates the event
                assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

                # However the message is not published
                mocked_rabbit_channel.basic_publish.assert_not_called()

                # But the record is there
                event = get_event_with_uuid(int_to_uuid(1))
                assert event is not None

                # And it has errors
                assert event[FIELD_EVENT_ERRORS] == {
                    "plate_barcode": ["'barcode' should not contain any whitespaces"],
                }
