import logging
from abc import abstractmethod
from enum import Enum, auto
from typing import Any, Dict, List

from lighthouse.classes.event_properties.interfaces import EventPropertyInterface
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.warehouse import WarehouseServiceMixin
from lighthouse.helpers.mongo import set_errors_to_event
from lighthouse.messages.message import Message

from .exceptions import EventNotInitializedError
from .plate_event_interface import PlateEventInterface

logger = logging.getLogger(__name__)


class PlateEvent(PlateEventInterface, WarehouseServiceMixin):
    EVENT_INITIALIZED = "initialized"
    EVENT_NOT_INITIALIZED = "not_initialized"

    class PlateTypeEnum(Enum):
        SOURCE = auto()
        DESTINATION = auto()

    def __init__(self, event_type: str, plate_type: PlateTypeEnum) -> None:
        """
        Creates a new instance of PlateEvent.
        Stores the event type in a property.
        Sets the state of the event to 'uninitialized' and it will not change until
        initialize_event() is called.
        Builds an empty dictionary for event_properties.
        """
        self._event_type = event_type
        self._plate_type = plate_type
        self._state: str = PlateEvent.EVENT_NOT_INITIALIZED
        self.properties: Dict[str, EventPropertyInterface] = {}
        self._validation: bool = True

    def initialize_event(self, params: Dict[str, Any]) -> None:
        """
        Initialize the event by parsing the event params.
        Stores the uuid and creation timestamp in properties; if any of them
        are missing it will raise an exception.
        Sets the state of the event to 'initialized'
        """
        if "event_wh_uuid" not in params.keys():
            raise EventNotInitializedError("Missing event_wh_uuid")

        if "_created" not in params.keys():
            raise EventNotInitializedError("Missing _created")

        self._state = PlateEvent.EVENT_INITIALIZED
        self._event_uuid: str = params["event_wh_uuid"]
        self._message_timestamp: str = params["_created"].isoformat(timespec="seconds")

    @abstractmethod
    def _create_message(self) -> Message:
        """Builds a warehouse message and adds all the information from this event
        so is ready to be published. As the content will depend on each event, it is
        implemented in the subclass.

        Returns:
            {Message} - warehouse message with all information related with current event
        """
        ...

    @property
    def event_type(self) -> str:
        """Returns the event type for the event

        Returns:
            {str} -- The event type for the event created.
        """
        return self._event_type

    @property
    def event_uuid(self) -> str:
        """Returns the uuid for the event as it is going to be stored in the warehouse

        Returns:
            {str} -- The UUID for the event created.
        """
        return self._event_uuid

    @property
    def message_timestamp(self) -> str:
        """Returns the datetime when the event was created in a format compatible with messaging.

        Returns:
            {str} -- The datetime for the event created.
        """
        return self._message_timestamp

    @property
    def state(self) -> str:
        """Returns the state where this event is ('initialized', 'not initialized') indicating
        if the params have been parsed or not.

        Returns:
            {str} -- The state where this event is: ('initialized', 'not initialized')
        """
        return self._state

    def process_event(self) -> None:
        """Adds a default behaviour for the event process. By default it will:
        - raise an exception if the event has not run initialize_event() before
        - create a new message to send to the warehouse
        - send the message to the warehouse
        """
        if not (self.state == PlateEvent.EVENT_INITIALIZED):
            raise EventNotInitializedError("Not initialized event")

        message = self._create_message()
        self.send_warehouse_message(message=message)

    def build_new_warehouse_message(self) -> WarehouseMessage:
        """
        Builds a new empty warehouse message with the generic information of an event:
        (type, uuid, timestamp). All other information needs to be fill in.
        Raises an exception if it does not have all information.

        Returns
            {WarehouseMessage} - Message that we are building in order to publish to
            the warehouse
        """
        if self.state == PlateEvent.EVENT_NOT_INITIALIZED:
            raise EventNotInitializedError("We cannot build a new message because the event is not initialized")
        return WarehouseMessage(self.event_type, self.event_uuid, self.message_timestamp)

    def build_new_sequencescape_message(self) -> SequencescapeMessage:
        if self.state == PlateEvent.EVENT_NOT_INITIALIZED:
            raise EventNotInitializedError("We cannot build a new message because the event is not initialized")
        return SequencescapeMessage()

    @property
    def errors(self) -> Dict[str, List[str]]:
        """Returns an object with all error messages from each event property

        Returns:
            {Dict[str,List[str]]} -- The object with the error messages, where the key is the id of the
            event property
        """
        error_message = {}
        for event_property_name in self.properties.keys():
            if len(self.properties[event_property_name].errors) > 0:
                error_message[event_property_name] = self.properties[event_property_name].errors

        return error_message

    def is_valid(self) -> bool:
        """
        Performs a validation on all event properties and returns True/False indicating if
        the current instance is valid

        Returns:
            {bool} - True if the event is valid, or False if not
        """
        self._validation = True
        for event_property_name in self.properties.keys():
            self._validation = self._validation and self.properties[event_property_name].is_valid()
        return self._validation

    def process_errors(self) -> bool:
        """Logs the errors into slack, and also writes them into the Mongodb table

        Returns:
            bool - True if the process has been correct, False if there has been a problem while writing
        """
        if len(self.errors) > 0:
            logger.error(f"Errors found while processing event {self.event_uuid}: {self.errors}")
            return set_errors_to_event(self.event_uuid, self.errors)
        return True

    def process_exception(self, exc: BaseException) -> bool:
        """Logs the exception into slack, and also writes it into the Mongodb table

        Returns:
            bool - True if the process has been correct, False if there has been a problem while writing
        """
        logger.exception(exc)
        return set_errors_to_event(self.event_uuid, {"base": [str(exc)]})
