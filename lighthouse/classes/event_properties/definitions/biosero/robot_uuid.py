import logging
from functools import cached_property
from typing import List

from flask import current_app as app

from lighthouse.classes.event_properties.exceptions import RetrievalError
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_ROBOT, SUBJECT_TYPE_ROBOT
from lighthouse.classes.services.cherrytrack import CherrytrackServiceMixin

logger = logging.getLogger(__name__)


class RobotUUID(EventPropertyAbstract, CherrytrackServiceMixin):
    def __init__(self, automation_system_name: EventPropertyInterface):
        self.reset()
        self._automation_system_name = automation_system_name

    def is_valid(self):
        return self._automation_system_name.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._automation_system_name.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._get_robot_uuid()

    def add_to_warehouse_message(self, message: WarehouseMessage):
        message.add_subject(
            role_type=ROLE_TYPE_ROBOT,
            subject_type=SUBJECT_TYPE_ROBOT,
            friendly_name=self._automation_system_name.value,
            uuid=self.value,
        )

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass

    def _get_robot_uuid(self) -> str:
        if self._automation_system_name.value in app.config["BIOSERO_ROBOTS"].keys():
            val: str = app.config["BIOSERO_ROBOTS"][self._automation_system_name.value]["uuid"]
            if val is None:
                raise RetrievalError(f"Unable to determine a uuid for robot '{self._automation_system_name.value}'")
            return val
        else:
            raise RetrievalError(f"Robot with barcode {self._automation_system_name.value} not found")
