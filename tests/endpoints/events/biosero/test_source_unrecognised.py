from http import HTTPStatus
from unittest.mock import patch
from lighthouse.helpers.mongo import get_event_with_uuid
from lighthouse.constants.fields import FIELD_EVENT_ERRORS


import pytest
from uuid import uuid4

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


@pytest.mark.parametrize("run_id", [3])
def test_post_event_source_unrecognised(
    app,
    client,
    biosero_auth_headers,
    clear_events_when_finish,
    mocked_rabbit_channel,
    run_id,
    mocked_responses,
    cherrytrack_mock_run_info,
):
    with app.app_context():
        with patch("lighthouse.hooks.events.uuid4", return_value=int_to_uuid(1)):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[int_to_uuid(2)]):
                with patch(
                    "lighthouse.classes.plate_event.PlateEvent.message_timestamp",
                    "mytime",
                ):
                    response = client.post(
                        "/events",
                        data={
                            "automation_system_run_id": 3,
                            "event_type": "lh_biosero_cp_source_plate_unrecognised",
                            "user_id": "user1",
                            "robot": "BHRB0001",
                        },
                        headers=biosero_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key="test.event.lh_biosero_cp_source_plate_unrecognised",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "lh_biosero_cp_source_plate_unrecognised", '
                            '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                            '[{"role_type": "robot", "subject_type": "robot", "friendly_name": "BHRB0001", '
                            '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}, '
                            '{"role_type": "run", "subject_type": "run", "friendly_name": 3, '
                            '"uuid": "' + int_to_uuid(2) + '"}], '
                            '"metadata": {}}, "lims": "LH_TEST"}'
                        ),
                    )

                    # The record is there
                    event = get_event_with_uuid(int_to_uuid(1))
                    assert event is not None

                    # And it does not have errors
                    assert event[FIELD_EVENT_ERRORS] is None


def test_post_event_source_unrecognised_with_validation_error_after_storing_in_mongo(
    app, client, biosero_auth_headers, clear_events_when_finish, mocked_rabbit_channel
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.events.uuid4",
            side_effect=[int_to_uuid(1), int_to_uuid(2), int_to_uuid(3), int_to_uuid(4)],
        ):
            with patch(
                "lighthouse.classes.plate_event.PlateEvent.message_timestamp",
                return_value="mytime",
            ):
                response = client.post(
                    "/events",
                    data={
                        "automation_system_run_id": 3,
                        "event_type": "lh_biosero_cp_source_plate_unrecognised",
                        "user_id": "us  er1",
                        "robot": "BHR  B0001",
                    },
                    headers=biosero_auth_headers,
                )

                # Test creates the event
                assert response.status_code == HTTPStatus.CREATED

                # However the message is not published
                mocked_rabbit_channel.basic_publish.assert_not_called()

                # But the record is there
                event = get_event_with_uuid(int_to_uuid(1))
                assert event is not None

                # And it has errors
                assert event[FIELD_EVENT_ERRORS] == {
                    "robot_serial_number": ["'robot' should not contain any whitespaces"],
                    "robot_uuid": ["'robot' should not contain any whitespaces"],
                }
