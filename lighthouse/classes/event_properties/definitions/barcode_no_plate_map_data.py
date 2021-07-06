import logging
from functools import cached_property

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.classes.messages import SequencescapeMessage
from lighthouse.classes.messages import WarehouseMessage
from lighthouse.constants.fields import FIELD_EVENT_BARCODE

logger = logging.getLogger(__name__)


class BarcodeNoPlateMapData(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.validate_param_not_missing(FIELD_EVENT_BARCODE)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        message.add_metadata("source_plate_barcode", self.value)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
