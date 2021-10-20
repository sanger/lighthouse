from http import HTTPStatus
from unittest.mock import patch

import pytest

from lighthouse.messages.message import Message

ENDPOINT_PREFIXES = ["", "/v1"]
CREATE_PLATE_EVENTS_URL = "/plate-events/create"
CREATE_PLATE_EVENTS_URLS = [prefix + CREATE_PLATE_EVENTS_URL for prefix in ENDPOINT_PREFIXES]


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_bad_request_no_event_type(client, url):
    response = client.get(f"{url}")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_bad_request_empty_event_type(client, url):
    response = client.get(f"{url}?event_type=")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_internal_error_failed_constructing_message(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        test_error_message = "test error"
        mock_construct.return_value = [test_error_message], None

        response = client.get(f"{url}?event_type=test_event_type")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert len(response.json["errors"]) == 1
        assert response.json["errors"][0] == test_error_message


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_internal_error_failed_broker_initialise(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.routes.common.plate_events.Broker", side_effect=Exception()):
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(f"{url}?event_type=test_event_type")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_internal_error_failed_broker_connect(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.routes.common.plate_events.Broker._connect", side_effect=Exception()):
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(f"{url}?event_type=test_event_type")

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_internal_error_failed_broker_publish(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.routes.common.plate_events.Broker") as mock_broker:
            mock_broker().publish.side_effect = Exception()
            mock_construct.return_value = [], Message({"test": "me"})

            response = client.get(f"{url}?event_type=test_event_type")

            mock_broker()._close_connection.assert_called()
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_internal_error_failed_callback(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        with patch("lighthouse.routes.common.plate_events.Broker") as mock_broker:
            with patch("lighthouse.routes.common.plate_events.fire_callbacks") as mock_callback:
                test_message = Message({"test": "me"})
                mock_construct.return_value = [], test_message
                mock_callback.return_value = False, ["Error"]

                response = client.get(f"{url}?event_type=test_event_type")

                mock_broker()._close_connection.assert_called()
                assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
                assert len(response.json["errors"]) == 1


@pytest.mark.parametrize("url", CREATE_PLATE_EVENTS_URLS)
def test_get_create_plate_event_endpoint_success(client, url):
    with patch("lighthouse.routes.common.plate_events.construct_event_message") as mock_construct:
        routing_key = "test.routing.key"
        with patch("lighthouse.routes.common.plate_events.get_routing_key", return_value=routing_key):
            with patch("lighthouse.routes.common.plate_events.Broker") as mock_broker:
                with patch("lighthouse.routes.common.plate_events.fire_callbacks") as mock_callback:
                    test_message = Message({"test": "me"})
                    mock_construct.return_value = [], test_message
                    mock_callback.return_value = True, []

                    response = client.get(f"{url}?event_type=test_event_type")

                    mock_broker().publish.assert_called_with(test_message, routing_key)
                    mock_broker()._close_connection.assert_called()

                    assert response.status_code == HTTPStatus.OK
                    assert len(response.json["errors"]) == 0
