import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.exceptions import RetrievalError
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.mongo import MongoServiceMixin
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_CONTROL,
    FIELD_CHERRYTRACK_CONTROL_BARCODE,
    FIELD_CHERRYTRACK_CONTROL_COORDINATE,
    FIELD_SS_CONTROL,
    FIELD_SS_CONTROL_TYPE,
    FIELD_SS_SUPPLIER_NAME,
)

logger = logging.getLogger(__name__)


class ControlsFromDestination(EventPropertyAbstract, MongoServiceMixin):
    def __init__(self, wells_from_destination: EventPropertyInterface):
        self.reset()
        self._wells_from_destination = wells_from_destination

    def is_valid(self):
        return self._wells_from_destination.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._wells_from_destination.errors))

    def _is_valid_positive_and_negative_present(self, wells):
        control_types = [well["control"] for well in wells]
        control_types.sort()
        if control_types != ["negative", "positive"]:
            raise RetrievalError("We were expecting one positive and one negative control to be present.")

    def _well_controls(self):
        val = []
        for well in self._wells_from_destination.value:
            if well["type"] == "control":
                val.append(well)
        return val

    def _mapping_with_controls(self):
        mapping = {}
        for control in self._well_controls():
            mapping[control["destination_coordinate"]] = control
        return mapping

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self._well_controls()
            self._is_valid_positive_and_negative_present(val)
            return self._mapping_with_controls()

    def add_to_warehouse_message(self, message: WarehouseMessage):
        for control in self.value.values():
            message.add_subject(
                role_type="control",
                subject_type="sample",
                friendly_name=self._supplier_name_for_control(control),
            )

    def _supplier_name_for_control(self, control):
        return (
            f"{control[FIELD_CHERRYTRACK_CONTROL]} control: {control[FIELD_CHERRYTRACK_CONTROL_BARCODE]}_"
            f"{control[FIELD_CHERRYTRACK_CONTROL_COORDINATE]}"
        )

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        for position in self.value:
            control = self.value[position]
            message.set_well_sample(
                position,
                {
                    FIELD_SS_SUPPLIER_NAME: self._supplier_name_for_control(control),
                    FIELD_SS_CONTROL: True,
                    FIELD_SS_CONTROL_TYPE: control[FIELD_CHERRYTRACK_CONTROL],
                },
            )
