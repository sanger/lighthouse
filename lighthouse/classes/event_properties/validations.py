class SimpleEventPropertyMixin:
    """Set of tools to perform validation on simple event properties.
    """
    def validate_param_not_missing(self, param: str) -> None:
        """
        Validates that the params dictionary contains a value for the
        key provided as argument

        Arguments
            param: str - Key to check in the params dictionary

        Returns
            bool - True/False indicating if this condition is met
        """
        with self.validation_scope():
            self.process_validation(
                self._params.get(param) is not None,
                f"'{ param }' is missing"
            )

    def validate_param_not_empty(self, param: str) -> None:
        """
        Validates that the params dictionary contains a value for the
        key provided as argument that is not an empty string ('')

        Arguments
            param: str - Key to check in the params dictionary

        Returns
            bool - True/False indicating if this condition is met
        """
        with self.validation_scope():
            self.process_validation(
                self._params.get(param) != "",
                f"'{ param }' should not be an empty string"
            )

    def validate_param_no_whitespaces(self, param: str) -> None:
        """
        Validates that the params dictionary contains a value for the
        key provided as argument that does not contain any whitespaces.

        Arguments
            param: str - Key to check in the params dictionary

        Returns
            bool - True/False indicating if this condition is met
        """
        with self.validation_scope():
            self.process_validation(
                ' ' not in self._params.get(param),
                f"'{ param }' should not contain any whitespaces"
            )

    def validate_param_is_integer(self, param: str) -> None:
        """
        Validates that the params dictionary contains a value for the
        key provided as argument that it represents an integer.
        This string can contain the sign of integer (+ for positive, - for negative)
        and could include whitespaces.
        This condition is check by the method is_integer().

        Arguments
            param: str - Key to check in the params dictionary

        Returns
            bool - True/False indicating if this condition is met
        """
        with self.validation_scope():
            self.process_validation(
                self.is_integer(self._params.get(param)),
                f"'{ param }' should be an integer"
            )

    def is_integer(self, n: str) -> bool:
        """
        Function that returns if the string provided can represent an integer.
        This string can contain the sign of integer (+ for positive, - for negative)
        and could include whitespaces.

        Arguments
            param: str - value to check if it represents an integer string.

        Returns
            bool - True/False indicating if this condition is met
        """
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

