from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, RetrievalError
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.constants.fields import (
    FIELD_EVENT_USER_ID
)


import logging

logger = logging.getLogger(__name__)


class UserID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.is_valid_param_not_missing(FIELD_EVENT_USER_ID)
        self.is_valid_param_not_empty(FIELD_EVENT_USER_ID)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self._params.get(FIELD_EVENT_USER_ID)
            if val is None:
                raise RetrievalError("Unable to determine a user id")
            return val

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)

