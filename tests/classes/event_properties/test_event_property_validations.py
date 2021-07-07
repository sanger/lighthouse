from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin


class DummyEventProperty(EventPropertyAbstract, SimpleEventPropertyMixin):
    def add_to_warehouse_message(self, message):
        return None

    def add_to_sequencescape_message(self, message):
        return None

    def is_valid(self):
        return self._is_valid

    def value(self):
        return self._value


class TestEventPropertyValidations:
    def test_validate_param_not_missing(self):
        test = DummyEventProperty({"asdf": 1})
        test.validate_param_not_missing("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.validate_param_not_missing("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' is missing"]

    def test_validate_param_not_empty(self):
        test = DummyEventProperty({"asdf": "1", "jkl": ""})
        test.validate_param_not_empty("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.validate_param_not_empty("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should not be an empty string"]

    def test_validate_param_no_whitespaces(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.validate_param_no_whitespaces("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.validate_param_no_whitespaces("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should not contain any whitespaces"]

    def test_validate_param_is_integer(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.validate_param_is_integer("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.validate_param_is_integer("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should be an integer"]
