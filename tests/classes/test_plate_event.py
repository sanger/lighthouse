from lighthouse.classes.plate_event import PlateEvent, EventNotInitialized
from pytest import raises
from datetime import datetime
from unittest.mock import MagicMock


class TestDummy(PlateEvent):
    def _create_message(self):
        return None


def test_source_partial_new(app):
    event = TestDummy("source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
    assert event.get_event_type() == "source_partial"


def test_process_event_uninitialized(app):
    event = TestDummy(name="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
    with raises(EventNotInitialized):
        event.process_event()


def test_initialize_event(app):
    event = TestDummy(name="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
    with raises(EventNotInitialized):
        event.initialize_event({"_created": datetime.now()})
        event.initialize_event({"event_wh_uuid": "uuid"})

    event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})


def test_process_event(app):
    with app.app_context():
        event = TestDummy(name="source_partial", plate_type=PlateEvent.PlateTypeEnum.SOURCE)
        event._create_message = MagicMock(name="_create_message")  # type: ignore
        event._send_warehouse_message = MagicMock(name="_send_warehouse_message")  # type: ignore

        event.initialize_event({"event_wh_uuid": "uuid", "_created": datetime.now()})
        event.process_event()

        event._create_message.assert_called_once()
        event._send_warehouse_message.assert_called_once()
