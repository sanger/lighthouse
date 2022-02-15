import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.dart import DartServiceMixin

from lighthouse.classes.event_properties.definitions import PlateBarcode


logger = logging.getLogger(__name__)


class DartSamplesFromSource(EventPropertyAbstract, DartServiceMixin):
    """
    All samples from dart for destination plate barcode
    """

    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self._barcode_property = barcode_property

    def is_valid(self):
        return self._barcode_property.is_valid() and len(self._dart_samples == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._barcode_property.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            self._dart_samples = self.get_samples_for_destination_barcode(self._barcode_property.value)
            return self._dart_samples

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
