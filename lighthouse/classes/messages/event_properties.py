from abc import ABC, abstractmethod
from typing import ContextManager
from lighthouse.helpers import mongo
from functools import cached_property
from .warehouse_messages import WarehouseMessage

from lighthouse.classes.mixins.services.cherry_tracker import ServiceCherryTrackerMixin
from lighthouse.classes.mixins.services.mongo import ServiceMongoMixin


class EventPropertyAccessor(ABC):
    def __init__(self, params):
        self._params = params
        if self._params is None:
            raise 'You need to define params to create the EventProperty'

    class ScopeForValidate(ContextManager):
        def __enter__(self):
            import pdb
            pdb.set_trace()

            self._validation = False
            try:
                if not self.preconditions_check():
                    self._validation = False
                    return
                yield
                self._validation = True
            except Exception:
                self._validation = False

        def __exit__(self, type, value, traceback):
            ...

    # Retuns a boolean (True or False) indicating if the value from this property
    # is a valid value and can be used. After obtaining a True value from this method
    # all subsequent calls with value() to this instance are considered be safe and
    # not to raise an error.
    def valid(self):
        import pdb
        pdb.set_trace()

        with EventPropertyAccessor.ScopeForValidate():
            import pdb
            pdb.set_trace()

            self.value
        return self._validate

    # Returns the value for the property. If the value cannot be obtained or
    # does not have a valid value, then it raises an exception.
    # NB: To avoid this it, the instance should be checked first with the
    # valid() method.
    @abstractmethod
    def value(self):
        ...

    def add_to_warehouse_message(self, message: WarehouseMessage):
        ...

    # Return a pre-validation of the instance by doing some checks on the inputs
    # before performing the most costly operations. Any validation checks we can
    # do without raising an exception should go in here.
    def preconditions_check(self):
        return self._params is not None


class RunID(EventPropertyAccessor):
    @cached_property
    def value(self):
        val = self._params.get("run_id")
        if (val is None):
            raise Exception("Unable to determine run id")
        return val

    def add_to_warehouse_message(self, message):
        return None


class PlateBarcode(EventPropertyAccessor):
    @cached_property
    def value(self):
        val = self._params.get("barcode")
        if (val is None):
            raise Exception("Unable to obtain barcode value'")
        return val

    def add_to_warehouse_message(self, message):
        for sample in self.value():
            message.add_subject(self.construct_mongo_sample_message_subject(sample))


class RunInfo(EventPropertyAccessor, ServiceCherryTrackerMixin):
    def __init__(self, run_id_property: RunID):
        self.run_id_property = run_id_property

    @cached_property
    def value(self):
        val = self.get_run_info(self.run_id_property.value)
        if val is None:
            raise Exception(f"Unable to determine a run info for run id '{self.run_id_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        return None


class PickedSamplesFromSource(EventPropertyAccessor, ServiceCherryTrackerMixin, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode, run_property: RunInfo):
        self.barcode_property = barcode_property
        self.run_property = run_property

    @cached_property
    def value(self):
        val = self.get_samples_from_mongo(self.filter_pickable_samples(
            self.get_samples_from_source_plates(self.run_property.value(), self.barcode_property.value())
        ))
        if val is None:
            raise Exception(f"Unable to obtain any samples picked from '{self.barcode_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        for sample in self.value():
            message.add_subject(self.construct_mongo_sample_message_subject(sample))


class UserID(EventPropertyAccessor):
    @cached_property
    def value(self):
        val = self._params.get("user_id")
        if val is None:
            raise Exception("Unable to determine a user id")
        return val

    def preconditions_check(self):
        return super().preconditions_check() and (self._params.get("user_id") is not None)

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)


class RobotSerialNumber(EventPropertyAccessor):
    @cached_property
    def value(self):
        val = self._params.get("robot")
        if val is None:
            raise Exception("Unable to determine robot")
        return val

    def add_to_warehouse_message(self, message):
        return None


class RobotUUID(EventPropertyAccessor, ServiceCherryTrackerMixin):
    def __init__(self, robot_serial_number_property: RobotSerialNumber):
        self.robot_serial_number_property = robot_serial_number_property

    @cached_property
    def value(self):
        val = self._event.get_robot_uuid(self.robot_serial_number_property.value)
        if val is None:
            raise Exception(f"Unable to determine a uuid for robot '{self.robot_serial_number_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        message.add_subject(self.construct_message_subject(
            role_type=self._event.ROLE_TYPE_ROBOT,
            subject_type=self._event.SUBJECT_TYPE_ROBOT,
            friendly_name=self.robot_serial_number_property.value,
            uuid=self.value,
        ))


class SourcePlateUUID(EventPropertyAccessor, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.barcode_property = barcode_property

    @cached_property
    def value(self):
        val = mongo.get_source_plate_uuid(self.barcode_property.value)
        if val is None:
            raise Exception(f"Unable to determine a uuid for source plate '{self.barcode_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        message.add_subject(self.construct_message_subject(
            role_type=self._event.ROLE_TYPE_CP_SOURCE_LABWARE,
            subject_type=self._event.SUBJECT_TYPE_PLATE,
            friendly_name=self.barcode_property.value,
            uuid=self.value,
        ))