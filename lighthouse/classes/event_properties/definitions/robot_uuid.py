from typing import List
from functools import cached_property
from .robot_serial_number import RobotSerialNumber
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, RetrievalError
from lighthouse.classes.services.cherrytrack import CherrytrackServiceMixin
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_ROBOT, SUBJECT_TYPE_ROBOT
from flask import current_app as app

import logging

logger = logging.getLogger(__name__)


class RobotUUID(EventPropertyAbstract, CherrytrackServiceMixin):
    def __init__(self, robot_serial_number_property: RobotSerialNumber):
        self.reset()
        self.robot_serial_number_property = robot_serial_number_property

    def is_valid(self):
        return self.robot_serial_number_property.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return self._errors + self.robot_serial_number_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self._get_robot_uuid()
            if val is None:
                raise Exception(f"Unable to determine a uuid for robot '{self.robot_serial_number_property.value}'")
            return val

    def add_to_warehouse_message(self, message):
        message.add_subject(
            role_type=ROLE_TYPE_ROBOT,
            subject_type=SUBJECT_TYPE_ROBOT,
            friendly_name=self.robot_serial_number_property.value,
            uuid=self.value,
        )

    def _get_robot_uuid(self):
        if self.robot_serial_number_property.value in app.config["BIOSERO_ROBOTS"].keys():
            return app.config["BIOSERO_ROBOTS"][self.robot_serial_number_property.value]["uuid"]
        else:
            raise RetrievalError(f"Robot with barcode {self.robot_serial_number_property.value} not found")
