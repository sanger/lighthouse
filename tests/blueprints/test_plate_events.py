from http import HTTPStatus
from unittest.mock import patch
from lighthouse.messages.message import Message


def test_get_create_plate_event_endpoint_bad_request_no_event_type(client):
    response = client.get("/plate-events/create")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_bad_request_empty_event_type(client):
    response = client.get("/plate-events/create?event_type=")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_internal_error_failed_constructing_message(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        test_error_message = "test error"
        mock_construct.return_value = [test_error_message], None

        response = client.get("/plate-events/create?event_type=test_event_type")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert response.json["errors"][0] == test_error_message


def test_get_create_plate_event_endpoint_internal_error_failed_broker_initialise(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.blueprints.plate_events.Broker", side_effect=Exception("Boom!")):
            mock_construct.return_value = [], Message("test message content")

            response = client.get("/plate-events/create?event_type=test_event_type")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_internal_error_failed_broker_connect(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        with patch(
            "lighthouse.blueprints.plate_events.Broker.connect", side_effect=Exception("Boom!")
        ):
            mock_construct.return_value = [], Message("test message content")

            response = client.get("/plate-events/create?event_type=test_event_type")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_internal_error_failed_broker_publish(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        with patch(
            "lighthouse.blueprints.plate_events.Broker.publish", side_effect=Exception("Boom!")
        ):
            mock_construct.return_value = [], Message("test message content")

            response = client.get("/plate-events/create?event_type=test_event_type")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_success(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.blueprints.plate_events.Broker"):
            test_message = Message("test message content")
            mock_construct.return_value = [], test_message

            response = client.get("/plate-events/create?event_type=test_event_type")

            assert response.status_code == HTTPStatus.OK
            assert len(response.json["errors"]) == 0
