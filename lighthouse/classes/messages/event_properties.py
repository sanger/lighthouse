from abc import ABC, abstractmethod
from functools import cached_property
from lighthouse.classes.messages.warehouse_messages import (  # type: ignore
    WarehouseMessage,
    ROLE_TYPE_CP_SOURCE_LABWARE,
    SUBJECT_TYPE_PLATE,
    ROLE_TYPE_ROBOT,
    SUBJECT_TYPE_ROBOT,
)
from typing import Any, List, Dict
from lighthouse.classes.mixins.services.cherrytrack import ServiceCherrytrackMixin  # type: ignore
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

    @abstractmethod
    def validate(self) -> bool:
        """
        Retuns a boolean (True or False) indicating if the params received for this
        EventProperty are correct in order to retrieve the data. If there is an error
        in validation it will add it to the errors list.
        This methods is safe and should not raise any exception.

        Arguments:
            None

        Returns:
            bool - True/False depending on the result of the validation.

        """
        ...

    def valid(self) -> bool:
        """Alias for #validate()"""

        return self.validate()

    @abstractmethod
    def value(self) -> Any:
        """
        Returns the value for the property. If the value cannot be obtained or
        does not have a valid value, then it raises an exception.
        NB: To avoid this it, the instance should be checked first with the
        validate() method.

        Arguments:
            None

        Returns:
            Any - Value of the property

        """
        ...

    @abstractmethod
    def add_to_warehouse_message(self, message: WarehouseMessage) -> None:
        """
        Adds this event property information into the warehouse message

        Arguments:
            message: WarehouseMessage - A building message where we want to write
            the information from this event property

        Returns:
            None

        """
        ...

    def enforce_validation(self):
        """
        Raises a ValidationError exception if the instance does not pass validation.

        Arguments:
            None

        Returns:
            ValidationError - Raises exception

        """
        if not self.validate():
            raise ValidationError("Validation error")


class RunID(EventPropertyAccessor):
    def validate(self):
        return self._params.get("automation_system_run_id") is not None

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get("automation_system_run_id")

    def add_to_warehouse_message(self, message):
        return None


class PlateBarcode(EventPropertyAccessor):
    def validate(self):
        return self._params.get("barcode") is not None

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get("barcode")

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class RunInfo(EventPropertyAccessor, ServiceCherrytrackMixin):
    def __init__(self, run_id_property: RunID):
        self.run_id_property = run_id_property

    def validate(self):
        return self.run_id_property.validate()

    @cached_property
    def value(self):
        super().enforce_validation()
        val = self.get_run_info(self.run_id_property.value)
        # TODO: handle more than None, but empty object? or include errors field
        if val is None:
            raise Exception(f"Unable to determine a run info for run id '{self.run_id_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        return None


class PickedSamplesFromSource(EventPropertyAccessor, ServiceCherrytrackMixin):
    def __init__(self, barcode_property: PlateBarcode, run_info: RunInfo):
        self.barcode_property = barcode_property
        self.run_info = run_info

    def validate(self):
        return self.barcode_property.validate() and self.run_info.validate()

    @cached_property
    def value(self):
        super().enforce_validation()
        val: List[Dict[str, Any]] = list(
            filter(
                self.filter_pickable_samples,
                self.get_samples_from_source_plates(self.barcode_property.value, self.run_info.value),
            )
        )
        if val is None:
            raise Exception(f"Unable to obtain any samples picked from '{self.barcode_property.value}'")
        return val

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class UserID(EventPropertyAccessor):
    def validate(self):
        return self._params.get("user_id") is not None

    @cached_property
    def value(self):
        super().enforce_validation()

        val = self._params.get("user_id")
        if val is None:
            raise RetrievalError("Unable to determine a user id")
        return val

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)


class RobotSerialNumber(EventPropertyAccessor):
    def validate(self):
        return self._params.get("robot") is not None

    @cached_property
    def value(self):
        super().enforce_validation()
        return self._params.get("robot")

    def add_to_warehouse_message(self, message):
        return None


class RobotUUID(EventPropertyAccessor, ServiceCherrytrackMixin):
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
