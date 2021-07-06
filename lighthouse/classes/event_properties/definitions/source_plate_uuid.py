from typing import List
from functools import cached_property
from .plate_barcode import PlateBarcode
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.exceptions import RetrievalError
from lighthouse.classes.services.mongo import MongoServiceMixin
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_CP_SOURCE_LABWARE, SUBJECT_TYPE_PLATE

import logging

logger = logging.getLogger(__name__)


class SourcePlateUUID(EventPropertyAbstract, MongoServiceMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self._barcode_property = barcode_property

    def is_valid(self):
        return self._barcode_property.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._barcode_property.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self.get_source_plate_uuid(self._barcode_property.value)
            if val is None:
                raise RetrievalError(f"Unable to determine a uuid for source plate '{self._barcode_property.value}'")
            return val

    def add_to_warehouse_message(self, message):
        message.add_subject(
            role_type=ROLE_TYPE_CP_SOURCE_LABWARE,
            subject_type=SUBJECT_TYPE_PLATE,
            friendly_name=self._barcode_property.value,
            uuid=self.value,
        )

    def add_to_sequencescape_message(self, message):
        pass
