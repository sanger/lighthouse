from pytest import raises, fail
from unittest.mock import MagicMock
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, ValidationError


class DummyEventProperty(EventPropertyAbstract):
    def add_to_warehouse_message(self):
        return None

    def validate(self):
        return self._validate

    def value(self):
        return self._value

    # Helper methods outside of the interface
    def set_value(self, val):
        self._value = val

    def set_validation(self, valid):
        self._validate = valid

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

    def test_reset_can_reset_both_errors_and_validate(self):
        test = DummyEventProperty({})
        test.set_validation(False)
        test.set_errors(["an error"])
        assert test.valid() is False
        assert test.errors == ["an error"]
        test.reset()
        assert test.valid() is True
        assert test.errors == []

    def test_enforce_validation_raises_exception_when_not_valid(self):
        test = DummyEventProperty({})
        test.set_validation(True)
        test.enforce_validation()
        test.set_validation(False)
        with raises(ValidationError):
            test.enforce_validation()

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
        assert test.validate() is False
        assert test.errors == ["Unexpected exception while trying to validate This is an error"]

    def test_retrieval_scope_can_raise_and_log_errors(self):
        test = DummyEventProperty({})
        mocking = MagicMock()
        try:
            with test.retrieval_scope():
                raise Exception("This is an error")
        except Exception:
            mocking()
        mocking.assert_called_once()
        assert test.validate() is False
        assert test.errors == ["Exception during retrieval: This is an error"]

    def test_can_call_other_methods(self):
        test = DummyEventProperty({})
        try:
            test.valid()
            test.validate()
            test.value()
            test.add_to_warehouse_message()
        except Exception as exception:
            raise fail("DID RAISE {0}".format(exception))
