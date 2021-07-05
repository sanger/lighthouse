from typing import List
from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.classes.services.mongo import MongoServiceMixin
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_CP_SOURCE_LABWARE, SUBJECT_TYPE_PLATE
from lighthouse.constants.fields import FIELD_BARCODE, FIELD_LH_SOURCE_PLATE_UUID


import logging

logger = logging.getLogger(__name__)


class SourcePlatesFromDestination(EventPropertyAbstract, MongoServiceMixin):
    def __init__(self, wells_from_destination: EventPropertyInterface):
        self.reset()
        self._wells_from_destination = wells_from_destination

    def is_valid(self):
        return self._wells_from_destination.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._wells_from_destination.errors))

    def _source_barcodes(self):
        val = set()
        for sample in self._wells_from_destination.value:
            if sample["type"] == "sample":
                if sample["source_barcode"] not in val:
                    val.add(sample["source_barcode"])
        return list(val)

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return list(self.get_source_plates_from_barcodes(self._source_barcodes()))

    def add_to_warehouse_message(self, message):
        for source_plate in self.value:
            message.add_subject(
                role_type=ROLE_TYPE_CP_SOURCE_LABWARE,
                subject_type=SUBJECT_TYPE_PLATE,
                friendly_name=source_plate[FIELD_BARCODE],
                uuid=source_plate[FIELD_LH_SOURCE_PLATE_UUID],
            )
