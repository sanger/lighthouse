import logging

from eve.io.mongo import Validator

from lighthouse.classes.beckman import Beckman
from lighthouse.classes.biosero import Biosero
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
        logger.debug("Running validation on input")
        if (event_type := self.document.get("event_type")) is not None:
            if event_type not in Biosero.PLATE_EVENT_NAMES:
                self._error(field, f"Unknown event type '{event_type}'")
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
                        f"'{event_type}' requires a corresponding 'run_id' parameter",
                    )
                    return

            if event_type == Biosero.EVENT_DESTINATION_FAILED:
                failure_type = self.document.get("failure_type")
                if failure_type is None:
                    self._error(
                        field,
                        f"'failure_type' required with '{Biosero.EVENT_DESTINATION_FAILED}' event",
                    )
                    return
                if failure_type not in [failure_type.get("type") for failure_type in Beckman.get_failure_types()]:
                    self._error(
                        field,
                        f"Unknown failure type '{failure_type}'",
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
