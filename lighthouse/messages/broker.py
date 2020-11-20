import pika
import logging
from lighthouse.messages.message import Message
from flask import current_app as app

logger = logging.getLogger(__name__)


class Broker:
    """Controls the connection, exchange and publishing to RabbitMQ."""

    def connect(self) -> None:
        self.__create_connection()
        self.__open_channel()
        if app.config["RMQ_DECLARE_EXCHANGE"]:
            self.__declare_exchange()

    def publish(self, message: Message) -> None:
        if message is not None:
            logger.debug("Publishing message")
            self.channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=app.config["RMQ_ROUTING_KEY"],
                body=message.payload(),
            )

    def close_connection(self) -> None:
        logger.debug("Closing connection")
        self.connection.close()

    def __create_connection(self) -> None:
        host = app.config["RMQ_HOST"]
        logger.debug(f"Creating messaging connection to '{host}'")
        credentials = pika.PlainCredentials(app.config["RMQ_USERNAME"], app.config["RMQ_PASSWORD"])
        parameters = pika.ConnectionParameters(
            host, app.config["RMQ_PORT"], app.config["RMQ_VHOST"], credentials
        )
        self.connection = pika.BlockingConnection(parameters)

    def __open_channel(self) -> None:
        logger.debug("Opening channel")
        self.channel = self.connection.channel()

    def __declare_exchange(self) -> None:
        exchange_name = app.config["RMQ_EXCHANGE"]
        logger.debug(f"Declaring exchange '{exchange_name}'")
        self.channel.exchange_declare(exchange_name, exchange_type=app.config["RMQ_EXCHANGE_TYPE"])
