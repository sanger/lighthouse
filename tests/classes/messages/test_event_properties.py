from pytest import raises
from lighthouse.classes.messages.event_properties import (
    UserID,
    ValidationError,
    RobotSerialNumber,
    RobotUUID,
    RetrievalError,
    RunInfo,
    RunID,
)
import responses
from http import HTTPStatus


def test_user_id_new(app):
    with raises(Exception):
        UserID(None)

    assert UserID({}) is not None
    assert UserID({"test": "another test"}) is not None
    assert UserID({"user_id": "1234"}) is not None


def test_user_id_value(app):
    with raises(ValidationError):
        UserID({}).value
        UserID({"test": "another test"}).value

    assert UserID({"user_id": "1234"}).value == "1234"


def test_user_id_validate(app):
    assert UserID({}).validate() is False
    assert UserID({"test": "another test"}).validate() is False
    assert UserID({"user_id": "1234"}).validate() is True


def test_robot_serial_number_new(app):
    assert RobotSerialNumber({}) is not None
    assert RobotSerialNumber({"test": "a test"}) is not None
    assert RobotSerialNumber({"robot": "a test"}) is not None


def test_robot_serial_number_validate(app):
    assert RobotSerialNumber({}).validate() is False
    assert RobotSerialNumber({"test": "another test"}).validate() is False
    assert RobotSerialNumber({"robot": "1234"}).validate() is True


def test_robot_serial_number_value(app):
    with raises(ValidationError):
        RobotSerialNumber({}).value
        RobotSerialNumber({"test": "another test"}).value

    assert RobotSerialNumber({"robot": "1234"}).value == "1234"


def test_robot_uuid_new(app):
    assert RobotUUID(RobotSerialNumber({})) is not None
    assert RobotUUID(RobotSerialNumber({"test": "a test"})) is not None
    assert RobotUUID(RobotSerialNumber({"robot": "a test"})) is not None


def test_robot_uuid_validate(app):
    assert RobotUUID(RobotSerialNumber({})).validate() is False
    assert RobotUUID(RobotSerialNumber({"test": "another test"})).validate() is False
    assert RobotUUID(RobotSerialNumber({"robot": "1234"})).validate() is True


def test_robot_uuid_value(app):
    with app.app_context():
        with raises(ValidationError):
            RobotUUID(RobotSerialNumber({})).value
            RobotUUID(RobotSerialNumber({"test": "another test"})).value

        with raises(RetrievalError):
            RobotUUID(RobotSerialNumber({"robot": "1234"})).value

        uuid = app.config["BIOSERO_ROBOTS"]["BHRB0001"]["uuid"]
        assert RobotUUID(RobotSerialNumber({"robot": "BHRB0001"})).value == uuid


def test_run_id_valid(app):
    assert RunID({"automation_system_run_id": 1}).valid() is True


def test_run_id_value(app):
    assert RunID({"automation_system_run_id": 1}).value == 1


def test_run_info_valid(app):
    assert RunInfo(RunID({"automation_system_run_id": 1})).valid() is True


def test_run_info_value_successful(app, mocked_responses):
    with app.app_context():
        run_id = 2
        url = f"{app.config['CHERRY_TRACK_URL']}/automation-system-runs/{run_id}"

        expected_response = {
            "data": {"id": run_id, "user_id": "ab1", "liquid_handler_serial_number": "aLiquidHandlerSerialNumber"}
        }

        mocked_responses.add(
            responses.GET,
            url,
            json=expected_response,
            status=HTTPStatus.OK,
        )

        val = RunInfo(RunID({"automation_system_run_id": run_id})).value

        assert val == expected_response


def test_run_info_value_unsuccessful(app, mocked_responses):
    with app.app_context():
        run_id = 0
        url = f"{app.config['CHERRY_TRACK_URL']}/automation-system-runs/{run_id}"

        expected_response = None

        mocked_responses.add(
            responses.GET,
            url,
            json=expected_response,
            status=HTTPStatus.OK,
        )

        with raises(Exception):
            RunInfo(RunID({"automation_system_run_id": run_id})).value


# def test_picked_samples_from_source(app):
# assert PickedSamplesFromSource({"barcode_property": "1", "run_property": "1"}).valid() is False
# assert (
#     PickedSamplesFromSource({"barcode_property": "PlateBarcode", run_property: {run_id_property: "1"}}).valid is True
# )
