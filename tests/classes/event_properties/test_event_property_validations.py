from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract  # type: ignore
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin  # type: ignore


class DummyEventProperty(EventPropertyAbstract, SimpleEventPropertyMixin):
    def add_to_warehouse_message(self):
        return None

    def validate(self):
        return self._validate

    def value(self):
        return self._value


class TestEventPropertyValidations:
    def test_validate_param_not_missing(self):
        test = DummyEventProperty({"asdf": 1})
        test.validate_param_not_missing("asdf")
        assert test.validate() is True
        assert test.errors == []
        test.validate_param_not_missing("jkl")
        assert test.validate() is False
        assert test.errors == ["'jkl' is missing"]

    def test_validate_param_not_empty(self):
        test = DummyEventProperty({"asdf": "1", "jkl": ""})
        test.validate_param_not_empty("asdf")
        assert test.validate() is True
        assert test.errors == []
        test.validate_param_not_empty("jkl")
        assert test.validate() is False
        assert test.errors == ["'jkl' should not be an empty string"]

    def test_validate_param_no_whitespaces(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.validate_param_no_whitespaces("asdf")
        assert test.validate() is True
        assert test.errors == []
        test.validate_param_no_whitespaces("jkl")
        assert test.validate() is False
        assert test.errors == ["'jkl' should not contain any whitespaces"]

    def test_validate_param_is_integer(self):
        test = DummyEventProperty({"asdf": "12", "jkl": "1 2"})
        test.validate_param_is_integer("asdf")
        assert test.validate() is True
        assert test.errors == []
        test.validate_param_is_integer("jkl")
        assert test.validate() is False
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
