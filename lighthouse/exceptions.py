class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class MultipleCentresError(Error):
    """Raised when a collection of samples have different centres."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = f"MultipleCentresError: Different centres for these samples"

        if self.message:
            return f"{default_message}: {self.message}"
        else:
            return default_message


class MissingCentreError(Error):
    """Raised when a sample is missing the name of the centre from which it came."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = f"MissingCentreError: No centre for this sample"

        if self.message:
            return f"{default_message}: {self.message}"
        else:
            return default_message


class MissingSourceError(Error):
    """Raised when a a sample is missing the source field."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = f"MissingSourceError: No source field for this sample"

        if self.message:
            return f"{default_message}: {self.message}"
        else:
            return default_message
