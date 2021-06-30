from typing import List, Any
from functools import cached_property
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract, EventPropertyInterface
from lighthouse.classes.event_properties.exceptions import RetrievalError
from lighthouse.classes.services.mongo import MongoServiceMixin
from lighthouse.constants.fields import FIELD_CHERRYTRACK_LH_SAMPLE_UUID

import logging

logger = logging.getLogger(__name__)


class SamplesFromDestination(EventPropertyAbstract, MongoServiceMixin):
    def __init__(self, wells_from_destination: EventPropertyInterface):
        self.reset()
        self._wells_from_destination = wells_from_destination

    def is_valid(self):
        return self._wells_from_destination.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return self._errors + self._wells_from_destination.errors

    # cherrytrack samples
    def _well_samples(self):
        val = []
        for sample in self._wells_from_destination.value:
            if sample["type"] == "sample":
                val.append(sample)
        return val

    def _is_valid_no_duplicate_uuids(self, uuids):
        duplicates = set([uuid for uuid in uuids if uuids.count(uuid) > 1])
        if len(duplicates) > 0:
            raise RetrievalError(f"There is duplication in the lh sample uuids provided: { list(duplicates) }")

    def _get_sample_with_uuid(self, samples, uuid):
        for sample in samples:
            if sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID] == uuid:
                return sample
        raise RetrievalError(f"We could not find sample with lh sample uuid {uuid}")

    def _mapping_with_samples(self, samples):
        mapping = {}
        for well_sample in self._well_samples():
            # get sample from mongo using cherrytrack sample id
            sample = self._get_sample_with_uuid(samples, well_sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID])
            mapping[well_sample["destination_coordinate"]] = sample
        return mapping

    # mongo samples from cherrytrack samples
    def samples(self) -> Any:
        lh_sample_uuids: List[str] = [sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID] for sample in self._well_samples()]
        self._is_valid_no_duplicate_uuids(lh_sample_uuids)
        return self.get_samples_from_mongo(lh_sample_uuids)

    @cached_property
    def value(self):
        with self.retrieval_scope():
            obtained_samples = self.samples()
            # mapping with mongo samples
            return self._mapping_with_samples(obtained_samples)

    def add_to_warehouse_message(self, message):
        pass
