from abc import ABC, abstractmethod
from typing import Any, List, Dict
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage
from contextlib import contextmanager

import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    pass


class RetrievalError(Exception):
    pass


def qualified_class_name(instance):
    import sys
    klass = type(instance)
    frame = sys._getframe(3)
    function_name = frame.f_code.co_name
    line_no = frame.f_lineno

    return f"{ klass.__qualname__ }::{ function_name } - line { line_no }"


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

    @property
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


class EventPropertyAbstract(EventPropertyInterface):
    """
    This class provide some tools to is_valid data obtained directly
    from the params argument.
    It is an abstract class that will need to define the methods specified
    in its interface class (EventPropertyInterface).
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
        self._errors: List[str] = []
        self._value = None
        self._is_valid = True

    @property
    def errors(self) -> List[str]:
        """
        is_valids the instance and returns the complete list of errors found (this
        errors are not just validations; it could also be previous exceptions
        thrown during the lifetime of this instance).

        Arguments:
            None

        Returns:
            List[str] - List of error messages found currently
        """
        self.is_valid()
        return self._errors

    def valid(self) -> bool:
        """Alias for #is_valid()"""

        return self.is_valid()

    def enforce_validation(self) -> None:
        """
        Raises a ValidationError exception if the instance does not pass validation.

        Returns:
            ValidationError - Raises exception
        """
        if not self.is_valid():
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
            self._is_valid = False
        self._is_valid = self._is_valid and True

    @contextmanager
    def validation_scope(self):
        """
        Creates a 'safe' scope where we can perform a validation check without
        raising the exception, but log this situations if it happens.
        This is intended to be use only with small validation operations inside the
        is_valid() method. It is not recommended in any other case.

        Arguments:
            None

        Returns:
            ContextManager - A context specifically created to handle a validation error
        """
        logger.debug(f"At { qualified_class_name(self) } - Start validation")

        try:
            yield
        except Exception as exc:
            logger.debug(f"At { qualified_class_name(self) } - Exception during validation")

            self._is_valid = False
            msg = f"Unexpected exception while trying to is_valid {exc}"
            if msg not in self._errors:
                self._errors.append(msg)
            logger.exception(exc)

        logger.debug(f"At { qualified_class_name(self) } - End validation")

    @contextmanager
    def retrieval_scope(self):
        """
        Creates an 'unsafe' scope where we can try to retrieve the value.
        If an exception happens, we mark the instance as invalid, store an
        error message and reraise the exception again.
        This is intended to be use only during retrieval operations inside the
        value() method. It is not recommended in any other case.

        Arguments:
            None

        Returns:
            ContextManager - A context specifically created to handle a retrieval process
        """
        logger.debug(f"At { qualified_class_name(self) } - Start retrieval")

        try:
            self.enforce_validation()
            yield
        except Exception as exc:
            logger.debug(f"At { qualified_class_name(self) } - Exception during retrieval")

            self._is_valid = False
            msg = f"Exception during retrieval: {exc}"
            if msg not in self._errors:
                self._errors.append(msg)
            raise exc

        logger.debug(f"At { qualified_class_name(self) } - End retrieval")
