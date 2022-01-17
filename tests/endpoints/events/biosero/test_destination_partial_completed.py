from http import HTTPStatus
from unittest.mock import patch, MagicMock
from lighthouse.helpers.mongo import get_event_with_uuid
from lighthouse.constants.fields import FIELD_EVENT_ERRORS
from lighthouse.classes.biosero import Biosero

import pytest
from uuid import uuid4

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]


# Event source partially completed


def test_post_destination_partial_completed_missing_barcode(app, client, lighthouse_ui_auth_headers, clear_events):
    with app.app_context():
        response = client.post(
            "/events",
            data={"user_id": "user1", "event_type": Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED},
            headers=lighthouse_ui_auth_headers,
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize("cherrytrack_mock_destination_plate_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_post_destination_partial_completed_cherrytrack_fails(
    app,
    client,
    lighthouse_ui_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    source_plates,
    run_id,
    mocked_responses,
    samples_from_cherrytrack_into_mongo,
    centres,
    destination_barcode,
    mlwh_samples_in_cherrytrack,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
    cherrytrack_mock_destination_plate_status,
):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "user_id": "user1",
                "barcode": "HT-1234",
                "event_type": Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED,
            },
            headers=lighthouse_ui_auth_headers,
        )
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.parametrize("run_id", [3])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize("baracoda_mock_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
@pytest.mark.parametrize(
    "baracoda_mock_responses",
    [
        {
            "TC1": {"barcodes_group": {"id": 1, "barcodes": ["COGUK1", "COGUK2"]}},
        }
    ],
)
def test_post_destination_partial_completed_baracoda_fails(
    app,
    client,
    lighthouse_ui_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    source_plates,
    run_id,
    mocked_responses,
    samples_from_cherrytrack_into_mongo,
    centres,
    destination_barcode,
    mlwh_samples_in_cherrytrack,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
    cherrytrack_mock_destination_plate_status,
    baracoda_mock_barcodes_group,
    baracoda_mock_responses,
):
    with app.app_context():
        response = client.post(
            "/events",
            data={
                "user_id": "user1",
                "barcode": "HT-1234",
                "event_type": Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED,
            },
            headers=lighthouse_ui_auth_headers,
        )
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


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
                    mock_response_send_ss = MagicMock()
                    mock_response_send_ss.ok = True
                    with patch(
                        "lighthouse.classes.messages.sequencescape_messages.SequencescapeMessage._send_to_ss",
                        return_value=mock_response_send_ss,
                    ) as send_to_ss:

                        response = client.post(
                            "/events",
                            data={
                                "user_id": "user1",
                                "barcode": "HT-1234",
                                "event_type": Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED,
                            },
                            headers=lighthouse_ui_auth_headers,
                        )

                        # Test creates the event
                        assert response.status_code == HTTPStatus.CREATED

                        event_message = (
                            '{"event": {"uuid": "'
                            + int_to_uuid(1)
                            + (
                                '", "event_type": "' + Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED + '", '
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
                                '], "metadata": {}}, "lims": "LH_TEST"}'
                            )
                        )

                        mocked_rabbit_channel.basic_publish.assert_called_with(
                            exchange="lighthouse.test.examples",
                            routing_key=f"test.event.{ Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED }",
                            body=event_message,
                        )

                        ss_message = (
                            '{"data": {"type": "plates", "attributes": {"barcode": "HT-1234", '
                            '"purpose_uuid": "ss_uuid_plate_purpose", '
                            '"study_uuid": "ss_uuid_study", "wells": '
                            '{"H08": {"content": {"name": "plate_123_A01", "sample_description": "aRootSampleId1", '
                            '"supplier_name": "COGUK1", "phenotype": "positive", "uuid": "aLighthouseUUID1"}}, '
                            '"H12": {"content": {"name": "plate_123_A03", "sample_description": "aRootSampleId3", '
                            '"supplier_name": "COGUK2", '
                            '"phenotype": "positive", "uuid": "aLighthouseUUID3"}}, '
                            '"E10": {"content": {"supplier_name": "positive control: DN1234_A1", "control": true, '
                            '"control_type": "positive"}}, '
                            '"E11": {"content": {"supplier_name": "negative control: DN1234_A1", "control": true, '
                            '"control_type": "negative"}}}, '
                            '"events": []}}}'
                        )

                        send_to_ss.assert_called_once_with(
                            ss_url=f"{app.config['SS_URL']}/api/v2/heron/plates",
                            headers={
                                "X-Sequencescape-Client-Id": app.config["SS_API_KEY"],
                                "Content-type": "application/json",
                            },
                            data=ss_message,
                        )

                        # The record is there
                        event = get_event_with_uuid(int_to_uuid(1))
                        assert event is not None

                        # And it does not have errors
                        assert event[FIELD_EVENT_ERRORS] is None
