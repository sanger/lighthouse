from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from flask import current_app as app

from lighthouse.constants.fields import (
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
)
from lighthouse.messages.message import Message
from lighthouse.types import EventMessage, SampleDoc, Subject


class PlateEvent(ABC):
    ###
    # subjects and roles for the message to the events warehouse
    ###
    ROLE_TYPE_ROBOT = "robot"
    ROLE_TYPE_SAMPLE = "sample"
    ROLE_TYPE_CP_SOURCE_LABWARE = "cherrypicking_source_labware"
    SUBJECT_TYPE_SAMPLE = ROLE_TYPE_SAMPLE
    SUBJECT_TYPE_ROBOT = ROLE_TYPE_ROBOT
    SUBJECT_TYPE_PLATE = "plate"

    class PlateTypeEnum(Enum):
        SOURCE = auto()
        DESTINATION = auto()

    @property
    def name(self) -> str:
        return self._name

    @property
    def plate_barcode(self) -> str:
        return self._plate_barcode

    def __init__(self, name: str, plate_type: PlateTypeEnum) -> None:
        self._name = name
        self._plate_type = plate_type
        self._plate_barcode = ""

    @abstractmethod
    def initialize_event(self, params: Dict[str, Union[str, Any]]) -> None:
        ...

    @abstractmethod
    def _create_message(self) -> Message:
        ...

    @abstractmethod
    def _send_warehouse_message(self, message: Message) -> None:
        ...

    @abstractmethod
    def process_event(self) -> None:
        message = self._create_message()
        self._send_warehouse_message(message=message)

    def construct_event_message(self, user_identifier: str, subjects: List[Subject]) -> EventMessage:
        return {
            "event": {
                "uuid": str(uuid4()),
                "event_type": self._name,
                "occured_at": self.get_message_timestamp(),
                "user_identifier": user_identifier,
                "subjects": subjects,
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }

    def construct_mongo_sample_message_subject(self, sample: SampleDoc) -> Subject:
        """Generates sample subject for a plate event message from a mongo sample.

        Arguments:
            samples {SampleDoc} -- The mongo sample for which to generate a subject.

        Returns:
            {Dict[str, str]} -- The plate message sample subject.
        """
        friendly_name = "__".join(
            [
                sample[FIELD_ROOT_SAMPLE_ID],
                sample[FIELD_RNA_ID],
                sample[FIELD_LAB_ID],
                sample[FIELD_RESULT],
            ]
        )
        return self.construct_message_subject(
            role_type=self.ROLE_TYPE_SAMPLE,
            subject_type=self.SUBJECT_TYPE_SAMPLE,
            friendly_name=friendly_name,
            uuid=sample[FIELD_LH_SAMPLE_UUID],
        )

    def _get_routing_key(self) -> str:
        """Determines the routing key for a plate event message.

        Arguments:
            event_type {str} -- The event type for which to determine the routing key.

        Returns:
            {str} -- The message routing key.
        """

        return str(app.config["RMQ_ROUTING_KEY"].replace("#", self._name))

    @staticmethod
    def construct_message_subject(
        role_type: str, subject_type: str, friendly_name: str, uuid: Optional[str] = None
    ) -> Subject:
        if uuid is None:
            uuid = str(uuid4())

        return {
            "role_type": role_type,
            "subject_type": subject_type,
            "friendly_name": friendly_name,
            "uuid": uuid,
        }

    @staticmethod
    def get_message_timestamp() -> str:
        """Returns the current datetime in a format compatible with messaging.

        Returns:
            {str} -- The current datetime.
        """
        return datetime.now().isoformat(timespec="seconds")
