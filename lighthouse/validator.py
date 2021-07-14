import logging

from eve.io.mongo import Validator

from lighthouse.classes.biosero import Biosero
from lighthouse.constants.error_messages import (
    ERROR_PLATE_SPECS_EMPTY_LIST,
    ERROR_PLATE_SPECS_INVALID_FORMAT,
)
from lighthouse.constants.fields import FIELD_EVENT_RUN_ID

logger = logging.getLogger(__name__)


class LighthouseValidator(Validator):
    def _check_with_priority_samples_required_bools(self, field, _):
        logger.debug("Running validation on input")
        if "must_sequence" not in self.document and "preferentially_sequence" not in self.document:
            self._error(field, "Document must be provided with 'must_sequence' or 'preferentially_sequence'")
            return

        # do not allow both to be True; both can be False though, if they want to "cancel" a priority sample
        if (
            (must_sequence := self.document.get("must_sequence")) is not None
            and isinstance(must_sequence, bool)
            and must_sequence
        ) and (
            (preferentially_sequence := self.document.get("preferentially_sequence")) is not None
            and isinstance(preferentially_sequence, bool)
            and preferentially_sequence
        ):
            self._error(field, "Document cannot contain both 'must_sequence' and 'preferentially_sequence' as true")

    def _check_with_plate_events_dependent_parameters(self, field, _):
        """
        - if the event type is PE_BIOSERO_SOURCE_NOT_RECOGNISED and a barcode is present, there must be an error
            in the client - we are not expecting a barcode with that event
        - if the event type is not PE_BIOSERO_SOURCE_NOT_RECOGNISED, a barcode is required
        """
        logger.debug("Running validation on input")
        if (event_type := self.document.get("event_type")) is not None:
            if event_type not in Biosero.PLATE_EVENT_NAMES:
                self._error(field, f"unallowed event type '{event_type}'")
                return

            events_that_create_a_plate = [
                Biosero.EVENT_DESTINATION_PARTIAL_COMPLETED,
                Biosero.EVENT_DESTINATION_COMPLETED,
                Biosero.EVENT_DESTINATION_FAILED,
            ]
            if event_type not in events_that_create_a_plate:
                if self.document.get(FIELD_EVENT_RUN_ID) is None:
                    self._error(
                        field,
                        f"Document cannot contain an event without run id with the '{event_type}' event",
                    )
                    return

            if event_type == Biosero.EVENT_SOURCE_UNRECOGNISED and self.document.get("barcode") is not None:
                self._error(
                    field,
                    f"Document cannot contain a barcode with the '{Biosero.EVENT_SOURCE_UNRECOGNISED}' event",
                )
                return

            if event_type != Biosero.EVENT_SOURCE_UNRECOGNISED and self.document.get("barcode") is None:
                self._error(field, f"'barcode' cannot be empty with the '{event_type}' event")
                return

    def _check_with_validate_cptd_plate_specs(self, field, _):
        """Check that the plate specs appear to be of the correct format.

        i.e. a List[List[int]] where each inner list contains exactly two values.
        e.g. [[2, 0], [4, 48], [1, 0], [5, 96]] would be valid
        """
        logger.debug(f"Running validation on '{field}' field")

        plate_specs = self.document.get(field)
        logger.debug(f"Value of field is {plate_specs}")

        # This validation gets called before Eve identifies the None value as invalid.
        # There's no need to add any errors because Eve will do it for us.
        if plate_specs is None:
            return

        # We can assume we have a list already because of the Eve imposed type checking
        if len(plate_specs) == 0:
            self._error(field, ERROR_PLATE_SPECS_EMPTY_LIST)

        if not all([type(ps) == list and len(ps) == 2 for ps in plate_specs]) or not all(
            [type(s) == int for ps in plate_specs for s in ps]
        ):
            self._error(field, ERROR_PLATE_SPECS_INVALID_FORMAT)
