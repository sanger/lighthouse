import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.constants.fields import (
    FIELD_COG_BARCODE,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SS_NAME,
    FIELD_SS_PHENOTYPE,
    FIELD_SS_SAMPLE_DESCRIPTION,
    FIELD_SS_SUPPLIER_NAME,
    FIELD_SS_UUID,
)
from lighthouse.helpers.plates import add_cog_barcodes_from_different_centres, update_mlwh_with_cog_uk_ids

from .samples_from_destination import SamplesFromDestination

logger = logging.getLogger(__name__)


class SamplesWithCogUkId(EventPropertyAbstract):
    def __init__(self, samples_from_destination: SamplesFromDestination):
        self.reset()
        self._samples_from_destination = samples_from_destination

    def is_valid(self):
        return self._samples_from_destination.is_valid() and (len(self._errors) == 0)

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._samples_from_destination.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            samples = list(self._samples_from_destination.value.values())
            updated_samples = add_cog_barcodes_from_different_centres(samples)
            update_mlwh_with_cog_uk_ids(updated_samples)
            return self._samples_from_destination.value

    def add_to_warehouse_message(self, message: WarehouseMessage):
        for sample in self.value.values():
            message.add_sample_as_subject(sample)

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        for coordinate in self.value:
            sample = self.value[coordinate]
            message.set_well_sample(
                coordinate,
                {
                    FIELD_SS_NAME: sample[FIELD_RNA_ID],
                    FIELD_SS_SAMPLE_DESCRIPTION: sample[FIELD_ROOT_SAMPLE_ID],
                    FIELD_SS_SUPPLIER_NAME: sample[FIELD_COG_BARCODE],
                    FIELD_SS_PHENOTYPE: sample[FIELD_RESULT].lower(),
                    FIELD_SS_UUID: sample[FIELD_LH_SAMPLE_UUID],
                },
            )
