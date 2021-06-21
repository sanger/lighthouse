from functools import cached_property
from lighthouse.classes.messages.warehouse_messages import (  # type: ignore
    ROLE_TYPE_CP_SOURCE_LABWARE,
    SUBJECT_TYPE_PLATE,
    ROLE_TYPE_ROBOT,
    SUBJECT_TYPE_ROBOT,
    ROLE_TYPE_RUN,
    SUBJECT_TYPE_RUN,
)
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, RetrievalError  # type: ignore
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin  # type: ignore
from typing import Any, List, Dict
from lighthouse.classes.services.cherrytrack import ServiceCherrytrackMixin  # type: ignore
from lighthouse.classes.services.mongo import ServiceMongoMixin  # type: ignore
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_LH_SAMPLE_UUID,
    FIELD_EVENT_RUN_ID,
    FIELD_EVENT_ROBOT,
    FIELD_EVENT_USER_ID,
    FIELD_EVENT_BARCODE,
)

from flask import current_app as app
import logging

logger = logging.getLogger(__name__)


class RunID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self.validate_param_not_missing(FIELD_EVENT_RUN_ID)
        self.validate_param_is_integer(FIELD_EVENT_RUN_ID)
        return self._validate

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_RUN_ID)

    def add_to_warehouse_message(self, message):
        return None


class PlateBarcode(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self.validate_param_not_missing(FIELD_EVENT_BARCODE)
        self.validate_param_not_empty(FIELD_EVENT_BARCODE)
        self.validate_param_no_whitespaces(FIELD_EVENT_BARCODE)
        return self._validate

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message):
        return None


class RunInfo(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, run_id_property: RunID):
        self.reset()
        self.run_id_property = run_id_property

    def validate(self):
        return self.run_id_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.run_id_property.errors  # type: ignore

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_run_info(self.run_id_property.value)

    @property
    def run_id(self):
        return self.value['id']

    def add_to_warehouse_message(self, message):
        message.add_subject(
            role_type=ROLE_TYPE_RUN,
            subject_type=SUBJECT_TYPE_RUN,
            friendly_name=self.run_id,
        )


class PickedSamplesFromSource(EventPropertyAbstract, ServiceCherrytrackMixin, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode, run_id_property: RunID):
        self.reset()
        self.barcode_property = barcode_property
        self.run_id_property = run_id_property

    def validate(self):
        return self.barcode_property.validate() and self.run_id_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.barcode_property.errors + self.run_id_property.errors  # type: ignore

    @cached_property
    def value(self):
        with self.retrieval_scope():
            sample_uuids: List[str] = [  # type: ignore
                sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID]
                for sample in filter(
                    lambda sample: sample[FIELD_EVENT_RUN_ID] == self.run_id_property.value,  # type: ignore
                    filter(
                        self.filter_pickable_samples,
                        self.get_samples_from_source_plates(self.barcode_property.value),
                    ),
                )
            ]
            val: List[Dict[str, Any]] = list(self.get_samples_from_mongo(sample_uuids))
            return val

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class AllSamplesFromSource(EventPropertyAbstract, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self.barcode_property = barcode_property

    def validate(self):
        return self.barcode_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.barcode_property.errors  # type: ignore

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_samples_from_mongo_for_barcode(self.barcode_property.value)

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)


class UserID(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self.validate_param_not_missing(FIELD_EVENT_USER_ID)
        self.validate_param_not_empty(FIELD_EVENT_USER_ID)
        return self._validate

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self._params.get(FIELD_EVENT_USER_ID)
            if val is None:
                raise RetrievalError("Unable to determine a user id")
            return val

    def add_to_warehouse_message(self, message):
        message.set_user_id(self.value)


class RobotSerialNumber(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self.validate_param_not_missing(FIELD_EVENT_ROBOT)
        self.validate_param_not_empty(FIELD_EVENT_ROBOT)
        self.validate_param_no_whitespaces(FIELD_EVENT_ROBOT)
        return self._validate

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_ROBOT)

    def add_to_warehouse_message(self, message):
        return None


class RobotUUID(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, robot_serial_number_property: RobotSerialNumber):
        self.reset()
        self.robot_serial_number_property = robot_serial_number_property

    def validate(self):
        return self.robot_serial_number_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.robot_serial_number_property.errors  # type: ignore

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
            raise RetrievalError(f"Robot with barcode %{self.robot_serial_number_property.value} not found")


class SourcePlateUUID(EventPropertyAbstract, ServiceMongoMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self.barcode_property = barcode_property

    def validate(self):
        return self.barcode_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.barcode_property.errors  # type: ignore

    @cached_property
    def value(self):
        with self.retrieval_scope():
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




class BarcodeNoPlateMapData(EventPropertyAbstract, SimpleEventPropertyMixin):
    def validate(self):
        self.validate_param_not_missing(FIELD_EVENT_BARCODE)
        return self._validate

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message):
        message.add_metadata('source_plate_barcode', self.value)

