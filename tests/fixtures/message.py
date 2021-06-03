import pytest

from lighthouse.constants.events import PE_BECKMAN_SOURCE_ALL_NEGATIVES, PE_BECKMAN_SOURCE_COMPLETED
from lighthouse.messages.message import Message
from lighthouse.types import EventMessage


@pytest.fixture
def message_unknown():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": "no_callbacks",
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)


@pytest.fixture
def message_source_complete():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": PE_BECKMAN_SOURCE_COMPLETED,
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [
                {
                    "role_type": "sample",
                    "subject_type": "sample",
                    "friendly_name": "friendly_name",
                    "uuid": "00000000-1111-2222-3333-555555555555",
                },
                {
                    "role_type": "cherrypicking_source_labware",
                    "subject_type": "plate",
                    "friendly_name": "plate-barcode",
                    "uuid": "00000000-1111-2222-3333-555555555556",
                },
                {
                    "role_type": "robot",
                    "subject_type": "robot",
                    "friendly_name": "robot-serial",
                    "uuid": "00000000-1111-2222-3333-555555555557",
                },
            ],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)


@pytest.fixture
def message_source_all_negative():
    message_content: EventMessage = {
        "event": {
            "uuid": "1770dbcd-0abf-4293-ac62-dd26964f80b0",
            "event_type": PE_BECKMAN_SOURCE_ALL_NEGATIVES,
            "occured_at": "2020-11-26T15:58:20",
            "user_identifier": "test1",
            "subjects": [
                {
                    "role_type": "cherrypicking_source_labware",
                    "subject_type": "plate",
                    "friendly_name": "plate-barcode",
                    "uuid": "00000000-1111-2222-3333-555555555556",
                },
                {
                    "role_type": "robot",
                    "subject_type": "robot",
                    "friendly_name": "robot-serial",
                    "uuid": "00000000-1111-2222-3333-555555555557",
                },
            ],
            "metadata": {},
        },
        "lims": "LH_TEST",
    }
    return Message(message_content)
