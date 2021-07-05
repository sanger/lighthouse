from typing import List
from functools import cached_property
from lighthouse.classes.event_properties.definitions import RunID
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.services.cherrytrack import CherrytrackServiceMixin
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_RUN, SUBJECT_TYPE_RUN

import logging

logger = logging.getLogger(__name__)


class RunInfo(EventPropertyAbstract, CherrytrackServiceMixin):
    def __init__(self, run_id_property: RunID):
        self.reset()
        self._run_id_property = run_id_property

    def is_valid(self):
        return self._run_id_property.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._run_id_property.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_run_info(self._run_id_property.value)

    @property
    def run_id(self):
        return self.value["id"]

    def add_to_warehouse_message(self, message):
        message.add_subject(
            role_type=ROLE_TYPE_RUN,
            subject_type=SUBJECT_TYPE_RUN,
            friendly_name=self.run_id,
        )
