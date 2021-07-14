import re
from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "add_to_dart, plate_specs, error_fields",
    [
        ["not_bool", [[1, 96]], ["add_to_dart"]],
        [1984, [[1, 96]], ["add_to_dart"]],
        [True, "not_list", ["plate_specs"]],
        [False, 1984, ["plate_specs"]],
        ["not_bool", "not_list", ["add_to_dart", "plate_specs"]],
    ],
)
def test_endpoint_generates_issues_for_wrong_types(client, add_to_dart, plate_specs, error_fields):
    response = client.post(
        "/cherrypick-test-data",
        json={"add_to_dart": add_to_dart, "plate_specs": plate_specs},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    for field in error_fields:
        assert field in response.json["_issues"]
        assert re.match("must be of \\w+ type", response.json["_issues"][field])


@pytest.mark.parametrize(
    "add_to_dart, plate_specs, error_fields",
    [
        [None, [[1, 96]], ["add_to_dart"]],
        [True, None, ["plate_specs"]],
        [None, None, ["add_to_dart", "plate_specs"]],
    ],
)
def test_endpoint_generates_issues_for_null_values(client, add_to_dart, plate_specs, error_fields):
    response = client.post(
        "/cherrypick-test-data",
        json={"add_to_dart": add_to_dart, "plate_specs": plate_specs},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    for field in error_fields:
        assert field in response.json["_issues"]
        assert re.match("null value not allowed", response.json["_issues"][field])


@pytest.mark.parametrize(
    "include_add_to_dart, include_plate_specs, error_fields",
    [
        [False, True, ["add_to_dart"]],
        [True, False, ["plate_specs"]],
        [False, False, ["add_to_dart", "plate_specs"]],
    ],
)
def test_endpoint_generates_issues_for_missing_values(client, include_add_to_dart, include_plate_specs, error_fields):
    json_obj: dict = {}
    if include_add_to_dart:
        json_obj["add_to_dart"] = True
    if include_plate_specs:
        json_obj["plate_specs"] = [[1, 96]]

    response = client.post(
        "/cherrypick-test-data",
        json=json_obj,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    for field in error_fields:
        assert field in response.json["_issues"]
        assert response.json["_issues"][field] == "required field"


def test_endpoint_generates_issues_for_extra_values(client):
    response = client.post(
        "/cherrypick-test-data",
        json={"add_to_dart": True, "plate_specs": [[1, 96]], "extra_value": "extra"},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "extra_value" in response.json["_issues"]
    assert response.json["_issues"]["extra_value"] == "unknown field"


def test_endpoint_generates_issues_for_bulk_insert(client):
    response = client.post(
        "/cherrypick-test-data",
        json=[{"add_to_dart": True, "plate_specs": [[1, 96]]}, {"add_to_dart": False, "plate_specs": [[1, 96]]}],
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
