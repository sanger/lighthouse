import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.mongo import MongoServiceMixin

from .plate_barcode import PlateBarcode

logger = logging.getLogger(__name__)


class SamplesFromSource(EventPropertyAbstract, MongoServiceMixin):
    """
    All samples from mongo for source plate barcode
    """

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
            return self.get_samples_from_mongo_for_barcode(self._barcode_property.value)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        for sample in self.value:
            message.add_sample_as_subject(sample)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
