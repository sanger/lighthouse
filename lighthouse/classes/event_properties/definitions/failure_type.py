import logging
from functools import cached_property

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.constants.fields import FIELD_FAILURE_TYPE

logger = logging.getLogger(__name__)


class FailureType(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.validate_param_not_missing(FIELD_FAILURE_TYPE)
        self.validate_param_not_empty(FIELD_FAILURE_TYPE)
        self.validate_param_no_whitespaces(FIELD_FAILURE_TYPE)

        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_FAILURE_TYPE)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        message.add_metadata("failure_type", self.value)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
