from pytest import raises
from lighthouse.classes.messages.event_properties import (
    UserID, ValidationError, RobotSerialNumber, RobotUUID, RetrievalError)


def test_user_id_new(app):
    with raises(Exception):
        UserID(None)

    assert UserID({}) is not None
    assert UserID({'test': 'another test'}) is not None
    assert UserID({'user_id': '1234'}) is not None


def test_user_id_value(app):
    with raises(ValidationError):
        UserID({}).value
        UserID({'test': 'another test'}).value

    assert UserID({'user_id': '1234'}).value == '1234'


def test_user_id_validate(app):
    assert UserID({}).validate() is False
    assert UserID({'test': 'another test'}).validate() is False
    assert UserID({'user_id': '1234'}).validate() is True


def test_robot_serial_number_new(app):
    assert RobotSerialNumber({}) is not None
    assert RobotSerialNumber({'test': 'a test'}) is not None
    assert RobotSerialNumber({'robot': 'a test'}) is not None


def test_robot_serial_number_validate(app):
    assert RobotSerialNumber({}).validate() is False
    assert RobotSerialNumber({'test': 'another test'}).validate() is False
    assert RobotSerialNumber({'robot': '1234'}).validate() is True


def test_robot_serial_number_value(app):
    with raises(ValidationError):
        RobotSerialNumber({}).value
        RobotSerialNumber({'test': 'another test'}).value

    assert RobotSerialNumber({'robot': '1234'}).value == '1234'


def test_robot_uuid_new(app):
    assert RobotUUID(RobotSerialNumber({})) is not None
    assert RobotUUID(RobotSerialNumber({'test': 'a test'})) is not None
    assert RobotUUID(RobotSerialNumber({'robot': 'a test'})) is not None


def test_robot_uuid_validate(app):
    assert RobotUUID(RobotSerialNumber({})).validate() is False
    assert RobotUUID(RobotSerialNumber({'test': 'another test'})).validate() is False
    assert RobotUUID(RobotSerialNumber({'robot': '1234'})).validate() is True


def test_robot_uuid_value(app):
    with app.app_context():
        with raises(ValidationError):
            RobotUUID(RobotSerialNumber({})).value
            RobotUUID(RobotSerialNumber({'test': 'another test'})).value

        with raises(RetrievalError):
            RobotUUID(RobotSerialNumber({'robot': '1234'})).value

        uuid = app.config['BIOSERO_ROBOTS']['BHRB0001']['uuid']
        assert RobotUUID(RobotSerialNumber({'robot': 'BHRB0001'})).value == uuid
