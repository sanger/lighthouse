from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Dict, Union, List

from flask import current_app as app

from lighthouse.messages.message import Message
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage  # type: ignore

from lighthouse.messages.broker import Broker
from lighthouse.helpers.mongo import set_errors_to_event
from lighthouse.classes.messages.event_properties import EventPropertyAccessor  # type: ignore
import logging

logger = logging.getLogger(__name__)

EVENT_INITIALIZED = "initialized"
EVENT_NOT_INITIALIZED = "not_initialized"


class EventNotInitialized(BaseException):
    pass


class PlateEvent(ABC):
    class PlateTypeEnum(Enum):
        SOURCE = auto()
        DESTINATION = auto()

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str, plate_type: PlateTypeEnum) -> None:
        self._name = name
        self._plate_type = plate_type
        self._state = EVENT_NOT_INITIALIZED
        self._properties: Dict[str, EventPropertyAccessor] = {}

    def initialize_event(self, params: Dict[str, Union[str, Any]]) -> None:
        if "event_wh_uuid" not in params.keys():
            raise EventNotInitialized("Missing event_wh_uuid")

        if "_created" not in params.keys():
            raise EventNotInitialized("Missing _created")

        self._state = EVENT_INITIALIZED
        self._event_uuid = params["event_wh_uuid"]
        self._message_timestamp = params["_created"].isoformat(timespec="seconds")  # type: ignore

    @abstractmethod
    def _create_message(self) -> Message:
        ...

    """Returns the uuid for the event as it is going to be stored in the warehouse

    Returns:
        {str} -- The UUID for the event created.
    """

    def get_event_uuid(self):
        return self._event_uuid

    """Returns the event type for the event

    Returns:
        {str} -- The event type for the event created.
    """

    def get_event_type(self):
        return self._name

    """Returns the datetime when the event was created in a format compatible with messaging.

    Returns:
        {str} -- The datetime for the event created.
    """

    def get_message_timestamp(self):
        return self._message_timestamp

    def process_event(self) -> None:
        if not self._state == EVENT_INITIALIZED:
            raise EventNotInitialized("Not initialized event")

        message = self._create_message()
        self._send_warehouse_message(message=message)

    def _get_routing_key(self) -> str:
        """Determines the routing key for a plate event message.

        Arguments:
            event_type {str} -- The event type for which to determine the routing key.

        Returns:
            {str} -- The message routing key.
        """

        return str(app.config["RMQ_ROUTING_KEY"].replace("#", self._name))

    def _send_warehouse_message(self, message: Message) -> None:
        logger.info("Attempting to publish the constructed plate event message")

        routing_key = self._get_routing_key()

        with Broker() as broker_channel:

            broker_channel.basic_publish(
                exchange=app.config["RMQ_EXCHANGE"],
                routing_key=routing_key,
                body=message.payload(),
            )

    def build_new_warehouse_message(self) -> WarehouseMessage:
        return WarehouseMessage(self.get_event_type(), self.get_event_uuid(), self.get_message_timestamp())

    def errors(self) -> Dict[str, List[str]]:
        """Returns an object with all error messages from each event property

        Arguments:
            None

        Returns:
            {Dict[str,List[str]]} -- The object with the error messages, where the key is the id of the
            event property
        """
        error_message = {}
        for event_property_name in self._properties.keys():
            if len(self._properties[event_property_name].errors()) > 0:
                error_message[event_property_name] = self._properties[event_property_name].errors()

        return error_message

    def process_errors(self) -> bool:
        """Logs the errors into slack, and also writes them into the Mongodb table

        Arguments:
            None

        Returns:
            bool - True if the process has been correct, False if there has been a problem while writing
        """
        if len(self.errors().keys()) > 0:
            logger.error(f"Errors found while processing event {self._event_uuid}: {self.errors()}")
            return set_errors_to_event(self._event_uuid, self.errors())
        return True

    def process_exception(self, exc: BaseException) -> bool:
        """Logs the exception into slack, and also writes it into the Mongodb table

        Arguments:
            None

        Returns:
            bool - True if the process has been correct, False if there has been a problem while writing
        """
        logger.exception(exc)
        return set_errors_to_event(self._event_uuid, {"base": [str(exc)]})
