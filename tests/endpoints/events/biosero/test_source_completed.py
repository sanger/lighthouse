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


# Event source partially completed


def test_post_event_partially_completed_missing_barcode(app, client, biosero_auth_headers, clear_events):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "event_type": "lh_biosero_cp_source_completed",
                "user_id": "user1",
                "robot": "roboto",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["plate_456"])
def test_post_event_partially_completed(
    app,
    client,
    biosero_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    source_plates,
    run_id,
    source_barcode,
    destination_barcode,
    mocked_responses,
    cherrytrack_mock_run_info,
    cherrytrack_mock_source_plates,
    samples_from_cherrytrack_into_mongo,
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.events.uuid4",
            side_effect=[int_to_uuid(1)],
        ):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[int_to_uuid(2)]):
                with patch(
                    "lighthouse.classes.events.PlateEvent.message_timestamp",
                    "mytime",
                ):
                    response = client.post(
                        "/events",
                        data={
                            "automation_system_run_id": run_id,
                            "barcode": source_barcode,
                            "event_type": "lh_biosero_cp_source_completed",
                            "user_id": "user1",
                            "robot": "BHRB0001",
                        },
                        headers=biosero_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key="test.event.lh_biosero_cp_source_completed",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "lh_biosero_cp_source_completed", '
                            '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                            '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId1__plate_123_A01__centre_1__Positive", "uuid": "aLighthouseUUID1"}, '
                            '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId3__plate_123_A03__centre_1__Positive", "uuid": "aLighthouseUUID3"}, '
                            '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                            '"friendly_name": "plate_123", "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc"}, '
                            '{"role_type": "robot", "subject_type": "robot", "friendly_name": "BHRB0001", '
                            '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}, '
                            '{"role_type": "run", "subject_type": "run", "friendly_name": 3, '
                            '"uuid": "' + int_to_uuid(2) + '"}'
                            '], "metadata": {}}, "lims": "LH_TEST"}'
                        ),
                    )

                    # The record is there
                    event = get_event_with_uuid(int_to_uuid(1))
                    assert event is not None

                    # And it does not have errors
                    assert event[FIELD_EVENT_ERRORS] is None


@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["plate_456"])
@pytest.mark.parametrize("cherrytrack_source_plates_response", [{"errors": ["One error", "Another error"]}])
@pytest.mark.parametrize("cherrytrack_mock_source_plates_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_post_event_partially_completed_with_error_accessing_cherrytrack_for_samples_info(
    app,
    client,
    biosero_auth_headers,
    source_plates,
    run_id,
    clear_events,
    source_barcode,
    destination_barcode,
    mocked_rabbit_channel,
    mocked_responses,
    cherrytrack_mock_source_plates,
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
                        "automation_system_run_id": run_id,
                        "barcode": source_barcode,
                        "event_type": "lh_biosero_cp_source_completed",
                        "user_id": "user1",
                        "robot": "BHRB0001",
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
                    "base": ["Response from Cherrytrack is not OK: One error,Another error"]
                }


def test_post_event_partially_completed_with_validation_error_after_storing_in_mongo(
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
                        "event_type": "lh_biosero_cp_source_completed",
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
                    "plate_barcode": ["'barcode' should not contain any whitespaces"],
                    "robot_serial_number": ["'robot' should not contain any whitespaces"],
                    "source_plate_uuid": ["'barcode' should not contain any whitespaces"],
                    "picked_samples_from_source": ["'barcode' should not contain any whitespaces"],
                    "robot_uuid": ["'robot' should not contain any whitespaces"],
                }
