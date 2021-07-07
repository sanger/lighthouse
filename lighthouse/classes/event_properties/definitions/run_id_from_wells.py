from typing import List
from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.constants.fields import FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID

import logging

logger = logging.getLogger(__name__)


class RunIDFromWells(EventPropertyAbstract):
    def __init__(self, wells_from_destination: EventPropertyInterface):
        self.reset()
        self._wells_from_destination = wells_from_destination

    def is_valid(self):
        return self._wells_from_destination.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._wells_from_destination.errors))

    # cherrytrack samples
    def _well_samples(self):
        val = []
        for sample in self._wells_from_destination.value:
            if sample["type"] == "sample":
                val.append(sample)
        return val

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return max(
                [sample[FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_RUN_ID] for sample in self._well_samples()]
            )

    def add_to_warehouse_message(self, message):
        pass

    def add_to_sequencescape_message(self, message):
        pass
