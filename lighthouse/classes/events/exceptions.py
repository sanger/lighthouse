class PlateEventException(Exception):
    pass


class EventNotInitializedError(PlateEventException):
    def __init__(self, message: str):
        self.message = message
