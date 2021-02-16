from eve.io.mongo import Validator


class PrioritySamplesValidator(Validator):
    def _check_with_required_bools(self, field, _):
        if "must_sequence" not in self.document and "preferentially_sequence" not in self.document:
            self._error(field, "Document must be provided with 'must_sequence' or 'preferentially_sequence'")

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
