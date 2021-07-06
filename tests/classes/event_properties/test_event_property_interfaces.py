from pytest import raises, fail
from unittest.mock import MagicMock
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.exceptions import ValidationError


class DummyEventProperty(EventPropertyAbstract):
    def add_to_warehouse_message(self, message):
        return None

    def add_to_sequencescape_message(self, message):
        return None

    def is_valid(self):
        return self._is_valid

    def value(self):
        return self._value

    # Helper methods outside of the interface
    def set_value(self, val):
        self._value = val

    def set_validation(self, valid):
        self._is_valid = valid

    def set_errors(self, errors):
        self._errors = errors


class TestEventPropertyAbstract:
    def test_init_raise_validation_error_without_params(self):
        with raises(ValidationError):
            DummyEventProperty(None)  # type: ignore

    def test_init_can_initialize_with_params(self):
        assert DummyEventProperty({}) is not None
        assert DummyEventProperty({"test": "another test"}) is not None
        assert DummyEventProperty({"user_id": "1234"}) is not None

    def test_reset_can_reset_both_errors_and_is_valid(self):
        test = DummyEventProperty({})
        test.set_validation(False)
        test.set_errors(["an error"])
        assert test.is_valid() is False
        assert test.errors == ["an error"]
        test.reset()
        assert test.is_valid() is True
        assert test.errors == []

    def test_process_validation_can_add_errors(self):
        test = DummyEventProperty({})
        test.process_validation(1 == 1, "This is right")
        assert test.errors == []
        test.process_validation(1 == 2, "This is not right")
        test.process_validation(1 == 3, "Neither")
        assert test.errors == ["This is not right", "Neither"]

    def test_validation_scope_can_supress_and_log_errors(self):
        test = DummyEventProperty({})
        mocking = MagicMock()
        try:
            with test.validation_scope():
                raise Exception("This is an error")
        except Exception:
            mocking()
        mocking.assert_not_called()
        assert test.is_valid() is False
        assert test.errors == ["Unexpected exception while trying to is_valid This is an error"]

    def test_retrieval_scope_raises_exception_when_not_valid(self):
        test = DummyEventProperty({})
        test.set_validation(True)
        with test.retrieval_scope():
            pass
        test.set_validation(False)
        with raises(ValidationError):
            with test.retrieval_scope():
                pass

    def test_retrieval_scope_can_raise_and_log_errors(self):
        test = DummyEventProperty({})
        mocking = MagicMock()
        try:
            with test.retrieval_scope():
                raise Exception("This is an error")
        except Exception:
            mocking()
        mocking.assert_called_once()
        assert test.is_valid() is False
        assert test.errors == ["Exception during retrieval: This is an error"]

    def test_can_call_other_methods(self):
        test = DummyEventProperty({})
        try:
            test.is_valid()
            test.is_valid()
            test.value()
            test.add_to_warehouse_message({})
            test.add_to_sequencescape_message({})
        except Exception as exception:
            raise fail("DID RAISE {0}".format(exception))
