from lighthouse.messages.message import Message
from lighthouse.types import Subject, EventMessage
from uuid import uuid4
from typing import List, Optional, Any
from flask import current_app as app
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_ROOT_SAMPLE_ID,
    FIELD_CHERRYTRACK_RNA_ID,
    FIELD_CHERRYTRACK_LAB_ID,
    FIELD_CHERRYTRACK_RESULT,
    FIELD_CHERRYTRACK_LH_SAMPLE_UUID,
)
from lighthouse.types import SampleDoc

###
# subjects and roles for the message to the events warehouse
###
ROLE_TYPE_ROBOT = "robot"
ROLE_TYPE_SAMPLE = "sample"
ROLE_TYPE_CP_SOURCE_LABWARE = "cherrypicking_source_labware"
SUBJECT_TYPE_SAMPLE = ROLE_TYPE_SAMPLE
SUBJECT_TYPE_ROBOT = ROLE_TYPE_ROBOT
SUBJECT_TYPE_PLATE = "plate"


class WarehouseMessage:
    def __init__(self, event_type, event_uuid, occured_at):
        self._name = event_type
        self._event_uuid = event_uuid
        self._occured_at = occured_at
        self._subjects = []

    def set_user_id(self, user_id: str) -> None:
        self._user_id = user_id

    def render(self) -> Message:
        message_content = self.construct_event_message(
            event_uuid=self._event_uuid,
            occured_at=self._occured_at,
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
                sample[FIELD_CHERRYTRACK_ROOT_SAMPLE_ID],
                sample[FIELD_CHERRYTRACK_RNA_ID],
                sample[FIELD_CHERRYTRACK_LAB_ID],
                sample[FIELD_CHERRYTRACK_RESULT],
            ]
        )
        return self.add_subject(
            role_type=ROLE_TYPE_SAMPLE,
            subject_type=SUBJECT_TYPE_SAMPLE,
            friendly_name=friendly_name,
            uuid=sample[FIELD_CHERRYTRACK_LH_SAMPLE_UUID],
        )
