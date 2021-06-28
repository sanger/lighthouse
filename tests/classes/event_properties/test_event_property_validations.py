from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin


class DummyEventProperty(EventPropertyAbstract, SimpleEventPropertyMixin):
    def add_to_warehouse_message(self):
        return None

    def is_valid(self):
        return self._is_valid

    def value(self):
        return self._value


class TestEventPropertyValidations:
    def test_is_valid_param_not_missing(self):
        test = DummyEventProperty({"asdf": 1})
        test.is_valid_param_not_missing("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.is_valid_param_not_missing("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' is missing"]

    def test_is_valid_param_not_empty(self):
        test = DummyEventProperty({"asdf": "1", "jkl": ""})
        test.is_valid_param_not_empty("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.is_valid_param_not_empty("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should not be an empty string"]

    def test_is_valid_param_no_whitespaces(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.is_valid_param_no_whitespaces("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.is_valid_param_no_whitespaces("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should not contain any whitespaces"]

    def test_is_valid_param_is_integer(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.is_valid_param_is_integer("asdf")
        assert test.is_valid() is True
        assert test.errors == []
        test.is_valid_param_is_integer("jkl")
        assert test.is_valid() is False
        assert test.errors == ["'jkl' should be an integer"]

    def test_is_integer(self):
        test = DummyEventProperty({})
        assert test.is_integer("123")
        assert not test.is_integer("1.23")
        assert test.is_integer("123 ")
        assert test.is_integer("   123 ")
        assert test.is_integer("   123")
        assert test.is_integer("-123")
        assert test.is_integer("+123")
        assert not test.is_integer("- 123")
        assert not test.is_integer("1,23")
        assert not test.is_integer("123 123")
