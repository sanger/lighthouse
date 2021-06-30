from typing import List
from functools import cached_property
from .plate_barcode import PlateBarcode
from lighthouse.classes.event_properties.interfaces import EventPropertyAbstract
from lighthouse.classes.services.cherrytrack import CherrytrackServiceMixin
from lighthouse.classes.event_properties.exceptions import RetrievalError
import logging

logger = logging.getLogger(__name__)


class CherrytrackWellsFromDestination(EventPropertyAbstract, CherrytrackServiceMixin):
    def __init__(self, barcode_property: PlateBarcode):
        self.reset()
        self._barcode_property = barcode_property

    def is_valid(self):
        return self._barcode_property.is_valid() and (len(self._errors) == 0)

    def _is_valid_destination_coordinate_not_duplicated(self, wells):
        coordinates = [well["destination_coordinate"] for well in wells]
        duplicates = set([coor for coor in coordinates if coordinates.count(coor) > 1])
        if len(duplicates) > 0:
            raise RetrievalError(f"Some coordinates have clashing samples/controls: { duplicates }")

    @property
    def errors(self) -> List[str]:
        self.is_valid()
        return self._errors + self._barcode_property.errors

    @cached_property
    def value(self):
        with self.retrieval_scope():
            val = self.get_wells_from_destination_plate(self._barcode_property.value)
            self._is_valid_destination_coordinate_not_duplicated(val)
            return val

    def add_to_warehouse_message(self, message):
        pass
