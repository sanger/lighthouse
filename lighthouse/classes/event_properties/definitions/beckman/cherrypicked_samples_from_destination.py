import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.mongo import MongoServiceMixin

from lighthouse.classes.event_properties.definitions import PlateBarcode, SourcePlateUUID

logger = logging.getLogger(__name__)


class CherryPickedSamplesFromSource(EventPropertyAbstract, MongoServiceMixin):
    """
    Positive samples from mongo for a source plate uuid
    """

    def __init__(self, dart_samples: DartSamplesFromSource):
        self.reset()
        self._dart_samples = dart_samples

    def is_valid(self):
        return self._dart_samples.is_valid() and self._mongo_samples

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._dart_samples.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            self._mongo_samples = self.find_samples(
                self.query_for_cherrypicked_samples(self._dart_samples.value))
            return self._mongo_samples

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass

    