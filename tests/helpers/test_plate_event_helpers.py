import pytest
from unittest.mock import patch
from lighthouse.messages.message import Message
from lighthouse.helpers.plate_events import (
    construct_event_message,
    construct_source_plate_not_recognised_message,
    construct_source_plate_no_map_data_message,
    construct_source_plate_all_negatives_message,
    construct_source_plate_completed_message,
    construct_source_plate_message_subject,
)
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_NOT_RECOGNISED,
    PLATE_EVENT_SOURCE_NO_MAP_DATA,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
)


# ---------- test helpers ----------


@pytest.fixture
def mock_robot_helpers():
    with patch("lighthouse.helpers.plate_events.construct_robot_message_subject") as mock_construct:
        with patch("lighthouse.helpers.plate_events.get_robot_uuid") as mock_get:
            yield mock_get, mock_construct


@pytest.fixture
def mock_get_source_plate_uuid():
    with patch("lighthouse.helpers.plate_events.get_source_plate_uuid") as mock_get_uuid:
        yield mock_get_uuid


# ---------- construct_event_messages tests ----------


def test_construct_event_message_unrecognised_event():
    errors, message = construct_event_message("not a real event", {})

    assert len(errors) == 1
    assert message is None


def test_construct_event_message_source_complete():
    with patch(
        "lighthouse.helpers.plate_events.construct_source_plate_completed_message"
    ) as mock_construct_source_completed_message:
        test_return_value = ([], Message("test message"))
        mock_construct_source_completed_message.return_value = test_return_value

        test_params = {"test_key": "test_value"}
        result = construct_event_message(PLATE_EVENT_SOURCE_COMPLETED, test_params)

        mock_construct_source_completed_message.assert_called_with(test_params)
        assert result == test_return_value


def test_construct_event_message_source_not_recognised():
    with patch(
        "lighthouse.helpers.plate_events.construct_source_plate_not_recognised_message"
    ) as mock_construct_source_not_recognised_message:
        test_return_value = ([], Message("test message"))
        mock_construct_source_not_recognised_message.return_value = test_return_value

        test_params = {"test_key": "test_value"}
        result = construct_event_message(PLATE_EVENT_SOURCE_NOT_RECOGNISED, test_params)

        mock_construct_source_not_recognised_message.assert_called_with(test_params)
        assert result == test_return_value


def test_construct_event_message_source_no_map_data():
    with patch(
        "lighthouse.helpers.plate_events.construct_source_plate_no_map_data_message"
    ) as mock_construct_source_no_map_data_message:
        test_return_value = ([], Message("test message"))
        mock_construct_source_no_map_data_message.return_value = test_return_value

        test_params = {"test_key": "test_value"}
        result = construct_event_message(PLATE_EVENT_SOURCE_NO_MAP_DATA, test_params)

        mock_construct_source_no_map_data_message.assert_called_with(test_params)
        assert result == test_return_value


def test_construct_event_message_source_all_negatives():
    with patch(
        "lighthouse.helpers.plate_events.construct_source_plate_all_negatives_message"
    ) as mock_construct_source_all_negatives_message:
        test_return_value = ([], Message("test message"))
        mock_construct_source_all_negatives_message.return_value = test_return_value

        test_params = {"test_key": "test_value"}
        result = construct_event_message(PLATE_EVENT_SOURCE_ALL_NEGATIVES, test_params)

        mock_construct_source_all_negatives_message.assert_called_with(test_params)
        assert result == test_return_value


# ---------- construct_source_plate_not_recognised_message tests ----------


