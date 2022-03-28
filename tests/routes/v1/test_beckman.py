from http import HTTPStatus

import pytest

ROBOTS_ENDPOINT = "/beckman/robots"
FAILURE_TYPES_ENDPOINT = "/beckman/failure-types"
ENDPOINT_PREFIXES = ["", "/v1"]

ROBOTS_BASE_URLS = [prefix + ROBOTS_ENDPOINT for prefix in ENDPOINT_PREFIXES]
FAILURE_TYPES_BASE_URLS = [prefix + FAILURE_TYPES_ENDPOINT for prefix in ENDPOINT_PREFIXES]


# ---------- get_robots tests ----------


@pytest.mark.parametrize("base_url", ROBOTS_BASE_URLS)
def test_get_robots_returns_expected_robots(app, client, base_url):
    with app.app_context():
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["errors"]) == 0
        assert response.json["robots"] == [
            {"name": "Robot 1", "serial_number": "BKRB0001"},
            {"name": "Robot 2", "serial_number": "BKRB0002"},
            {"name": "Robot 3", "serial_number": "BKRB0003"},
            {"name": "Robot 4", "serial_number": "BKRB0004"},
        ]


@pytest.mark.parametrize("base_url", ROBOTS_BASE_URLS)
def test_get_robots_internal_server_error_no_robots_config_exists(app, client, base_url):
    with app.app_context():
        del app.config["BECKMAN_ROBOTS"]
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["robots"]) == 0


@pytest.mark.parametrize("base_url", ROBOTS_BASE_URLS)
def test_get_robots_internal_server_error_incorrect_format_config(app, client, base_url):
    with app.app_context():
        app.config["BECKMAN_ROBOTS"] = {"BKRB0001": {"no name key": "not a name"}}
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["robots"]) == 0


# ---------- get_failure_types tests ----------


@pytest.mark.parametrize("base_url", FAILURE_TYPES_BASE_URLS)
def test_get_failure_types_returns_expected_failure_types(app, client, base_url):
    with app.app_context():
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["errors"]) == 0
        assert response.json["failure_types"] == [
            {"type": "robot_crashed", "description": "The robot crashed"},
            {"type": "sample_contamination", "description": "Sample contamination occurred"},
            {"type": "other", "description": "Any other failure"},
        ]


@pytest.mark.parametrize("base_url", FAILURE_TYPES_BASE_URLS)
def test_get_failure_types_internal_server_error_no_failure_types_config_exists(app, client, base_url):
    with app.app_context():
        del app.config["ROBOT_FAILURE_TYPES"]
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["failure_types"]) == 0


@pytest.mark.parametrize("base_url", FAILURE_TYPES_BASE_URLS)
def test_get_failure_types_internal_server_error_incorrect_format_config(app, client, base_url):
    with app.app_context():
        app.config["ROBOT_FAILURE_TYPES"] = ["not the expected dictionary"]
        response = client.get(base_url)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["failure_types"]) == 0
