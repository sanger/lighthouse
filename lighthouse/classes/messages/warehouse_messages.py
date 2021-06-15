from lighthouse.messages.message import Message
from lighthouse.types import Subject, EventMessage
from uuid import uuid4
from typing import List, Optional, Any
from flask import current_app as app
from datetime import datetime
from lighthouse.constants.fields import (
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
)
from lighthouse.types import SampleDoc
from lighthouse.classes.plate_event import PlateEvent, ROLE_TYPE_SAMPLE, SUBJECT_TYPE_SAMPLE


class WarehouseMessage:
    def __init__(self, event_type):
        self._name = event_type
        self._subjects = []

    def set_user_id(self, user_id):
        self._user_id = user_id

    def render(self, event: PlateEvent):
        message_content = self.construct_event_message(
            event_uuid=event.get_event_uuid(),
            occured_at=event.get_message_timestamp(),
            subjects=self._subjects,
        )

        return Message(message_content)

    def add_subject(
        self, role_type: str, subject_type: str, friendly_name: str, uuid: Optional[str] = None
    ) -> List[Any]:
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
        return self._subjects

    def construct_event_message(self, event_uuid: str, occured_at: str, subjects: List[Subject]) -> EventMessage:
        return {
            "event": {
                "uuid": event_uuid,
                "event_type": self._name,
                "occured_at": occured_at,
                "user_identifier": self._user_id,
                "subjects": subjects,
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }

    def add_sample_as_subject(self, sample: SampleDoc) -> Any:
        """Adds sample subject for a plate event message from a mongo sample.

        Arguments:
            samples {SampleDoc} -- The mongo sample for which to generate a subject.

        """
        friendly_name = "__".join(
            [
                sample[FIELD_ROOT_SAMPLE_ID],
                sample[FIELD_RNA_ID],
                sample[FIELD_LAB_ID],
                sample[FIELD_RESULT],
            ]
        )
        return self.add_subject(
            role_type=ROLE_TYPE_SAMPLE,
            subject_type=SUBJECT_TYPE_SAMPLE,
            friendly_name=friendly_name,
            uuid=sample[FIELD_LH_SAMPLE_UUID],
        )

