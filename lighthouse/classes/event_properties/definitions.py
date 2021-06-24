from functools import cached_property
from lighthouse.classes.messages.warehouse_messages import (
    ROLE_TYPE_CP_SOURCE_LABWARE,
    SUBJECT_TYPE_PLATE,
    ROLE_TYPE_ROBOT,
    SUBJECT_TYPE_ROBOT,
    ROLE_TYPE_RUN,
    SUBJECT_TYPE_RUN,
)
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, RetrievalError
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from typing import Any, List, Dict
from lighthouse.classes.services.cherrytrack import ServiceCherrytrackMixin
from lighthouse.classes.services.mongo import ServiceMongoMixin
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_LH_SAMPLE_UUID,
    FIELD_EVENT_RUN_ID,
    FIELD_EVENT_ROBOT,
    FIELD_EVENT_USER_ID,
    FIELD_EVENT_BARCODE,
    FIELD_SS_NAME,
    FIELD_RNA_ID,
    FIELD_SS_SAMPLE_DESCRIPTION,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SS_SUPPLIER_NAME,
    FIELD_COG_BARCODE,
    FIELD_SS_PHENOTYPE,
    FIELD_RESULT,
    FIELD_SS_UUID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_SS_CONTROL,
    FIELD_SS_CONTROL_TYPE,
    FIELD_CHERRYTRACK_CONTROL,
    FIELD_CHERRYTRACK_CONTROL_BARCODE,
    FIELD_CHERRYTRACK_CONTROL_COORDINATE,
)

from lighthouse.helpers.plates import add_cog_barcodes_from_different_centres, update_mlwh_with_cog_uk_ids

from uuid import uuid4

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

    def add_to_sequencescape(self, message):
        message.add_barcode(self.value)


