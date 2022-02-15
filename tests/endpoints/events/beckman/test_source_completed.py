from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest

from lighthouse.constants.fields import FIELD_EVENT_ERRORS
from lighthouse.helpers.mongo import get_event_with_uuid
from lighthouse.classes.beckman_v3 import Beckman

CACHE = {}


def int_to_uuid(value: int) -> str:
    if value not in CACHE:
        CACHE[value] = str(uuid4())
    return CACHE[value]

def test_event_source_completed_missing_barcode(
    app,
    client,
    beckman_auth_headers,
    clear_events,
):

    with app.app_context():
        response = client.get(
                    "/v3/plate-events/create?barcode=&event_type=lh_beckman_cp_source_completed&robot=BKRB0001&user_id=RC34",
                    headers=beckman_auth_headers,
                )

        response_errors = response.json.get('_issues')
        assert "'barcode' should not be an empty string" in response_errors.get('plate_barcode')


@pytest.mark.parametrize("source_barcode", ["GLS-GP-016240"])
@pytest.mark.parametrize("robot", ["BKRB0001"])
@pytest.mark.parametrize("user_id", ["LT1"])
def test_get_event_source_completed(
    app,
    client,
    beckman_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    #source_plates,
    positive_samples_in_source_plate,
    source_barcode,
    robot,
    user_id,
    mocked_responses,
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
                    test_source_plate_uuid = "3a06a935-0029-49ea-81bc-e5d8eeb1319e"

                    with patch(
                        "lighthouse.classes.services.mongo.MongoServiceMixin.get_source_plate_uuid",
                        return_value=test_source_plate_uuid,
                    ):
                        with patch(
                            "lighthouse.classes.services.mongo.MongoServiceMixin.get_positive_samples_in_source_plate",
                            return_value=positive_samples_in_source_plate,
                        ):
                            message = WarehouseMessage("mytype", "myuuid", "at some point")
                            message.add_subject("myrole", "mysubject", "myname", "myuuid"
                            with patch("lighthouse.classes.services.labwhere.set_locations_in_labwhere") as mocked_labwhere:

                                response = client.get(
                                    "/v3/plate-events/create?barcode=" + source_barcode +
                                    "&event_type=" + Beckman.EVENT_SOURCE_COMPLETED +
                                    "&robot=" + robot +
                                    "&user_id=" + user_id,
                                    headers=beckman_auth_headers,
                                )

                        # Test creates the event
                        assert response.status_code == HTTPStatus.CREATED
"""
                        mocked_rabbit_channel.basic_publish.assert_called_with(
                            exchange="lighthouse.test.examples",
                            routing_key=f"test.event.{ Beckman.EVENT_SOURCE_COMPLETED }",
                            body='{"event": {"uuid": "'
                            + int_to_uuid(1)
                            + (
                                '", "event_type": "' + Beckman.EVENT_SOURCE_COMPLETED + '", '
                                '"occured_at": "mytime", "user_identifier": "user1", "subjects": '
                                '[{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                                '"aRootSampleId1__plate_123_A01__centre_1__Positive", "uuid": "aLighthouseUUID1"}, '
                                '{"role_type": "sample", "subject_type": "sample", "friendly_name": '
                                '"aRootSampleId3__plate_123_A03__centre_1__Positive", "uuid": "aLighthouseUUID3"}, '
                                '{"role_type": "cherrypicking_source_labware", "subject_type": "plate", '
                                '"friendly_name": "plate_123", "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc"}, '
                                '{"role_type": "robot", "subject_type": "robot", "friendly_name": "CPA", '
                                '"uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"}, '
                                '{"role_type": "run", "subject_type": "run", "friendly_name": 3, '
                                '"uuid": "' + int_to_uuid(2) + '"}'
                                '], "metadata": {}}, "lims": "LH_TEST"}'
                            ),
                        )

                        mocked_labwhere.assert_called_once_with(
                            labware_barcodes=[source_barcode],
                            location_barcode=app.config["LABWHERE_DESTROYED_BARCODE"],
                            user_barcode="CPA",
                        )

                        # The record is there
                        event = get_event_with_uuid(int_to_uuid(1))
                        assert event is not None

                        # And it does not have errors
                        assert event[FIELD_EVENT_ERRORS] is None
"""


