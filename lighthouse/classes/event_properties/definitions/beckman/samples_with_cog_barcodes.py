import logging
from functools import cached_property
from typing import List, Dict

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage

logger = logging.getLogger(__name__)


class SamplesWithCOGBarcodes(EventPropertyAbstract, BaracodaServiceMixin, MongoServiceMixin):
    """
    Classify samples from mongo based on the centre
    """

    def __init__(self, classified_samples: ClassifiedSamplesByCentre):
        self.reset()
        self._classified_samples = classified_samples

    def is_valid(self):
        return self._classified_samples.is_valid()

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._classified_samples.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._add_cog_barcodes_from_different_centres()

    def _add_cog_barcodes_from_different_centres(self) -> List[str]:
        for centre_name in self._classified_samples:
            self.add_cog_barcodes(self._classified_samples[centre_name])

        return list(self._classified_samples.keys())

    def _add_cog_barcodes(self, samples):
        centre_name = _confirm_centre(samples)
        centre_prefix = self.get_centre_prefix(centre_name)
        num_samples = len(samples)
        #call baracoda to get barcodes
        barcodes = self.get_barcodes_for_samples(num_samples, centre_prefix)

        for (sample, barcode) in zip(samples, barcodes):
            sample[FIELD_COG_BARCODE] = barcode

    def _confirm_centre(self, samples: List[Dict[str, str]]) -> str:
        """Confirm that the centre for all the samples is populated and the same 
        and return the name of the centre of these samples
        """
        try:
            # check that the 'source' field has a valid name
            for sample in samples:
                if not sample[FIELD_SOURCE]:
                    raise MissingCentreError(sample)

            # create a set from the 'source' field to check we only have 1 unique centre
            # for these samples
            centre_set = {sample[FIELD_SOURCE] for sample in samples}
        except KeyError:
            raise MissingSourceError()
        else:
            if len(centre_set) > 1:
                raise MultipleCentresError()

        return centre_set.pop()

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass

    