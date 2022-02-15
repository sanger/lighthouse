import logging
from functools import cached_property
from typing import List, Dict

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage

logger = logging.getLogger(__name__)


class ClassifiedSamplesByCentre(EventPropertyAbstract):
    """
    Classify samples from mongo based on the centre
    """

    def __init__(self, mongo_samples: CherryPickedSamplesFromSource):
        self.reset()
        self._mongo_samples = mongo_samples

    def is_valid(self):
        return self._mongo_samples.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._mongo_samples.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._classify_samples_by_centre(self._mongo_samples)

    def _classify_samples_by_centre(self, samples: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        classified_samples = {}  # type: ignore
        for sample in samples:
            centre_name = sample[FIELD_SOURCE]
            if centre_name in classified_samples:
                classified_samples[centre_name].append(sample)
            else:
                classified_samples[centre_name] = [sample]
        return classified_samples

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass

    