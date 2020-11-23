from unittest.mock import patch
from lighthouse.messages.message import Message
from lighthouse.helpers.plate_events import (
    construct_event_message,
    get_routing_key,
)
from lighthouse.constants import (
    PLATE_EVENT_SOURCE_COMPLETED,
    PLATE_EVENT_SOURCE_NOT_RECOGNISED,
    PLATE_EVENT_SOURCE_NO_MAP_DATA,
    PLATE_EVENT_SOURCE_ALL_NEGATIVES,
)


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


def test_get_routing_key(app):
    with app.app_context():
        test_event_type = "test_event_type"
        result = get_routing_key(test_event_type)

        assert result == f"test.event.{test_event_type}"
