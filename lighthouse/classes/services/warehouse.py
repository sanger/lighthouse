import logging

from flask import current_app as app

from lighthouse.messages.broker import Broker
from lighthouse.messages.message import Message

logger = logging.getLogger(__name__)


class WarehouseServiceMixin:
    @property
    def routing_key(self) -> str:
        """Determines the routing key for a plate event message.

        Returns:
            {str} -- The message routing key.
        """
        return str(app.config["RMQ_ROUTING_KEY"].replace("#", self.event_type))  # type: ignore

    def send_warehouse_message(self, message: Message) -> None:
        """Publishes a message to the exchange as specified in configuration."""
        logger.info("Attempting to publish the constructed plate event message")
        with Broker() as broker_channel:
            broker_channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=self.routing_key,
                body=message.payload(),
            )
