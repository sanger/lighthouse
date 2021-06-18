class SimpleEventPropertyMixin:
    """Set of tools to perform validation on simple event properties.
    """
    def validate_param_not_missing(self, param: str) -> None:

        with self.validation_scope():
            self.process_validation(
                self._params.get(param) is not None,
                f"'{ param }' is missing"
            )

    def validate_param_not_empty(self, param: str) -> None:
        with self.validation_scope():
            self.process_validation(
                self._params.get(param) != "",
                f"'{ param }' should not be an empty string"
            )

    def validate_param_no_whitespaces(self, param: str) -> None:
        with self.validation_scope():
            self.process_validation(
                ' ' not in self._params.get(param),
                f"'{ param }' should not contain any whitespaces"
            )

    def validate_param_is_integer(self, param: str) -> None:
        with self.validation_scope():
            self.process_validation(
                self._is_integer(self._params.get(param)),
                f"'{ param }' should be an integer"
            )

    def is_integer(self, n: str) -> bool:
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

