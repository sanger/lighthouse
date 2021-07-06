import logging
from functools import cached_property

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.event_properties.validations import SimpleEventPropertyMixin
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.messages.warehouse_messages import ROLE_TYPE_CP_DESTINATION_LABWARE, SUBJECT_TYPE_PLATE
from lighthouse.constants.fields import FIELD_EVENT_BARCODE

logger = logging.getLogger(__name__)


class PlateBarcode(EventPropertyAbstract, SimpleEventPropertyMixin):
    def is_valid(self):
        self.validate_param_not_missing(FIELD_EVENT_BARCODE)
        self.validate_param_not_empty(FIELD_EVENT_BARCODE)
        self.validate_param_no_whitespaces(FIELD_EVENT_BARCODE)
        return self._is_valid

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._params.get(FIELD_EVENT_BARCODE)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        message.add_subject(
            role_type=ROLE_TYPE_CP_DESTINATION_LABWARE,
            subject_type=SUBJECT_TYPE_PLATE,
            friendly_name=self.value,
        )

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        message.set_barcode(self.value)
