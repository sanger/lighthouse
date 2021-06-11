from lighthouse.messages.message import Message
from typing import List
from lighthouse.types import Subject, EventMessage


class WarehouseMessage(Message):
    def __init__(self, event_type):
        self._name = event_type
        self._subjects = []

    def add_subject(self, subject):
        self._subjects.push(subject)

    def set_user_id(self, user_id):
        self._user_id = user_id

    def render(self):
        message_content = self.construct_event_message(subjects=self._subjects)

        return Message(message_content)

    def construct_event_message(self, subjects: List[Subject]) -> EventMessage:
        return {
            "event": {
                "uuid": str(uuid4()),
                "event_type": self._name,
                "occured_at": self.get_message_timestamp(),
                "user_identifier": self._user_id,
                "subjects": subjects,
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }


