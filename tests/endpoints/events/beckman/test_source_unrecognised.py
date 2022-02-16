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

def test_event_source_unrecognised_missing_user_id(app, client, beckman_auth_headers, clear_events):
    with app.app_context():
        with pytest.raises(Exception) as excinfo:
            response = client.get(
                        "/v1/plate-events/create?event_type=lh_beckman_cp_source_plate_unrecognised&robot=BKRB0001&user_id=",
                        headers=beckman_auth_headers,
                    )
        
        assert "GET request needs 'user_id' in URL" in str(excinfo.value)

def test_get_event_source_unrecognised(
    app,
    client,
    beckman_auth_headers,
    clear_events,
    mocked_rabbit_channel,
    mocked_responses,
):
    with app.app_context():
        with patch("lighthouse.hooks.beckman_events.uuid4", return_value=int_to_uuid(1)):
            with patch("lighthouse.classes.messages.warehouse_messages.uuid4", side_effect=[int_to_uuid(2)]):
                with patch(
                    "lighthouse.classes.events.PlateEvent.message_timestamp",
                    "mytime",
                ):  
                    response = client.get(
                        "/v1/plate-events/create?event_type=lh_beckman_cp_source_plate_unrecognised&robot=BKRB0001&user_id=user_id",
                        headers=beckman_auth_headers,
                    )

                    assert response.status_code == HTTPStatus.OK.value

                    mocked_rabbit_channel.basic_publish.assert_called_with(
                        exchange="lighthouse.test.examples",
                        routing_key=f"test.event.{ Beckman.EVENT_SOURCE_UNRECOGNISED }",
                        body='{"event": {"uuid": "'
                        + int_to_uuid(1)
                        + (
                            '", "event_type": "' + Beckman.EVENT_SOURCE_UNRECOGNISED + '", '
                            '"occured_at": "mytime", "user_identifier": "user_id", "subjects": '
                            '[{"role_type": "robot", "subject_type": "robot", "friendly_name": "BKRB0001", '
                            '"uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b"}], '
                            '"metadata": {}}, "lims": "LH_TEST"}'
                        ),
                    )

                    
