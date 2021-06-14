from lighthouse.messages.message import Message
from lighthouse.types import Subject, EventMessage
from uuid import uuid4
from typing import List, Optional
from flask import current_app as app
from datetime import datetime


class WarehouseMessage:
    def __init__(self, event_type):
        self._name = event_type
        self._subjects = []

    def set_user_id(self, user_id):
        self._user_id = user_id

    def render(self):
        message_content = self.construct_event_message(subjects=self._subjects)

        return Message(message_content)

    def add_subject(self, role_type: str, subject_type: str, friendly_name: str, uuid: Optional[str] = None) -> Subject:
        if uuid is None:
            uuid = str(uuid4())

        self._subjects.append(
            {
                "role_type": role_type,
                "subject_type": subject_type,
                "friendly_name": friendly_name,
                "uuid": uuid,
            }
        )

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

    def get_message_timestamp(self) -> str:
        """Returns the current datetime in a format compatible with messaging.

        Returns:
            {str} -- The current datetime.
        """
        return datetime.now().isoformat(timespec="seconds")
