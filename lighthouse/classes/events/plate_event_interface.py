from abc import ABC, abstractmethod
from typing import Dict, Union, Any, List


class PlateEventInterface(ABC):
    @abstractmethod
    def initialize_event(self, params: Dict[str, Union[str, Any]]) -> None:
        """This method will parse the event information provided in params and
        store the relevant information from it.
        """
        ...

    @abstractmethod
    def process_event(self) -> None:
        """This method will produce the action required for this event, that could
        mean publishing in the warehouse, creating a plate in Sequencescape, updating
        labwhere, etc... This will vary dependent on the type of event.
        """
        ...

    @abstractmethod
    def errors(self) -> Dict[str, List[str]]:
        """This method will return all errors that have happened during the lifetime of
        this event.
        Returns:
            {Dict[str, List[str]]} - an object where the key is the name of an event property and the value
            is a list of error messages.
        """
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        """This method will perform a validation of all event properties.
        Returns:
            {bool} - True if all properties are valid, False if not
        """
        ...

    @abstractmethod
    def process_errors(self) -> bool:
        """This method will provide the behaviour for what action to do if the
        current instance has any errors.
        """
        ...

    @abstractmethod
    def process_exception(self, exc: Exception) -> bool:
        """This method will provide the behaviour for what to do if an
        exception has happened during the process of this event.
        Arguments:
            {Exception} - An exception related with the execution of this
            event.
        """
        ...
