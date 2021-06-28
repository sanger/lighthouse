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


def test_post_event_source_no_pickable_samples_missing_barcode(
    app, client, biosero_auth_headers, clear_events_when_finish
):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "automation_system_run_id": 123,
                "event_type": "lh_biosero_cp_source_no_pickable_samples",
                "user_id": "user1",
                "robot": "roboto",
            },
            headers=biosero_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("run_id", [3])
def test_post_event_source_no_pickable_samples(
    app,
    client,
    biosero_auth_headers,
    clear_events_when_finish,
    mocked_rabbit_channel,
    source_plates,
    run_id,
    mocked_responses,
    cherrytrack_mock_run_info,
    samples_from_cherrytrack_into_mongo,
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.events.uuid4",
            side_effect=[int_to_uuid(1)],
        ):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[int_to_uuid(2)]):

                with patch(
                    "lighthouse.classes.plate_event.PlateEvent.message_timestamp",
                    "mytime",
                ):
                    response = client.post(
                        "/events",
                        data={
                            "automation_system_run_id": 3,
                            "barcode": "plate_123",
                            "event_type": "lh_biosero_cp_source_no_pickable_samples",
                            "user_id": "user1",
                            "robot": "BHRB0001",
                        },
                        headers=biosero_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key="test.event.lh_biosero_cp_source_no_pickable_samples",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "lh_biosero_cp_source_no_pickable_samples", '
                            '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                            '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId1__plate_123_A01__centre_1__Positive", "uuid": "aLighthouseUUID1"}, '
                            '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId2__plate_123_A02__centre_2__Positive", "uuid": "aLighthouseUUID2"}, '
                            '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId3__plate_123_A03__centre_1__Positive", "uuid": "aLighthouseUUID3"}, '
                            '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId4__plate_123_A04__centre_2__Positive", "uuid": "aLighthouseUUID4"}, '
                            '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                            '"friendly_name": "plate_123", "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc"}, '
                            '{"role_type": "robot", "subject_type": "robot", "friendly_name": "BHRB0001", '
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


# TODO duplicate of test+all_source_negatives?
@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("cherrytrack_run_info_response", [{"errors": ["One error", "Another error"]}])
@pytest.mark.parametrize("cherrytrack_mock_run_info_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_post_event_source_no_pickable_samples_with_error_accessing_cherrytrack_for_samples_info(
    app,
    client,
    biosero_auth_headers,
    source_plates,
    run_id,
    clear_events_when_finish,
    mocked_rabbit_channel,
    mocked_responses,
    cherrytrack_mock_run_info,
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
                        "barcode": "plate_123",
                        "event_type": "lh_biosero_cp_source_no_pickable_samples",
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


def test_post_event_source_no_pickable_samples_with_validation_error_after_storing_in_mongo(
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
                        "barcode": "a Barcode",
                        "event_type": "lh_biosero_cp_source_no_pickable_samples",
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
                    "all_samples": ["'barcode' should not contain any whitespaces"],
                    "robot_uuid": ["'robot' should not contain any whitespaces"],
                }
