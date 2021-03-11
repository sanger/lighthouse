class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class MultipleCentresError(Error):
    """Raised when a collection of samples have different centres."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "Different centres for these samples"

        if self.message:
            return f"MultipleCentresError: {self.message}"
        else:
            return f"MultipleCentresError: {default_message}"


class MissingCentreError(Error):
    """Raised when a sample is missing the name of the centre from which it came."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "No centre for this sample"

        if self.message:
            return f"MissingCentreError: {self.message}"
        else:
            return f"MissingCentreError: {default_message}"


class MissingSourceError(Error):
    """Raised when a sample is missing the source field."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "No centre for this sample"

        if self.message:
            return f"MissingSourceError: {self.message}"
        else:
            return f"MissingSourceError: {default_message}"


class DataError(Error):
    """Raised when a generic error occured with data."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "Error with data"

        if self.message:
            return f"DataError: {self.message}"
        else:
            return f"DataError: {default_message}"


class ReportCreationError(Error):
    """Raised when an error occurred while trying to generate the fit to pick samples report."""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        default_message = "Error while creating report"

        if self.message:
            return f"ReportCreationError: {self.message}"
        else:
            return f"ReportCreationError: {default_message}"


class UnmatchedSampleError(Error):
    pass
