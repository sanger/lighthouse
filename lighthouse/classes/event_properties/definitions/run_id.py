from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.constants.fields import (
    FIELD_EVENT_RUN_ID
)

import logging

logger = logging.getLogger(__name__)


class RunID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.is_valid_param_not_missing(FIELD_EVENT_RUN_ID)
        self.is_valid_param_is_integer(FIELD_EVENT_RUN_ID)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_RUN_ID)

    def add_to_warehouse_message(self, message):
        pass
