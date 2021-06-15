from abc import ABC, abstractmethod
from functools import cached_property
from .warehouse_messages import WarehouseMessage  # type: ignore
from typing import Any
from lighthouse.classes.plate_event import (
    ROLE_TYPE_CP_SOURCE_LABWARE,
    SUBJECT_TYPE_PLATE,
    ROLE_TYPE_ROBOT,
    SUBJECT_TYPE_ROBOT,
)
from lighthouse.classes.mixins.services.cherry_tracker import ServiceCherryTrackerMixin  # type: ignore
from lighthouse.classes.mixins.services.mongo import ServiceMongoMixin  # type: ignore

from flask import current_app as app


class ValidationError(BaseException):
    pass


class RetrievalError(BaseException):
    pass


class EventPropertyAccessor(ABC):
    def __init__(self, params):
        self._params = params
        if self._params is None:
            raise ValidationError("You need to define params to create the EventProperty")

    # Retuns a boolean (True or False) indicating if the params received for this
    # EventProperty have a valid value and can be used to send a request.
    @abstractmethod
    def validate(self):
        ...

    def valid(self):
        return self.validate()

    # Returns the value for the property. If the value cannot be obtained or
    # does not have a valid value, then it raises an exception.
    # NB: To avoid this it, the instance should be checked first with the
    # valid() method.
    @abstractmethod
    def value(self):
        ...

    @abstractmethod
    def add_to_warehouse_message(self, message: WarehouseMessage) -> Any:
        ...

    def enforce_validation(self):
        if not self.validate():
            raise ValidationError("Validation error")


class RunID(EventPropertyAccessor):
    def validate(self):
        return self._params.get("automation_system_run_id") is not None

    @cached_property
    def value(self):
        val = self._params.get("automation_system_run_id")
        if val is None:
            raise Exception("Unable to determine run id")
        return val

    def add_to_warehouse_message(self, message):
        return None


class PlateBarcode(EventPropertyAccessor):
    def validate(self):
        return self._params.get("barcode") is not None

    @cached_property
    def value(self):
        val = self._params.get("barcode")
        if val is None:
            raise Exception("Unable to obtain barcode value'")
        return val

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class RunInfo(EventPropertyAccessor, ServiceCherryTrackerMixin):
    def __init__(self, run_id_property: RunID):
        self.run_id_property = run_id_property

    def validate(self):
        return self.run_id_property.validate()

    @cached_property
    def value(self):
        val = self.get_run_info(self.run_id_property.value)
        # TODO: handle more than None, but empty object? or include errors field
        if val is None:
            raise Exception(f"Unable to determine a run info for run id '{self.run_id_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        return None


class PickedSamplesFromSource(EventPropertyAccessor, ServiceCherryTrackerMixin, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode, run_property: RunInfo):
        import pdb

        pdb.set_trace()
        self.barcode_property = barcode_property
        self.run_property = run_property

    def validate(self):
        return self.barcode_property.validate() and self.run_property.validate()

    @cached_property
    # read from client
    # values should have sample fields
    def value(self):
        val = self.get_samples_from_mongo(
            self.filter_pickable_samples(
                self.get_samples_from_source_plates(self.run_property.value, self.barcode_property.value)
            )
        )
        if val is None:
            raise Exception(f"Unable to obtain any samples picked from '{self.barcode_property.value}'")
        return val

    # use value list of sample and write
    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


##
#
##
class UserID(EventPropertyAccessor):
    @cached_property
    def value(self):
        super().enforce_validation()

        val = self._params.get("user_id")
        if val is None:
            raise RetrievalError("Unable to determine a user id")
        return val

    def validate(self):
        return self._params.get("user_id") is not None

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)


class RobotSerialNumber(EventPropertyAccessor):
    @cached_property
    def value(self):
        super().enforce_validation()
        val = self._params.get("robot")
        if val is None:
            raise RetrievalError("Unable to determine robot")
        return val

    def validate(self):
        return self._params.get("robot") is not None

    def add_to_warehouse_message(self, message):
        return None


class RobotUUID(EventPropertyAccessor, ServiceCherryTrackerMixin):
    def __init__(self, robot_serial_number_property: RobotSerialNumber):
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


class SourcePlateUUID(EventPropertyAccessor, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.barcode_property = barcode_property

    def validate(self):
        return self.barcode_property.validate()

    @cached_property
    def value(self):
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
