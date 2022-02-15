import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.dart import DartServiceMixin
from lighthouse.constants.fields import (
    FIELD_DART_CONTROL,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_LAB_ID,
)
from lighthouse.helpers.responses import internal_server_error
from lighthouse.constants.error_messages import ERROR_SAMPLE_DATA_MISMATCH

logger = logging.getLogger(__name__)


class MatchingSampleNumbersCheck(EventPropertyAbstract):
    """
    Check for matching number of dart and mongo samples
    """

    def __init__(self, dart_samples: DartSamplesFromSource, mongo_samples: CherryPickedSamplesFromSource):
        self.reset()
        self._dart_samples = dart_samples
        self._mongo_samples = mongo_samples

    def is_valid(self):
        return self._dart_samples.is_valid() and self._mongo_samples.is_valid()
    
    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return list(set(self._errors + self._dart_samples.errors))

    @cached_property
    def value(self):
        with self.retrieval_scope():
            return self._join_rows_with_samples()

    def _equal_row_and_sample(self, row, sample):
        return (
            (sample[FIELD_ROOT_SAMPLE_ID] == getattr(row, FIELD_DART_ROOT_SAMPLE_ID))
            and (sample[FIELD_RNA_ID] == getattr(row, FIELD_DART_RNA_ID))
            and (sample[FIELD_LAB_ID] == getattr(row, FIELD_DART_LAB_ID))
            and sample[FIELD_RESULT].lower() == "positive"
        )

    def _find_sample_matching_row(self, row, samples):
        return next((sample for sample in samples if self._equal_row_and_sample(row, sample)), None)


    def _join_rows_with_samples(self):
        return [
            {"row": row_to_dict(row), 
                "sample": self._find_sample_matching_row(row, self._mongo_samples)}
            for row in self._rows_without_controls(self._dart_samples)
        ]

    def _rows_without_controls(rows):
        return list(filter(lambda x: self._row_is_normal_sample(x), rows))

    def _row_is_normal_sample(self, row):
        control_value = getattr(row, FIELD_DART_CONTROL)
        return control_value is None or control_value == "NULL" or control_value == ""

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