def test_construct_source_plate_not_recognised_message_errors_without_user_id():
    test_params = {"robot": "12345"}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"robot": "12345", "user_id": ""}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_not_recognised_message_errors_without_robot():
    test_params = {"user_id": "test_user"}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"user_id": "test_user", "robot": ""}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_not_recognised_message_errors_with_failure_getting_robot_uuid(
    mock_robot_helpers,
):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.side_effect = Exception("Boom!")
    test_params = {"user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "An unexpected error occurred" in errors[0]
    assert message is None


def test_construct_source_plate_not_recognised_message_errors_without_robot_uuid(
    mock_robot_helpers,
):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.return_value = None
    test_params = {"user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_not_recognised_message(test_params)

    assert len(errors) == 1
    assert "Unable to determine a uuid for robot" in errors[0]
    assert message is None


def test_construct_source_plate_not_recognised_message_creates_expected_message(
    app, mock_robot_helpers
):
    _, mock_construct = mock_robot_helpers
    test_robot_subject = {"test robot": "this is a robot"}
    mock_construct.return_value = test_robot_subject
    with app.app_context():
        with patch("lighthouse.helpers.plate_events.Message") as mock_message:
            test_user_id = "test_user"
            test_params = {"user_id": test_user_id, "robot": "12345"}
            errors, _ = construct_source_plate_not_recognised_message(test_params)

            assert len(errors) == 0

            args, _ = mock_message.call_args
            message_content = args[0]

            assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

            event = message_content["event"]
            assert event["uuid"] is not None
            assert event["event_type"] == PLATE_EVENT_SOURCE_NOT_RECOGNISED
            assert event["occured_at"] is not None
            assert event["user_identifier"] == test_user_id

            subjects = event["subjects"]
            assert len(subjects) == 1
            assert test_robot_subject in subjects  # robot subject


# ---------- construct_source_plate_no_map_data_message tests ----------


def test_construct_source_plate_no_map_data_message_errors_without_barcode():
    test_params = {"user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "", "user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_no_map_data_message_errors_without_user_id():
    test_params = {"barcode": "ABC123", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_no_map_data_message_errors_without_robot():
    test_params = {"barcode": "ABC123", "user_id": "test user"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "test user", "robot": ""}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_no_map_data_message_errors_with_failure_getting_robot_uuid(
    mock_robot_helpers,
):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.side_effect = Exception("Boom!")
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "An unexpected error occurred" in errors[0]
    assert message is None


def test_construct_source_plate_no_map_data_message_errors_without_robot_uuid(mock_robot_helpers):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.return_value = None
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_no_map_data_message(test_params)

    assert len(errors) == 1
    assert "Unable to determine a uuid for robot" in errors[0]
    assert message is None


def test_construct_source_plate_no_map_data_message_errors_with_failure_getting_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.side_effect = Exception("Boom!")
    with app.app_context():
        test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
        errors, message = construct_source_plate_no_map_data_message(test_params)

        assert len(errors) == 1
        assert "An unexpected error occurred" in errors[0]
        assert message is None


def test_construct_source_plate_no_map_data_message_errors_without_source_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.return_value = None
    with app.app_context():
        test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
        errors, message = construct_source_plate_no_map_data_message(test_params)

        assert len(errors) == 1
        assert "Unable to determine a uuid for source plate" in errors[0]
        assert message is None


def test_construct_source_plate_no_map_data_message_creates_expected_message(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    _, mock_construct = mock_robot_helpers
    test_robot_subject = {"test robot": "this is a robot"}
    mock_construct.return_value = test_robot_subject
    with app.app_context():
        test_source_plate_subject = {"test source plate": "this is a source plate"}
        with patch(
            "lighthouse.helpers.plate_events.construct_source_plate_message_subject",
            return_value=test_source_plate_subject,
        ):
            with patch("lighthouse.helpers.plate_events.Message") as mock_message:
                test_barcode = "ABC123"
                test_user_id = "test_user"
                test_params = {
                    "barcode": test_barcode,
                    "user_id": test_user_id,
                    "robot": "12345",
                }
                errors, _ = construct_source_plate_no_map_data_message(test_params)

                assert len(errors) == 0

                args, _ = mock_message.call_args
                message_content = args[0]

                assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                event = message_content["event"]
                assert event["uuid"] is not None
                assert event["event_type"] == PLATE_EVENT_SOURCE_NO_MAP_DATA
                assert event["occured_at"] is not None
                assert event["user_identifier"] == test_user_id

                subjects = event["subjects"]
                assert len(subjects) == 2
                assert test_robot_subject in subjects  # robot subject
                assert test_source_plate_subject in subjects  # source plate subject


# ---------- construct_source_plate_all_negatives_message tests ----------


def test_construct_source_plate_all_negatives_message_errors_without_barcode():
    test_params = {"user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "", "user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_all_negatives_message_errors_without_user_id():
    test_params = {"barcode": "ABC123", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_all_negatives_message_errors_without_robot():
    test_params = {"barcode": "ABC123", "user_id": "test user"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "test user", "robot": ""}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_all_negatives_message_errors_with_failure_getting_robot_uuid(
    mock_robot_helpers,
):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.side_effect = Exception("Boom!")
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "An unexpected error occurred" in errors[0]
    assert message is None


def test_construct_source_plate_all_negatives_message_errors_without_robot_uuid(mock_robot_helpers):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.return_value = None
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_all_negatives_message(test_params)

    assert len(errors) == 1
    assert "Unable to determine a uuid for robot" in errors[0]
    assert message is None


def test_construct_source_plate_all_negatives_message_errors_with_failure_getting_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.side_effect = Exception("Boom!")
    with app.app_context():
        test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
        errors, message = construct_source_plate_all_negatives_message(test_params)

        assert len(errors) == 1
        assert "An unexpected error occurred" in errors[0]
        assert message is None


def test_construct_source_plate_all_negatives_message_errors_without_source_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.return_value = None
    with app.app_context():
        test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
        errors, message = construct_source_plate_all_negatives_message(test_params)

        assert len(errors) == 1
        assert "Unable to determine a uuid for source plate" in errors[0]
        assert message is None


def test_construct_source_plate_all_negatives_message_creates_expected_message(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    _, mock_construct = mock_robot_helpers
    test_robot_subject = {"test robot": "this is a robot"}
    mock_construct.return_value = test_robot_subject
    with app.app_context():
        test_source_plate_subject = {"test source plate": "this is a source plate"}
        with patch(
            "lighthouse.helpers.plate_events.construct_source_plate_message_subject",
            return_value=test_source_plate_subject,
        ):
            with patch("lighthouse.helpers.plate_events.Message") as mock_message:
                test_barcode = "ABC123"
                test_user_id = "test_user"
                test_params = {
                    "barcode": test_barcode,
                    "user_id": test_user_id,
                    "robot": "12345",
                }
                errors, _ = construct_source_plate_all_negatives_message(test_params)

                assert len(errors) == 0

                args, _ = mock_message.call_args
                message_content = args[0]

                assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                event = message_content["event"]
                assert event["uuid"] is not None
                assert event["event_type"] == PLATE_EVENT_SOURCE_ALL_NEGATIVES
                assert event["occured_at"] is not None
                assert event["user_identifier"] == test_user_id

                subjects = event["subjects"]
                assert len(subjects) == 2
                assert test_robot_subject in subjects  # robot subject
                assert test_source_plate_subject in subjects  # source plate subject


# ---------- construct_source_plate_completed_message tests ----------


def test_construct_source_plate_completed_message_errors_without_barcode():
    test_params = {"user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "", "user_id": "test user", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_completed_message_errors_without_user_id():
    test_params = {"barcode": "ABC123", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_completed_message_errors_without_robot():
    test_params = {"barcode": "ABC123", "user_id": "test user"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None

    test_params = {"barcode": "ABC123", "user_id": "test user", "robot": ""}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "'barcode', 'user_id' and 'robot' are required" in errors[0]
    assert message is None


def test_construct_source_plate_completed_message_errors_with_failure_getting_robot_uuid(
    mock_robot_helpers,
):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.side_effect = Exception("Boom!")
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "An unexpected error occurred" in errors[0]
    assert message is None


def test_construct_source_plate_completed_message_errors_without_robot_uuid(mock_robot_helpers):
    mock_get_uuid, _ = mock_robot_helpers
    mock_get_uuid.return_value = None
    test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
    errors, message = construct_source_plate_completed_message(test_params)

    assert len(errors) == 1
    assert "Unable to determine a uuid for robot" in errors[0]
    assert message is None


def test_construct_source_plate_completed_message_errors_with_failure_getting_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.side_effect = Exception("Boom!")
    with app.app_context():
        test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
        errors, message = construct_source_plate_completed_message(test_params)

        assert len(errors) == 1
        assert "An unexpected error occurred" in errors[0]
        assert message is None


def test_construct_source_plate_completed_message_errors_without_source_plate_uuid(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    mock_get_source_plate_uuid.return_value = None
    with app.app_context():
        with patch("lighthouse.helpers.plate_events.get_source_plate_uuid", return_value=None):
            test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
            errors, message = construct_source_plate_completed_message(test_params)

            assert len(errors) == 1
            assert "Unable to determine a uuid for source plate" in errors[0]
            assert message is None


def test_construct_source_plate_completed_message_errors_with_failure_getting_samples(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    with app.app_context():
        test_source_plate_uuid = "3a06a935-0029-49ea-81bc-e5d8eeb1319e"
        with patch(
            "lighthouse.helpers.plate_events.get_source_plate_uuid",
            return_value=test_source_plate_uuid,
        ):
            with patch(
                "lighthouse.helpers.plate_events.get_samples_in_source_plate",
                side_effect=Exception("Boom!"),
            ):
                test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
                errors, message = construct_source_plate_completed_message(test_params)

                assert len(errors) == 1
                assert "An unexpected error occurred" in errors[0]
                assert message is None


def test_construct_source_plate_completed_message_errors_without_samples(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    with app.app_context():
        test_source_plate_uuid = "3a06a935-0029-49ea-81bc-e5d8eeb1319e"
        with patch(
            "lighthouse.helpers.plate_events.get_source_plate_uuid",
            return_value=test_source_plate_uuid,
        ):
            with patch(
                "lighthouse.helpers.plate_events.get_samples_in_source_plate", return_value=None
            ):
                test_params = {"barcode": "ABC123", "user_id": "test_user", "robot": "12345"}
                errors, message = construct_source_plate_completed_message(test_params)

                assert len(errors) == 1
                assert "Unable to determine samples that belong to source plate" in errors[0]
                assert message is None


def test_construct_source_plate_completed_message_creates_expected_message(
    app, mock_robot_helpers, mock_get_source_plate_uuid
):
    _, mock_construct = mock_robot_helpers
    test_robot_subject = {"test robot": "this is a robot"}
    mock_construct.return_value = test_robot_subject
    with app.app_context():
        test_source_plate_subject = {"test source plate": "this is a source plate"}
        with patch(
            "lighthouse.helpers.plate_events.construct_source_plate_message_subject",
            return_value=test_source_plate_subject,
        ):
            test_sample_subject = {"test sample": "this is a sample"}
            with patch(
                "lighthouse.helpers.plate_events.construct_mongo_sample_message_subject",
                return_value=test_sample_subject,
            ):
                test_samples = [
                    {"test key": "test sample 1"},
                    {"test key": "test sample 2"},
                ]
                with patch(
                    "lighthouse.helpers.plate_events.get_samples_in_source_plate",
                    return_value=test_samples,
                ):
                    with patch("lighthouse.helpers.plate_events.Message") as mock_message:
                        test_barcode = "ABC123"
                        test_user_id = "test_user"
                        test_params = {
                            "barcode": test_barcode,
                            "user_id": test_user_id,
                            "robot": "12345",
                        }
                        errors, _ = construct_source_plate_completed_message(test_params)

                        assert len(errors) == 0

                        args, _ = mock_message.call_args
                        message_content = args[0]

                        assert message_content["lims"] == app.config["RMQ_LIMS_ID"]

                        event = message_content["event"]
                        assert event["uuid"] is not None
                        assert event["event_type"] == PLATE_EVENT_SOURCE_COMPLETED
                        assert event["occured_at"] is not None
                        assert event["user_identifier"] == test_user_id

                        subjects = event["subjects"]
                        assert len(subjects) == 4
                        assert test_robot_subject in subjects  # robot subject
                        assert test_source_plate_subject in subjects  # source plate subjects
                        assert subjects.count(test_sample_subject) == 2  # sample subjects
