from unittest.mock import MagicMock, patch

import pytest
from lighthouse.messages.broker import Broker


def test_broker_connect_connects(app, mock_pika):
    with app.app_context():
        test_credentials, test_parameters, mock_channel, mock_connection, pika = mock_pika

        broker = Broker()
        broker.connect()

        pika.PlainCredentials.assert_called_with(
            app.config["RMQ_USERNAME"], app.config["RMQ_PASSWORD"]
        )
        pika.ConnectionParameters.assert_called_with(
            app.config["RMQ_HOST"],
            app.config["RMQ_PORT"],
            app.config["RMQ_VHOST"],
            test_credentials,
        )
        pika.BlockingConnection.assert_called_with(test_parameters)
        mock_connection.channel.assert_called()
        if app.config["RMQ_DECLARE_EXCHANGE"]:
            mock_channel.exchange_declare.assert_called_with(
                app.config["RMQ_EXCHANGE"], exchange_type=app.config["RMQ_EXCHANGE_TYPE"]
            )

        assert broker.connection == mock_connection
        assert broker.channel == mock_channel


def test_broker_publish(app, mock_pika, mock_message):
    with app.app_context():
        _, _, mock_channel, _, _ = mock_pika
        test_payload, test_message = mock_message
        test_routing_key = "routing key"

        broker = Broker()
        broker.connect()
        broker.publish(test_message, test_routing_key)

        mock_channel.basic_publish.assert_called_with(
            exchange=app.config["RMQ_EXCHANGE"],
            routing_key=test_routing_key,
            body=test_payload,
        )


def test_broker_publish_no_message(app, mock_pika):
    with app.app_context():
        _, _, mock_channel, _, _ = mock_pika
        test_routing_key = "routing key"

        broker = Broker()
        broker.connect()
        broker.publish(None, test_routing_key)

        mock_channel.basic_publish.assert_not_called()


def test_broker_publish_no_routing_key(app, mock_pika, mock_message):
    with app.app_context():
        _, _, mock_channel, _, _ = mock_pika
        _, test_message = mock_message

        broker = Broker()
        broker.connect()
        broker.publish(test_message, None)

        mock_channel.basic_publish.assert_not_called()


def test_broker_publish_no_connection(app, mock_pika, mock_message):
    with app.app_context():
        _, _, mock_channel, _, _ = mock_pika
        _, test_message = mock_message

        broker = Broker()
        with pytest.raises(AttributeError):
            broker.publish(test_message, "test routing key")


def test_broker_close_connection(app, mock_pika):
    with app.app_context():
        _, _, _, mock_connection, _ = mock_pika

        broker = Broker()
        broker.connect()
        broker.close_connection()

        mock_connection.close.assert_called()


def test_broker_close_connection_no_connection():
    broker = Broker()

    with pytest.raises(AttributeError):
        broker.close_connection()


# class-specific test helpers


@pytest.fixture
def mock_pika():
    with patch("lighthouse.messages.broker.pika") as pika:
        test_credentials = "test credentials"
        pika.PlainCredentials.return_value = test_credentials

        test_parameters = "test parameters"
        pika.ConnectionParameters.return_value = test_parameters

        mock_channel = MagicMock()
        mock_connection = MagicMock()
        mock_connection.channel.return_value = mock_channel
        pika.BlockingConnection.return_value = mock_connection

        yield test_credentials, test_parameters, mock_channel, mock_connection, pika


@pytest.fixture
def mock_message():
    test_payload = "test payload"
    test_message = MagicMock()
    test_message.payload.return_value = test_payload
    return test_payload, test_message
