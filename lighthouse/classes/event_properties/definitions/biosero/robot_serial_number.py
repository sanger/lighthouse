import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.classes.messages import SequencescapeMessage
from lighthouse.classes.messages import WarehouseMessage
from lighthouse.constants.fields import FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER

logger = logging.getLogger(__name__)


class RobotSerialNumber(EventPropertyAbstract):
    def __init__(self, run_info: EventPropertyInterface):
        self.reset()
        self._run_info = run_info

    def is_valid(self):
        return self._run_info.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._run_info.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._run_info.value[FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER]

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
