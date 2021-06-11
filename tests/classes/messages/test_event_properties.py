from pytest import raises
from lighthouse.classes.messages.event_properties import UserID


def test_user_id_new(app):
    with raises(Exception):
        UserID(None)

    assert UserID({}) is not None
    assert UserID({'test': 'another test'}) is not None
    assert UserID({'user_id': '1234'}) is not None


def test_user_id_value(app):
    assert UserID({}).value is None
    assert UserID({'test': 'another test'}).value is None
    assert UserID({'user_id': '1234'}).value == '1234'



def test_user_id_valid(app):
    assert UserID({}).valid() is False
    assert UserID({'test': 'another test'}).valid() is False
    assert UserID({'user_id': '1234'}).valid() is True