class RunInfo(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, run_id_property: RunID):
        self.reset()
        self.run_id_property = run_id_property

    def validate(self):
        return self.run_id_property.validate()

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.run_id_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_run_info(self.run_id_property.value)

    @property
    def run_id(self):
        return self.value["id"]

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
        return self._errors + self.barcode_property.errors + self.run_id_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            sample_uuids: List[str] = [
                sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID]
                for sample in filter(
                    lambda sample: sample[FIELD_EVENT_RUN_ID] == self.run_id_property.value,
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
        return self._errors + self.barcode_property.errors

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
        return self._errors + self.barcode_property.errors

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
        message.add_metadata("source_plate_barcode", self.value)


class CherrytrackWellsFromDestination(EventPropertyAbstract, ServiceCherrytrackMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self.barcode_property = barcode_property

    def validate(self):
        return self.barcode_property.validate() and (len(self._errors) == 0)

    def _validate_destination_coordinate_not_duplicated(self, wells):
        coordinates = [well["destination_coordinate"] for well in wells]
        duplicates = set([coor for coor in coordinates if coordinates.count(coor) > 1])
        if len(duplicates) > 0:
            raise RetrievalError(f"Some coordinates have clashing samples/controls: { duplicates }")

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.barcode_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self.get_wells_from_destination_plate(self.barcode_property.value)
            self._validate_destination_coordinate_not_duplicated(val)
            return val

    def add_to_warehouse_message(self, message):
        return None


class SamplesFromDestination(EventPropertyAbstract, ServiceMongoMixin):
    def __init__(self, cherrytrack_wells_from_destination: CherrytrackWellsFromDestination):
        self.reset()
        self.cherrytrack_wells_from_destination = cherrytrack_wells_from_destination

    def validate(self):
        return self.cherrytrack_wells_from_destination.validate() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.cherrytrack_wells_from_destination.errors

    def _well_samples(self):
        val = []
        for sample in self.cherrytrack_wells_from_destination.value:
            if sample["type"] == "sample":
                val.append(sample)
        return val

    def _validate_no_duplicate_uuids(self, uuids):
        duplicates = set([uuid for uuid in uuids if uuids.count(uuid) > 1])
        if len(duplicates) > 0:
            raise RetrievalError(f"There is duplication in the sample ids provided: { list(duplicates) }")

    def _get_sample_with_uuid(self, samples, uuid):
        for sample in samples:
            if sample["lh_sample_uuid"] == uuid:
                return sample
        raise RetrievalError(f"We could not find sample with uuid {uuid}")

    def _mapping_with_samples(self, samples):
        mapping = {}
        for well_sample in self._well_samples():
            uuid = well_sample["sample_id"]
            sample = self._get_sample_with_uuid(samples, uuid)
            mapping[well_sample["destination_coordinate"]] = sample
        return mapping

    def samples(self) -> Any:
        sample_uuids: List[str] = [sample["sample_id"] for sample in self._well_samples()]
        self._validate_no_duplicate_uuids(sample_uuids)
        return self.get_samples_from_mongo(sample_uuids)

    @cached_property
    def value(self):
        with self.retrieval_scope():
            obtained_samples = self.samples()
            return self._mapping_with_samples(obtained_samples)

    def add_to_warehouse_message(self, message):
        return None


class SamplesWithCogUkId(EventPropertyAbstract):
    def __init__(self, samples_from_destination: SamplesFromDestination):
        self.reset()
        self.samples_from_destination = samples_from_destination

    def validate(self):
        return self.samples_from_destination.validate() and (len(self._errors) == 0)

    @cached_property
    def value(self):
        with self.retrieval_scope():
            samples = list(self.samples_from_destination.value.values())
            add_cog_barcodes_from_different_centres(samples)
            update_mlwh_with_cog_uk_ids(samples)
            return self.samples_from_destination.value

    def add_to_warehouse_message(self, message):
        for sample in self.value.values():
            message.add_sample_as_subject(sample)

    def add_to_sequencescape_message(self, message):
        for position in self.value:
            sample = self.value[position]
            message.set_well_sample(
                position,
                {
                    FIELD_SS_NAME: sample[FIELD_RNA_ID],
                    FIELD_SS_SAMPLE_DESCRIPTION: sample[FIELD_ROOT_SAMPLE_ID],
                    FIELD_SS_SUPPLIER_NAME: sample[FIELD_COG_BARCODE],
                    FIELD_SS_PHENOTYPE: sample[FIELD_RESULT],
                    FIELD_SS_UUID: sample[FIELD_LH_SAMPLE_UUID],
                },
            )


class ControlsFromDestination(EventPropertyAbstract, ServiceMongoMixin):
    def __init__(self, cherrytrack_wells_from_destination: CherrytrackWellsFromDestination):
        self.reset()
        self.cherrytrack_wells_from_destination = cherrytrack_wells_from_destination

    def validate(self):
        return self.cherrytrack_wells_from_destination.validate() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.validate()
        return self._errors + self.cherrytrack_wells_from_destination.errors

    def _validate_positive_and_negative_present(self, wells):
        control_types = [well["control"] for well in wells]
        control_types.sort()
        if control_types != ["negative", "positive"]:
            raise RetrievalError("We were expecting one positive and one negative control to be present.")

    def _well_controls(self):
        val = []
        for well in self.cherrytrack_wells_from_destination.value:
            if well["type"] == "control":
                val.append(well)
        return val

    def _mapping_with_controls(self):
        mapping = {}
        for control in self._well_controls():
            if "uuid" not in control:
                control["uuid"] = str(uuid4())
            mapping[control["destination_coordinate"]] = control
        return mapping

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self._well_controls()
            self._validate_positive_and_negative_present(val)
            return self._mapping_with_controls()

    def add_to_warehouse_message(self, message):
        for control in self.value.values():
            message.add_subject(
                role_type="control",
                subject_type="sample",
                friendly_name=self._supplier_name_for_control(control),
                uuid=control["uuid"],
            )

    def _supplier_name_for_control(self, control):
        return (
            f"{control[FIELD_CHERRYTRACK_CONTROL]} control: {control[FIELD_CHERRYTRACK_CONTROL_BARCODE]}_"
            f"{control[FIELD_CHERRYTRACK_CONTROL_COORDINATE]}"
        )

    def add_to_sequencescape_message(self, message):
        for position, control in self.value:
            message.set_well_sample(
                position,
                {
                    FIELD_SS_SUPPLIER_NAME: self._supplier_name_for_control(control),
                    FIELD_SS_CONTROL: True,
                    FIELD_SS_CONTROL_TYPE: control[FIELD_CHERRYTRACK_CONTROL],
                    FIELD_SS_UUID: control["uuid"],
                },
            )
