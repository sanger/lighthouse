from abc import ABC, abstractmethod
from typing import Any, List, Dict
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage  # type: ignore
from contextlib import contextmanager

import logging

logger = logging.getLogger(__name__)


class ValidationError(BaseException):
    pass


class RetrievalError(BaseException):
    pass


class EventPropertyInterface(ABC):
    """
    This class defines the public interface offered by an event property.
    Any method we need to have present in event property should be defined
    inside this class.
    """

    @abstractmethod
    def validate(self) -> bool:
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

    @abstractmethod
    def value(self) -> Any:
        """
        Returns the value for the property. If the value cannot be obtained or
        does not have a valid value, then it raises an exception.
        NB: To avoid this it, the instance should be checked first with the
        validate() method.

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


class EventPropertyAbstract(EventPropertyInterface):
    """
    This class provide some tools to validate data obtained directly
    from the params argument.
    It is an abstract class that will need to define the methods specified
    in its interface class (EventPropertyInterface).
    If a more advanced process is needed (like accessing an external service),
    then the methods of this class should be rewritten (or a new class
    should be created).
    This class also contains methods that will be needed for internal
    process for the class but should not be called from outside of this
    instance (they should be considered all protected methods).
    The public interface that should be used in this case is
    defined in EventPropertyInterface.
    """

    def __init__(self, params: Dict[str, Any]):
        """
        Stores the params, resets the instance and perform a validation check on the params

        Arguments:
            params: Dict[str, Any] - dict of key/value with the settings for
            this property
        """
        self.reset()
        self._params = params
        if self._params is None:
            raise ValidationError("You need to define params to create the EventProperty")

    def reset(self):
        """
        Deletes all errors and clears the validation setting.
        """
        self._errors = []
        self._value = None
        self._validate = True

    def errors(self) -> List[str]:
        """
        Validates the instance and returns the complete list of errors found (this
        errors are not just validations; it could also be previous exceptions
        thrown during the lifetime of this instance).

        Arguments:
            None

        Returns:
            List[str] - List of error messages found currently
        """
        self.validate()
        return self._errors

    def valid(self) -> bool:
        """Alias for #validate()"""

        return self.validate()

    def enforce_validation(self) -> None:
        """
        Raises a ValidationError exception if the instance does not pass validation.

        Returns:
            ValidationError - Raises exception
        """
        if not self.validate():
            raise ValidationError("Validation error")

    def process_validation(self, condition: bool, message: str) -> None:
        """
        Stores the error message if the condition is not True.
        Changes the validation state for the instance.
        It is recommended to run this inside a validation_scope() context
        to be able to properly log any possible exceptions while checking the
        condition.

        Arguments:
            condition: bool - Condition to check
            message: str - Error message to store

        Returns:
            None

        """
        if not condition:
            if message not in self._errors:
                self._errors.append(message)
            self._validate = False
        self._validate = self._validate and True

    @contextmanager
    def validation_scope(self):
        """
        Creates a 'safe' scope where we can perform a validation check without
        raising the exception, but log this situations if it happens.
        This is intended to be use only with small validation operations inside the
        validate() method. It is not recommended in any other case.

        Arguments:
            None

        Returns:
            ContextManager - A context specifically created to handle a validation error
        """
        try:
            yield
        except Exception as exc:
            self._validate = False
            self._errors.append(f"Unexpected exception while trying to validate {exc}")
            logger.exception(exc)
