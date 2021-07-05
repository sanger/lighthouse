from typing import Dict, Any, List, Optional
from .event_property_interface import EventPropertyInterface
from lighthouse.classes.event_properties.exceptions import ValidationError
from contextlib import contextmanager

import sys
import logging

logger = logging.getLogger(__name__)


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

    def get_param_value(self, param_name: str) -> Optional[Any]:
        """
        Returns the param of the value

        Arguments:
            param_name: str - Name of the param to get the value

        Returns:
            Optional[Any] - value for the param, or None if no value
        """
        return self._params.get(param_name)

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
        try:
            yield
        except Exception as exc:
            logger.debug(f"At { self._source_code_position_for_logging() } - Exception during validation")

            self._is_valid = False
            msg = f"Unexpected exception while trying to is_valid {exc}"
            if msg not in self._errors:
                self._errors.append(msg)
            logger.exception(exc)

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
        logger.info(f"At { self._source_code_position_for_logging() } - Start retrieval")

        try:
            self.enforce_validation()
            yield
        except Exception as exc:
            logger.error(f"At { self._source_code_position_for_logging() } - Exception during retrieval")

            self._is_valid = False
            msg = f"Exception during retrieval: {exc}"
            if msg not in self._errors:
                self._errors.append(msg)
            raise exc

        logger.info(f"At { self._source_code_position_for_logging() } - End retrieval")

    def _source_code_position_for_logging(self):
        klass = type(self)
        frame = sys._getframe(3)
        function_name = frame.f_code.co_name
        line_no = frame.f_lineno

        return f"{ klass.__qualname__ }::{ function_name } - line { line_no }"
