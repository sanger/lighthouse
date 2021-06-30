from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.constants.fields import FIELD_EVENT_BARCODE

import logging

logger = logging.getLogger(__name__)


class BarcodeNoPlateMapData(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.is_valid_param_not_missing(FIELD_EVENT_BARCODE)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message):
        message.add_metadata("source_plate_barcode", self.value)
