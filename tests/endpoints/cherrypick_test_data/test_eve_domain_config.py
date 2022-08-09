import re
from http import HTTPStatus

import pytest

ENDPOINT_PREFIXES = ["", "/v1"]


@pytest.mark.parametrize("endpoint_prefix", ENDPOINT_PREFIXES)
@pytest.mark.parametrize("plate_specs", ["not_list", 1984])
def test_endpoint_generates_issues_for_wrong_types(client, endpoint_prefix, plate_specs):
    response = client.post(
        f"{endpoint_prefix}/cherrypick-test-data",
        json={"plate_specs": plate_specs},
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "plate_specs" in response.json["_issues"]
    assert re.match("must be of \\w+ type", response.json["_issues"]["plate_specs"])


@pytest.mark.parametrize("endpoint_prefix", ENDPOINT_PREFIXES)
def test_endpoint_generates_issues_for_null_values(client, endpoint_prefix):
    response = client.post(
        f"{endpoint_prefix}/cherrypick-test-data",
        json={"plate_specs": None},
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "plate_specs" in response.json["_issues"]
    assert re.match("null value not allowed", response.json["_issues"]["plate_specs"])


@pytest.mark.parametrize("endpoint_prefix", ENDPOINT_PREFIXES)
def test_endpoint_generates_issues_for_missing_values(client, endpoint_prefix):
    json_obj: dict = {}

    response = client.post(
        f"{endpoint_prefix}/cherrypick-test-data",
        json=json_obj,
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "plate_specs" in response.json["_issues"]
    assert response.json["_issues"]["plate_specs"] == "required field"


@pytest.mark.parametrize("endpoint_prefix", ENDPOINT_PREFIXES)
def test_endpoint_generates_issues_for_extra_values(client, endpoint_prefix):
    response = client.post(
        f"{endpoint_prefix}/cherrypick-test-data",
        json={"plate_specs": [[1, 96]], "extra_value": "extra"},
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "extra_value" in response.json["_issues"]
    assert response.json["_issues"]["extra_value"] == "unknown field"


@pytest.mark.parametrize("endpoint_prefix", ENDPOINT_PREFIXES)
def test_endpoint_generates_issues_for_bulk_insert(client, endpoint_prefix):
    response = client.post(
        f"{endpoint_prefix}/cherrypick-test-data",
        json=[{"plate_specs": [[1, 96]]}, {"plate_specs": [[1, 96]]}],
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
