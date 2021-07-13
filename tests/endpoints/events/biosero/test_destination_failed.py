from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest

from lighthouse.classes.beckman import Beckman
from lighthouse.classes.biosero import Biosero
from lighthouse.constants.fields import FIELD_EVENT_ERRORS
from lighthouse.helpers.mongo import get_event_with_uuid

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


def test_post_destination_completed_missing_barcode(app, client, lighthouse_ui_auth_headers, clear_events):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "user_id": "user1",
                "event_type": Biosero.EVENT_DESTINATION_FAILED,
            },
            headers=lighthouse_ui_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "baracoda_mock_responses",
    [
        {
            "TC1": {"barcodes_group": {"id": 1, "barcodes": ["COGUK1", "COGUK2"]}},
        }
    ],
)
@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_post_event_partially_completed(
    app,
    client,
    lighthouse_ui_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    source_plates,
    run_id,
    mocked_responses,
    cherrytrack_mock_run_info,
    samples_from_cherrytrack_into_mongo,
    centres,
    destination_barcode,
    mlwh_samples_in_cherrytrack,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
    baracoda_mock_barcodes_group,
    baracoda_mock_responses,
):
    with app.app_context():
        with patch(
            "lighthouse.hooks.events.uuid4",
            side_effect=[int_to_uuid(1)],
        ):
            with patch(
                "lighthouse.classes.messages.warehouse_messages.uuid4",
                side_effect=[int_to_uuid(2), int_to_uuid(3), int_to_uuid(4), int_to_uuid(5)],
            ):
                with patch(
                    "lighthouse.classes.events.PlateEvent.message_timestamp",
                    "mytime",
                ):
                    failure_type = Beckman.getFailureTypes()[0].get("type")
                    response = client.post(
                        "/events",
                        data={
                            "barcode": "HT-1234",
                            "event_type": Biosero.EVENT_DESTINATION_FAILED,
                            "failure_type": failure_type,
                            "user_id": "user1",
                        },
                        headers=lighthouse_ui_auth_headers,
                    )

                    # Test creates the event
                    assert response.status_code == HTTPStatus.CREATED

                    event_message = (
                        '{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "' + Biosero.EVENT_DESTINATION_FAILED + '", '
                            '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                            '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId1__plate_123_A01__centre_1__Positive", "uuid": "aLighthouseUUID1"}, '
                            '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                            '"aRootSampleId3__plate_123_A03__centre_1__Positive", "uuid": "aLighthouseUUID3"}, '
                            '{"role_type": "control", "subject_type": "sample", "friendly_name": '
                            '"positive control: DN1234_A1", '
                            '"uuid": "' + int_to_uuid(2) + '"}, '
                            '{"role_type": "control", "subject_type": "sample", "friendly_name": '
                            '"negative control: DN1234_A1", '
                            '"uuid": "' + int_to_uuid(3) + '"}, '
                            '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                            '"friendly_name": "plate_123", "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc"}, '
                            '{"role_type": "cherrypicking_destination_labware", "subject_type": "plate", '
                            '"friendly_name": "HT-1234", "uuid": "' + int_to_uuid(4) + '"}, '
                            '{"role_type": "robot", "subject_type": "robot", "friendly_name": "CPA", '
                            '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}, '
                            '{"role_type": "run", "subject_type": "run", "friendly_name": 3, '
                            '"uuid": "' + int_to_uuid(5) + '"}'
                            '], "metadata": {"failure_type": ' + failure_type + '}}, "lims": "LH_TEST"}'
                        )
                    )

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key=f"test.event.{ Biosero.EVENT_DESTINATION_FAILED }",
                        body=event_message,
                    )

                    # The record is there
                    event = get_event_with_uuid(int_to_uuid(1))
                    assert event is not None

                    # And it does not have errors
                    assert event[FIELD_EVENT_ERRORS] is None
