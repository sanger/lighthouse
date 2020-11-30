from uuid import uuid4
from unittest.mock import patch
from lighthouse.helpers.events import (
    get_routing_key,
    construct_destination_plate_message_subject,
)


# ---------- get_routing_key tests ----------


def test_get_routing_key(app):
    with app.app_context():
        test_event_type = "test_event_type"
        result = get_routing_key(test_event_type)

        assert result == f"test.event.{test_event_type}"


# ---------- construct_destination_plate_message_subject tests ----------


def test_construct_destination_plate_message_subject():
    test_uuid = uuid4()
    with patch("lighthouse.helpers.events.uuid4", return_value=test_uuid):
        barcode = "ABC123"
        expected_subject = {
            "role_type": "cherrypicking_destination_labware",
            "subject_type": "plate",
            "friendly_name": barcode,
            "uuid": str(test_uuid),
        }

        result = construct_destination_plate_message_subject(barcode)
        assert result == expected_subject
        

