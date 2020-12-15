from lighthouse.messages.message import Message


def test_messages_none_message():
    message = Message(None)
    assert message.payload() == "null"


def test_messages_string_message():
    message = Message("test message")
    assert message.payload() == '"test message"'


def test_messages_number_message():
    message = Message(14)
    assert message.payload() == "14"


def test_messages_dict_message():
    message = Message({"test key": "test value"})
    assert message.payload() == '{"test key": "test value"}'


def test_messages_array_message():
    message = Message([53, "value", {"test key": "test value"}])
    assert message.payload() == '[53, "value", {"test key": "test value"}]'
