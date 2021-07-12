import pytest

from lighthouse.helpers.requests import get_required_params_from_json_body
from lighthouse.types import EndpointParamsException


def test_json_body_params_correctly_extracted():
    json_keys = ("a_bool", "a_string")
    json_dict = {json_keys[0]: True, json_keys[1]: "string"}

    expected = (True, "string")
    actual = get_required_params_from_json_body(json_dict, json_keys, (bool, str))

    assert actual == expected


def test_json_body_params_ignores_extra_values():
    json_keys = ("a_bool", "a_string")
    json_dict = {json_keys[0]: False, json_keys[1]: "string_2", "another_string": "string_2"}

    expected = (False, "string_2")
    actual = get_required_params_from_json_body(json_dict, json_keys, (bool, str))

    assert actual == expected


@pytest.mark.parametrize("json_obj", [None, ["an_array"]])
def test_json_body_params_raises_exception_when_json_not_a_dict(json_obj):
    with (pytest.raises(EndpointParamsException)) as e_info:
        get_required_params_from_json_body(json_obj, ("an_array"), (str))

    assert "JSON dictionary" in str(e_info.value)


@pytest.mark.parametrize(
    "json_dict, missing",
    [[{}, ["a_bool", "a_string"]], [{"a_bool": True}, ["a_string"]], [{"a_string": "string"}, ["a_bool"]]],
)
def test_json_body_params_reports_missing_keys(json_dict, missing):
    json_keys = ("a_bool", "a_string")

    with (pytest.raises(EndpointParamsException)) as e_info:
        get_required_params_from_json_body(json_dict, json_keys, (bool, str))

    assert "JSON needs" in str(e_info.value)
    assert "parameter(s)" in str(e_info.value)
    assert all([f"'{param}'" in str(e_info.value) for param in missing])


@pytest.mark.parametrize(
    "json_dict, wrong_type",
    [
        [{"a_bool": "not_bool", "a_string": "string"}, ["a_bool"]],
        [{"a_bool": True, "a_string": True}, ["a_string"]],
        [{"a_bool": "not_bool", "a_string": False}, ["a_bool", "a_string"]],
    ],
)
def test_json_body_params_reports_wrong_types(json_dict, wrong_type):
    json_keys = ("a_bool", "a_string")

    with (pytest.raises(EndpointParamsException)) as e_info:
        get_required_params_from_json_body(json_dict, json_keys, (bool, str))

    assert "contains parameter(s)" in str(e_info.value)
    assert "wrong type" in str(e_info.value)
    assert all([f"'{param}'" in str(e_info.value) for param in wrong_type])
