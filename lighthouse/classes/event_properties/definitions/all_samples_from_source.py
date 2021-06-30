from typing import List
from functools import cached_property
from .plate_barcode import PlateBarcode
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.services.mongo import MongoServiceMixin

import logging

logger = logging.getLogger(__name__)


# all samples from mongo for source plate barcode
class AllSamplesFromSource(EventPropertyAbstract, MongoServiceMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self._barcode_property = barcode_property

    def is_valid(self):
        return self._barcode_property.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return self._errors + self._barcode_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_samples_from_mongo_for_barcode(self._barcode_property.value)

    def add_to_warehouse_message(self, message):
        for sample in self.value:
            message.add_sample_as_subject(sample)
