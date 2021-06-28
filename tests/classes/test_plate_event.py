from lighthouse.classes.plate_event import PlateEvent, EventNotInitialized
from pytest import raises
from datetime import datetime
from unittest.mock import MagicMock, patch
from lighthouse.classes.plate_event import EVENT_NOT_INITIALIZED, EVENT_INITIALIZED


class TestDummy(PlateEvent):
    def _create_message(self):
        return None


def test_source_partial_new(app):
    event = TestDummy("source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
    assert event.event_type == "source_partial"
    assert event.state == EVENT_NOT_INITIALIZED


def test_process_event_uninitialized(app):
    event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
    with raises(EventNotInitialized):
        event.process_event()


def test_initialize_event(app):
    mytime = datetime.now()
    event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)

    with raises(EventNotInitialized):
        event.initialize_event({"_created": mytime})
    assert event.state == EVENT_NOT_INITIALIZED

    with raises(EventNotInitialized):
        event.initialize_event({"event_wh_uuid": "uuid"})
    assert event.state == EVENT_NOT_INITIALIZED

    event.initialize_event({"event_wh_uuid": "uuid", "_created": mytime})
    assert event.event_uuid == "uuid"
    assert event.message_timestamp == mytime.isoformat(timespec="seconds")
    assert event.state == EVENT_INITIALIZED


def test_process_event(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        with patch.object(event, "_create_message") as create_message:
            with patch.object(event, "send_warehouse_message") as send_warehouse_message:
                event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})
                event.process_event()

                create_message.assert_called_once()
                send_warehouse_message.assert_called_once()


def test_build_new_warehouse_message(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        with raises(EventNotInitialized):
            event.build_new_warehouse_message()

        event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})
        assert event.build_new_warehouse_message() is not None


def test_errors(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        assert event.errors == {}
        mock = MagicMock()
        mock.errors = ["an error"]
        mock2 = MagicMock()
        mock2.errors = ["another error", "other one"]
        event.properties["myprop1"] = mock
        event.properties["myprop2"] = mock2
        assert event.errors == {"myprop1": ["an error"], "myprop2": ["another error", "other one"]}


def test_is_valid(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        assert event.is_valid() is True

        mock = MagicMock()
        mock.is_valid = MagicMock(name="is_valid", return_value=True)
        event.properties["myprop1"] = mock
        assert event.is_valid() is True

        mock2 = MagicMock()
        mock2.is_valid = MagicMock(name="is_valid", return_value=False)
        event.properties["myprop2"] = mock2
        assert event.is_valid() is False


def test_process_errors(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})

        with patch("lighthouse.classes.plate_event.set_errors_to_event") as mock:
            event.process_errors()
            mock.assert_not_called()

            mock2 = MagicMock()
            mock2.errors = ["an error"]
            event.properties["myprop2"] = mock2
            event.process_errors()
            mock.assert_called_once_with("uuid", {"myprop2": ["an error"]})


def test_process_exception(app):
    with app.app_context():
        event = TestDummy(event_type="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})

        exc = Exception("boom!")

        with patch("lighthouse.classes.plate_event.set_errors_to_event") as mock:
            event.process_exception(exc)
            mock.assert_called_once_with("uuid", {"base": ["boom!"]})
