from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, List

from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage


class EventPropertyInterface(ABC):
    """
    This class defines the public interface offered by an event property.
    Any method we need to have present in event property should be defined
    inside this class.
    """

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Retuns a boolean (True or False) indicating if the params received for this
        EventProperty are correct in order to retrieve the data. If there is an error
        in validation it will add it to the errors list.
        This methods is safe and should not raise any exception.

        Arguments:
            None

        Returns:
            bool - True/False depending on the result of the validation.

        """
        ...

    @property
    @abstractmethod
    def errors(self) -> List[str]:
        """
        Returns the complete list of errors found.

        Arguments:
            None

        Returns:
            List[str] - List of error messages found currently
        """
        ...

    @cached_property
    @abstractmethod
    def value(self) -> Any:
        """
        Returns the value for the property. If the value cannot be obtained or
        does not have a valid value, then it raises an exception.
        NB: To avoid this it, the instance should be checked first with the
        is_valid() method.

        Arguments:
            None

        Returns:
            Any - Value of the property

        """
        ...

    @abstractmethod
    def add_to_warehouse_message(self, message: WarehouseMessage) -> None:
        """
        Adds this event property information into the warehouse message

        Arguments:
            message: WarehouseMessage - A building message where we want to write
            the information from this event property

        Returns:
            None

        """
        ...

    @abstractmethod
    def add_to_sequencescape_message(self, message: SequencescapeMessage) -> None:
        """
        Adds this event property information into the sequencescape message
        for plate creation

        Arguments:
            message: SequencescapeMessage - A message that will be sent to
            sequencescape to create a plate.

        Returns:
            None

        """
        ...
