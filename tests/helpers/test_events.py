from datetime import datetime
from unittest.mock import patch
from uuid import uuid4

from lighthouse.constants.fields import (
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
)
from lighthouse.helpers.events import (
    construct_destination_plate_message_subject,
    construct_mongo_sample_message_subject,
    construct_robot_message_subject,
    construct_source_plate_message_subject,
    get_message_timestamp,
    get_robot_uuid,
    get_routing_key,
)

# ---------- tests helpers ----------


def any_robot_info(app):
    return next((serial_num, robot["uuid"]) for serial_num, robot in app.config["BECKMAN_ROBOTS"].items())


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


# ---------- get_robot_uuid tests ----------


def test_get_robot_uuid_returns_none_no_config_option(app):
    with app.app_context():
        del app.config["BECKMAN_ROBOTS"]

        result = get_robot_uuid("BKRB0001")
        assert result is None


def test_get_robot_uuid_returns_none_no_matching_robot(app):
    with app.app_context():
        result = get_robot_uuid("no matching robot")
        assert result is None


def test_get_robot_uuid_returns_expected_uuid(app):
    with app.app_context():
        test_robot_serial_number, test_robot_uuid = any_robot_info(app)
        result = get_robot_uuid(test_robot_serial_number)

        assert result == test_robot_uuid


# ---------- construct_robot_message_subject tests ----------


def test_construct_robot_message_subject(app):
    test_robot_serial_number, test_robot_uuid = any_robot_info(app)

    correct_subject = {
        "role_type": "robot",
        "subject_type": "robot",
        "friendly_name": test_robot_serial_number,
        "uuid": test_robot_uuid,
    }

    assert construct_robot_message_subject(test_robot_serial_number, test_robot_uuid) == correct_subject


# ---------- construct_mongo_sample_message_subject tests ----------


def test_construct_mongo_sample_message_subject(app):
    test_sample = {
        FIELD_ROOT_SAMPLE_ID: "MCM001",
        FIELD_RNA_ID: "rna_1",
        FIELD_LAB_ID: "Lab 1",
        FIELD_RESULT: "Positive",
        FIELD_LH_SAMPLE_UUID: "17be6834-06e7-4ce1-8413-9d8667cb9022",
    }

    expected_subject = {
        "role_type": "sample",
        "subject_type": "sample",
        "friendly_name": "MCM001__rna_1__Lab 1__Positive",
        "uuid": "17be6834-06e7-4ce1-8413-9d8667cb9022",
    }

    result = construct_mongo_sample_message_subject(test_sample)
    assert result == expected_subject


# ---------- construct_source_plate_message_subject tests ----------


def test_construct_source_plate_message_subject():
    test_barcode = "BAC123"
    test_uuid = "17be6834-06e7-4ce1-8413-9d8667cb9022"

    expected_subject = {
        "role_type": "cherrypicking_source_labware",
        "subject_type": "plate",
        "friendly_name": test_barcode,
        "uuid": test_uuid,
    }

    result = construct_source_plate_message_subject(test_barcode, test_uuid)
    assert result == expected_subject


# ---------- get_message_timestamp tests ----------


def test_get_message_timestamp_returns_expected_datetime():
    timestamp = datetime.now()
    with patch("lighthouse.helpers.events.datetime") as mock_datetime:
        mock_datetime.now().isoformat.return_value = timestamp

        result = get_message_timestamp()

        assert result == timestamp
        mock_datetime.now().isoformat.assert_called_with(timespec="seconds")
