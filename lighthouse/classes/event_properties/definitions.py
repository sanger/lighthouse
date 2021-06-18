
from functools import cached_property
from lighthouse.classes.messages.warehouse_messages import (  # type: ignore
    ROLE_TYPE_CP_SOURCE_LABWARE,
    SUBJECT_TYPE_PLATE,
    ROLE_TYPE_ROBOT,
    SUBJECT_TYPE_ROBOT,
)
from lighthouse.classes.messages.event_property_interfaces import EventPropertyAbstract
from typing import Any, List, Dict
from lighthouse.classes.mixins.services.cherrytrack import ServiceCherrytrackMixin  # type: ignore
from lighthouse.classes.mixins.services.mongo import ServiceMongoMixin  # type: ignore

from lighthouse.constants.fields import FIELD_EVENT_RUN_ID, FIELD_EVENT_ROBOT, FIELD_EVENT_USER_ID, FIELD_EVENT_BARCODE
from lighthouse.classes.messages.event_property_validations import SimpleEventPropertyMixin
from flask import current_app as app
import logging

logger = logging.getLogger(__name__)


class RunID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self._validate_param_not_missing(FIELD_EVENT_RUN_ID)
        self._validate_param_is_integer(FIELD_EVENT_RUN_ID)
        return self._validate

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get(FIELD_EVENT_RUN_ID)

    def add_to_warehouse_message(self, message):
        return None


class PlateBarcode(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self._validate_param_not_missing(FIELD_EVENT_BARCODE)
        self._validate_param_not_empty(FIELD_EVENT_BARCODE)
        self._validate_param_no_whitespaces(FIELD_EVENT_BARCODE)
        return self._validate

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class RunInfo(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, run_id_property: RunID):
        self.reset()
        self.run_id_property = run_id_property

    def validate(self):
        return self.run_id_property.validate()

    @cached_property
    def value(self):
        super().enforce_validation()
        return self.get_run_info(self.run_id_property.value)

    def add_to_warehouse_message(self, message):
        return None


class PickedSamplesFromSource(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, barcode_property: PlateBarcode, run_info_property: RunInfo):
        self.reset()
        self.barcode_property = barcode_property
        self.run_info_property = run_info_property

    def validate(self):
        return self.barcode_property.validate() and self.run_info_property.validate()

    @cached_property
    def value(self):
        super().enforce_validation()

        # TODO: Filter by run_id from this list
        val: List[Dict[str, Any]] = list(
            filter(
                self.filter_pickable_samples,
                self.get_samples_from_source_plates(self.barcode_property.value),
            )
        )

        return val

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class UserID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self._validate_param_not_missing(FIELD_EVENT_USER_ID)
        self._validate_param_not_empty(FIELD_EVENT_USER_ID)
        self._validate_param_no_whitespaces(FIELD_EVENT_USER_ID)
        return self._validate

    @cached_property
    def value(self):
        super().enforce_validation()

        val = self._params.get(FIELD_EVENT_USER_ID)
        if val is None:
            raise RetrievalError("Unable to determine a user id")
        return val

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)


class RobotSerialNumber(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self._validate_param_not_missing(FIELD_EVENT_ROBOT)
        self._validate_param_not_empty(FIELD_EVENT_ROBOT)
        self._validate_param_no_whitespaces(FIELD_EVENT_ROBOT)
        return self._validate

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get(FIELD_EVENT_ROBOT)

    def add_to_warehouse_message(self, message):
        return None


class RobotUUID(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, robot_serial_number_property: RobotSerialNumber):
        self.reset()
        self.robot_serial_number_property = robot_serial_number_property

    def validate(self):
        return self.robot_serial_number_property.validate()

    @cached_property
    def value(self):
        super().enforce_validation()
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
            raise RetrievalError(f"Robot with barcode %{self.robot_serial_number_property.value} not found")


class SourcePlateUUID(EventPropertyAbstract, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self.barcode_property = barcode_property

    def validate(self):
        return self.barcode_property.validate()

    @cached_property
    def value(self):
        super().enforce_validation()
        val = self.get_source_plate_uuid(self.barcode_property.value)
        if val is None:
            raise Exception(f"Unable to determine a uuid for source plate '{self.barcode_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        message.add_subject(
            role_type=ROLE_TYPE_CP_SOURCE_LABWARE,
            subject_type=SUBJECT_TYPE_PLATE,
            friendly_name=self.barcode_property.value,
            uuid=self.value,
        )
