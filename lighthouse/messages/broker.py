import logging

import pika
from flask import current_app as app

from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


class Broker:
    """Controls the connection, exchange and publishing to RabbitMQ."""

    def connect(self) -> None:
        self._create_connection()
        self._open_channel()
        if app.config["RMQ_DECLARE_EXCHANGE"]:
            self._declare_exchange()

    def publish(self, message: Message, routing_key: str) -> None:
        if message is not None and routing_key is not None:
            logger.debug("Publishing message")
            self._channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=routing_key,
                body=message.payload(),
            )

    def close_connection(self) -> None:
        logger.debug("Closing connection")
        self._connection.close()

    def _create_connection(self) -> None:
        host = app.config["RMQ_HOST"]
        logger.debug(f"Creating messaging connection to '{host}'")
        credentials = pika.PlainCredentials(app.config["RMQ_USERNAME"], app.config["RMQ_PASSWORD"])
        parameters = pika.ConnectionParameters(host, app.config["RMQ_PORT"], app.config["RMQ_VHOST"], credentials)
        self._connection = pika.BlockingConnection(parameters)

    def _open_channel(self) -> None:
        logger.debug("Opening channel")
        self._channel = self._connection.channel()

    def _declare_exchange(self) -> None:
        exchange_name = app.config["RMQ_EXCHANGE"]
        logger.debug(f"Declaring exchange '{exchange_name}'")
        self._channel.exchange_declare(exchange_name, exchange_type=app.config["RMQ_EXCHANGE_TYPE"])
