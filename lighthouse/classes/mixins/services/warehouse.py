from lighthouse.classes.messages.warehouse_messages import WarehouseMessage  # type: ignore
from flask import current_app as app
from lighthouse.messages.broker import Broker
import logging

logger = logging.getLogger(__name__)


class ServiceWarehouseMixin(object):
    def _get_routing_key(self) -> str:
        """Determines the routing key for a plate event message.

        Arguments:
            event_type {str} -- The event type for which to determine the routing key.

        Returns:
            {str} -- The message routing key.
        """
        return str(app.config["RMQ_ROUTING_KEY"])  # .replace("#", self._name))

    def _send_warehouse_message(self, message: WarehouseMessage) -> None:
        logger.info("Attempting to publish the constructed plate event message")

        routing_key = self._get_routing_key()
        with Broker() as broker_channel:
            broker_channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=routing_key,
                body=message.payload(),
            )
