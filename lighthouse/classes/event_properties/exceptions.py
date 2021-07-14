class EventPropertyError(Exception):
    pass


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message


class RetrievalError(Exception):
    def __init__(self, message: str):
        self.message = message
