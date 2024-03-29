import logging
from functools import cached_property
from typing import Any, Dict, List

from lighthouse.classes.event_properties.definitions import PlateBarcode, RunID
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.cherrytrack import CherrytrackServiceMixin
from lighthouse.classes.services.mongo import MongoServiceMixin
from lighthouse.constants.fields import FIELD_CHERRYTRACK_LH_SAMPLE_UUID, FIELD_EVENT_RUN_ID

logger = logging.getLogger(__name__)


class SamplesPickedFromSource(EventPropertyAbstract, CherrytrackServiceMixin, MongoServiceMixin):
    def __init__(self, barcode_property: PlateBarcode, run_id_property: RunID):
        self.reset()
        self._barcode_property = barcode_property
        self._run_id_property = run_id_property

    def is_valid(self):
        return self._barcode_property.is_valid() and self._run_id_property.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._barcode_property.errors + self._run_id_property.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            lh_sample_uuids: List[str] = [
                sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID]
                for sample in filter(
                    lambda sample: sample[FIELD_EVENT_RUN_ID] == self._run_id_property.value,
                    filter(
                        self.filter_pickable_samples,
                        self.get_samples_from_source_plates(self._barcode_property.value),
                    ),
                )
            ]
            val: List[Dict[str, Any]] = list(self.get_samples_from_mongo(lh_sample_uuids))
            return val

    def add_to_warehouse_message(self, message: WarehouseMessage):
        for sample in self.value:
            message.add_sample_as_subject(sample)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
