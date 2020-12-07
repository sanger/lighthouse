from http import HTTPStatus
from unittest.mock import patch
from lighthouse.messages.message import Message  # type: ignore


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
        with patch("lighthouse.blueprints.plate_events.Broker") as mock_broker:
            mock_broker().publish.side_effect = Exception("Boom!")
            mock_construct.return_value = [], Message("test message content")

            response = client.get("/plate-events/create?event_type=test_event_type")

            mock_broker().close_connection.assert_called()
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_internal_error_failed_callback(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.blueprints.plate_events.Broker") as mock_broker:
            with patch("lighthouse.blueprints.plate_events.fire_callbacks") as mock_callback:
                test_message = Message("test message content")
                mock_construct.return_value = [], test_message
                mock_callback.return_value = False, ["Error"]

                response = client.get("/plate-events/create?event_type=test_event_type")

                mock_broker().close_connection.assert_called()
                assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
                assert len(response.json["errors"]) == 1


def test_get_create_plate_event_endpoint_success(client):
    with patch("lighthouse.blueprints.plate_events.construct_event_message") as mock_construct:
        routing_key = "test.routing.key"
        with patch("lighthouse.blueprints.plate_events.get_routing_key", return_value=routing_key):
            with patch("lighthouse.blueprints.plate_events.Broker") as mock_broker:
                with patch("lighthouse.blueprints.plate_events.fire_callbacks") as mock_callback:
                    test_message = Message("test message content")
                    mock_construct.return_value = [], test_message
                    mock_callback.return_value = True, []

                    response = client.get("/plate-events/create?event_type=test_event_type")

                    mock_broker().publish.assert_called_with(test_message, routing_key)
                    mock_broker().close_connection.assert_called()
                    assert response.status_code == HTTPStatus.OK
                    assert len(response.json["errors"]) == 0
