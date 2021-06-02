from eve.io.mongo import Validator

from lighthouse.constants.events import (
    PE_BIOSERO_DESTINATION_CREATED,
    PE_BIOSERO_DESTINATION_FAILED,
    PE_BIOSERO_SOURCE_ALL_NEGATIVES,
    PE_BIOSERO_SOURCE_COMPLETED,
    PE_BIOSERO_SOURCE_NO_MAP_DATA,
    PE_BIOSERO_SOURCE_NOT_RECOGNISED,
)

ALLOWABLE_EVENTS = (
    PE_BIOSERO_DESTINATION_CREATED,
    PE_BIOSERO_DESTINATION_FAILED,
    PE_BIOSERO_SOURCE_ALL_NEGATIVES,
    PE_BIOSERO_SOURCE_COMPLETED,
    PE_BIOSERO_SOURCE_NO_MAP_DATA,
    PE_BIOSERO_SOURCE_NOT_RECOGNISED,
)


class LighthouseValidator(Validator):
    def _check_with_priority_samples_required_bools(self, field, _):
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
        if (event_type := self.document.get("event_type")) is not None:
            if event_type not in ALLOWABLE_EVENTS:
                self._error(field, f"unallowed event type '{event_type}'")
                return

            if event_type == PE_BIOSERO_SOURCE_NOT_RECOGNISED and self.document.get("barcode") is not None:
                self._error(
                    field, f"Document cannot contain a barcode with the '{PE_BIOSERO_SOURCE_NOT_RECOGNISED}' event"
                )
                return

            if event_type != PE_BIOSERO_SOURCE_NOT_RECOGNISED and self.document.get("barcode") is None:
                self._error(field, f"'barcode' cannot be empty with the '{event_type}' event")
                return
