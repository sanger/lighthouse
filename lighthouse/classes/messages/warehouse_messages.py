from lighthouse.messages.message import Message
from lighthouse.types import Subject, EventMessage
from uuid import uuid4
from typing import List, Optional, Any, Dict
from flask import current_app as app
from lighthouse.constants.fields import (
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
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
ROLE_TYPE_RUN = "run"
SUBJECT_TYPE_RUN = "run"


class WarehouseMessage:
    def __init__(self, event_type, event_uuid, occured_at):
        self._event_type = event_type
        self._event_uuid = event_uuid
        self._occured_at = occured_at
        self._subjects = []
        self._metadata = {}
        self._user_id = None

    def set_user_id(self, user_id: str) -> None:
        self._user_id = user_id

    def render(self) -> Message:
        message_content = self.construct_event_message(
            event_uuid=self._event_uuid,
            occured_at=self._occured_at,
            subjects=self._subjects,
            metadata=self._metadata,
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

    def construct_event_message(
        self, event_uuid: str, occured_at: str, subjects: List[Subject],
        metadata: Dict[str, str]
    ) -> EventMessage:
        if self._user_id is None:
            raise Exception("User id needs to be defined to generate a new event message")

        return {
            "event": {
                "uuid": event_uuid,
                "event_type": self._event_type,
                "occured_at": occured_at,
                "user_identifier": self._user_id,
                "subjects": subjects,
                "metadata": metadata,
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

    def add_metadata(self, name, value):
        self._metadata[name] = value
