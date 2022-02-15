import logging
from functools import cached_property
from typing import List

from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.messages import SequencescapeMessage, WarehouseMessage
from lighthouse.classes.services.dart import DartServiceMixin
from lighthouse.constants.fields import FIELD_DART_CONTROL
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
            if not self._check_matching_sample_numbers(self._dart_samples, self._mongo_samples):
                return internal_server_error(f"{ERROR_SAMPLE_DATA_MISMATCH}")
            return True

    def _check_matching_sample_numbers(self, rows, samples):
        return len(samples) == len(self._rows_without_controls(rows))

    def _rows_without_controls(rows):
        return list(filter(lambda x: self._row_is_normal_sample(x), rows))

    def _row_is_normal_sample(self, row):
        control_value = getattr(row, FIELD_DART_CONTROL)
        return control_value is None or control_value == "NULL" or control_value == ""

    def add_to_warehouse_message(self, message: WarehouseMessage):
        pass

    def add_to_sequencescape_message(self, message: SequencescapeMessage):
        pass
