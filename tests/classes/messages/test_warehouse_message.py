import pytest
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage  # type: ignore
from lighthouse.messages.message import Message
from unittest.mock import patch


def test_can_set_user_id():
    message = WarehouseMessage("mytype", "myuuid", "at some point")
    message.set_user_id("user 1")

    assert message._user_id == "user 1"


def test_add_subject():
    message = WarehouseMessage("mytype", "myuuid", "at some point")
    message.add_subject("myrole", "mysubject", "myname", "myuuid")

    assert message._subjects == [
        {
            "role_type": "myrole",
            "subject_type": "mysubject",
            "friendly_name": "myname",
            "uuid": "myuuid",
        }
    ]
    with patch("lighthouse.classes.messages.warehouse_messages.uuid4", return_value="avalue"):
        message.add_subject("myrole", "mysubject", "myname", None)

    assert message._subjects == [
        {
            "role_type": "myrole",
            "subject_type": "mysubject",
            "friendly_name": "myname",
            "uuid": "myuuid",
        },
        {
            "role_type": "myrole",
            "subject_type": "mysubject",
            "friendly_name": "myname",
            "uuid": "avalue",
        },
    ]


def test_construct_event_message(app):
    with app.app_context():
        message = WarehouseMessage("mytype", "myuuid", "at some point")

        with pytest.raises(Exception):
            message.construct_event_message("myuuid", "some date", [])

        message.set_user_id("my user")
        msg = message.construct_event_message("myuuid", "some date", [])

        assert msg == {
            "event": {
                "uuid": "myuuid",
                "event_type": "mytype",
                "occured_at": "some date",
                "user_identifier": "my user",
                "subjects": [],
                "metadata": {},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }


def test_add_sample_as_subject(samples):
    message = WarehouseMessage("mytype", "myuuid", "at some point")

    message.add_sample_as_subject(samples[0][0])
    assert message._subjects == [
        {
            "friendly_name": "sample_001__rna_1__lab_1__Positive",
            "role_type": "sample",
            "subject_type": "sample",
            "uuid": "0a53e7b6-7ce8-4ebc-95c3-02dd64942531",
        }
    ]


def test_render(app):
    with app.app_context():
        message = WarehouseMessage("mytype", "myuuid", "at some point")
        with pytest.raises(Exception):
            message.render()

        message.set_user_id("my user")

        assert isinstance(message.render(), Message)
