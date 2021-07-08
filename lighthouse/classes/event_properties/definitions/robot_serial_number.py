import logging
from functools import cached_property

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.constants.fields import FIELD_EVENT_ROBOT

logger = logging.getLogger(__name__)


class RobotSerialNumber(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.validate_param_not_missing(FIELD_EVENT_ROBOT)
        self.validate_param_not_empty(FIELD_EVENT_ROBOT)
        self.validate_param_no_whitespaces(FIELD_EVENT_ROBOT)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_ROBOT)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
