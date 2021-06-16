from http import HTTPStatus
import responses
from unittest.mock import patch
from lighthouse.helpers.mongo import get_event_with_uuid
from lighthouse.constants.fields import FIELD_EVENT_ERRORS

from typing import Dict


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


def test_post_event_partially_completed(
    app, client, biosero_auth_headers, mocked_rabbit_channel, mocked_cherrytrack_responses
):
    with app.app_context():
        with patch("lighthouse.hooks.events.uuid4", side_effect=[1, 2, 3, 4]):
            with patch(
                "lighthouse.classes.plate_event.PlateEvent.get_message_timestamp",
                return_value="mytime",
            ):
                response = client.post(
                    "/events",
                    data={
                        "automation_system_run_id": "2",
                        "barcode": "aBarcode",
                        "event_type": "lh_biosero_cp_source_partial",
                        "user_id": "user1",
                        "robot": "BHRB0001",
                    },
                    headers=biosero_auth_headers,
                )

                # Test creates the event
                assert response.status_code == HTTPStatus.CREATED

                mocked_rabbit_channel.basic_publish.assert_called_with(
                    exchange="lighthouse.test.examples",
                    routing_key="test.event.lh_biosero_cp_source_partial",
                    body=(
                        '{"event": {"uuid": "1", "event_type": "lh_biosero_cp_source_partial", '
                        '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                        '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                        '"aRootSampleId2__aRNAId2__aLabId1__Positive", "uuid": "aLighthouseUUID2"}, '
                        '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                        '"friendly_name": "aBarcode", "uuid": "1234"}, {"role_type": "robot", '
                        '"subject_type": "robot", "friendly_name": "BHRB0001", "uuid": '
                        '"e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}], "metadata": {}}, "lims": "LH_TEST"}'
                    ),
                )

                assert get_event_with_uuid("1") is not None


def test_post_event_partially_completed_with_error_accessing_cherrytrack(
    app, client, biosero_auth_headers, mocked_rabbit_channel, mocked_responses
):
    with app.app_context():
        with patch("lighthouse.hooks.events.uuid4", side_effect=[1, 2, 3, 4]):
            with patch(
                "lighthouse.classes.plate_event.PlateEvent.get_message_timestamp",
                return_value="mytime",
            ):
                run_id = 3
                run_url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

                expected_run_response: Dict[str, str] = {}

                mocked_responses.add(
                    responses.GET,
                    run_url,
                    json=expected_run_response,
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

                response = client.post(
                    "/events",
                    data={
                        "automation_system_run_id": "3",
                        "barcode": "aBarcode",
                        "event_type": "lh_biosero_cp_source_partial",
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
                event = get_event_with_uuid("1")
                assert event is not None

                # And it has errors
                assert event[FIELD_EVENT_ERRORS] == {"base": ["Response from Cherrytrack is not OK"]}
