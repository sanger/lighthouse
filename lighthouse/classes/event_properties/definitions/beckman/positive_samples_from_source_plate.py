import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.mongo import MongoServiceMixin

from lighthouse.classes.event_properties.definitions import SourcePlateUUID

logger = logging.getLogger(__name__)


class PositiveSamplesFromSource(EventPropertyAbstract, MongoServiceMixin):
    """
    Positive samples from mongo for a source plate uuid
    """

    def __init__(self, source_plate_uuid: SourcePlateUUID):
        self.reset()
        self._source_plate_uuid = source_plate_uuid

    def is_valid(self):
        return self._source_plate_uuid.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._source_plate_uuid.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self.get_positive_samples_in_source_plate(self._source_plate_uuid.value)

    def add_to_warehouse_message(self, message: WarehouseMessage):
        for sample in self.value:
            message.add_sample_as_subject(sample)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
