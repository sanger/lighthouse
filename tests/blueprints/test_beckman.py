from http import HTTPStatus


# ---------- get_robots tests ----------


def test_get_robots_returns_expected_robots(app, client):
    with app.app_context():
        response = client.get("/beckman/robots")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["errors"]) == 0
        assert response.json["robots"] == [
            {"name": "Robot 1", "serial_number": "BKRB0001"},
            {"name": "Robot 2", "serial_number": "BKRB0002"},
            {"name": "Robot 3", "serial_number": "BKRB0003"},
            {"name": "Robot 4", "serial_number": "BKRB0004"},
        ]


def test_get_robots_internal_server_error_no_robots_config_exists(app, client):
    with app.app_context():
        del app.config["BECKMAN_ROBOTS"]
        response = client.get("/beckman/robots")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["robots"]) == 0


def test_get_robots_internal_server_error_incorrect_format_config(app, client):
    with app.app_context():
        app.config["BECKMAN_ROBOTS"] = {"BKRB0001": {"no name key": "not a name"}}
        response = client.get("/beckman/robots")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["robots"]) == 0


# ---------- get_failure_types tests ----------


def test_get_failure_types_returns_expected_failure_types(app, client):
    with app.app_context():
        response = client.get("/beckman/failure-types")

        assert response.status_code == HTTPStatus.OK
        assert len(response.json["errors"]) == 0
        assert response.json["failure_types"] == [
            {"type": "robot_crashed", "description": "The robot crashed"},
            {"type": "sample_contamination", "description": "Sample contamination occurred"},
            {"type": "other", "description": "Any other failure"},
        ]


def test_get_failure_types_internal_server_error_no_failure_types_config_exists(app, client):
    with app.app_context():
        del app.config["BECKMAN_FAILURE_TYPES"]
        response = client.get("/beckman/failure-types")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["failure_types"]) == 0


def test_get_failure_types_internal_server_error_incorrect_format_config(app, client):
    with app.app_context():
        app.config["BECKMAN_FAILURE_TYPES"] = ["not the expected dictionary"]
        response = client.get("/beckman/failure-types")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert len(response.json["failure_types"]) == 0
