from pytest import raises
import pytest
from lighthouse.classes.event_properties.interfaces import ValidationError, RetrievalError  # type: ignore
from lighthouse.classes.event_properties.definitions import (  # type: ignore
    UserID,
    RobotSerialNumber,
    RobotUUID,
    RunInfo,
    RunID,
    PlateBarcode,
    PickedSamplesFromSource,
)
from lighthouse.constants.fields import FIELD_EVENT_RUN_ID, FIELD_EVENT_ROBOT, FIELD_EVENT_USER_ID, FIELD_EVENT_BARCODE
from http import HTTPStatus

SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS = [
    [RunID, FIELD_EVENT_RUN_ID, ["1234"], [None, "12 34", "12.34"]],
    [PlateBarcode, FIELD_EVENT_BARCODE, ["AA1234"], [None, "AA 1234", ""]],
    [UserID, FIELD_EVENT_USER_ID, ["user1", "user 1"], [None, ""]],
    [RobotSerialNumber, FIELD_EVENT_ROBOT, ["1234"], ["12 34", None, ""]],
]


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_new_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params
    with raises(ValidationError):
        klass(None)

    for invalid in invalid_list:
        assert klass({field: invalid}) is not None

    for valid in valid_list:
        assert klass({field: valid}) is not None


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_value_for_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params

    for invalid in invalid_list:
        with raises(ValidationError):
            klass({field: invalid}).value

    for valid in valid_list:
        assert klass({field: valid}).value == valid


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_validate_for_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params

    for invalid in invalid_list:
        assert klass({field: invalid}).validate() is False

    for valid in valid_list:
        assert klass({field: valid}).validate() is True


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_errors_for_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params

    for invalid in invalid_list:
        assert len(klass({field: invalid}).errors) > 0

    for valid in valid_list:
        assert len(klass({field: valid}).errors) == 0


def test_robot_uuid_new(app):
    assert RobotUUID(RobotSerialNumber({})) is not None
    assert RobotUUID(RobotSerialNumber({"test": "a test"})) is not None
    assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "a test"})) is not None


def test_robot_uuid_validate(app):
    assert RobotUUID(RobotSerialNumber({})).validate() is False
    assert RobotUUID(RobotSerialNumber({"test": "another test"})).validate() is False
    assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"})).validate() is True


def test_robot_uuid_value(app):
    with app.app_context():
        with raises(ValidationError):
            RobotUUID(RobotSerialNumber({})).value
            RobotUUID(RobotSerialNumber({"test": "another test"})).value

        with raises(RetrievalError):
            RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"})).value

        uuid = app.config["BIOSERO_ROBOTS"]["BHRB0001"]["uuid"]
        assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "BHRB0001"})).value == uuid


def test_robot_uuid_errors(app):
    with app.app_context():
        # After success
        robot = RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "BHRB0001"}))
        robot.value
        assert len(robot.errors) == 0

        # After validate false
        robot = RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "12 34"}))
        robot.validate()
        assert len(robot.errors) > 0

        # After retrieval error
        robot = RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"}))
        with raises(RetrievalError):
            robot.value

        assert len(robot.errors) > 0


def test_run_info_valid(app):
    assert RunInfo(RunID({FIELD_EVENT_RUN_ID: 1})).valid() is True


@pytest.mark.parametrize("run_id", [5])
def test_run_info_value_successful(app, run_id, mocked_responses, cherrytrack_mock_run_info):
    with app.app_context():

        expected_response = {
            "data": {
                "id": run_id,
                FIELD_EVENT_USER_ID: "ab1",
                "liquid_handler_serial_number": "aLiquidHandlerSerialNumber",
            }
        }

        val = RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id})).value

        assert val == expected_response["data"]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize(
    "cherrytrack_run_info_response",
    [{"data": {"errors": ["Failed to get automation system run info for the given run id"]}}],
)
@pytest.mark.parametrize("cherrytrack_mock_run_info_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_run_info_value_unsuccessful(app, mocked_responses, cherrytrack_mock_run_info):
    with app.app_context():
        myExc = None
        run_info = RunInfo(RunID({FIELD_EVENT_RUN_ID: 5}))
        try:
            run_info.value
        except Exception as exc:
            myExc = exc

        msg = "Response from Cherrytrack is not OK: Failed to get automation system run info for the given run id"
        assert msg == str(myExc)
        assert len(run_info.errors) == 1
        assert ["Exception during retrieval: " + msg] == run_info.errors

        # Another try does not add more errors
        try:
            run_info.value
        except Exception:
            ...
        assert len(run_info.errors) == 1


def test_picked_samples_from_source_valid(app):
    assert (
        PickedSamplesFromSource(
            PlateBarcode({FIELD_EVENT_BARCODE: "aBarcode"}), RunID({FIELD_EVENT_RUN_ID: "5"})
        ).valid()
        is True
    )
    assert (
        PickedSamplesFromSource(
            PlateBarcode(
                {
                    "missing_barcode_field": "aBarcode",
                }
            ),
            RunID({FIELD_EVENT_RUN_ID: "5"}),
        ).valid()
        is False
    )


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
def test_picked_samples_from_source_value_successful(
    app, run_id, source_barcode, cherrytrack_source_plates_response, mocked_responses, cherrytrack_mock_source_plates
):
    with app.app_context():
        val = PickedSamplesFromSource(
            PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: run_id})
        ).value
        assert val == [cherrytrack_source_plates_response["data"][0], cherrytrack_source_plates_response["data"][2]]
        assert len(val) == 2


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["aUnknownBarcode"])
@pytest.mark.parametrize(
    "cherrytrack_source_plates_response",
    [{"data": {"errors": ["Failed to get samples for the given source plate barcode."]}}],
)
@pytest.mark.parametrize("cherrytrack_mock_source_plates_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_picked_samples_from_source_value_unsuccessful(
    app, run_id, source_barcode, mocked_responses, cherrytrack_mock_source_plates
):
    with app.app_context():
        myExc = None
        with raises(Exception) as exc:
            myExc = exc
            PickedSamplesFromSource(
                PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: run_id})
            ).value

        assert "Response from Cherrytrack is not OK: Failed to get samples for the given source plate barcode." == str(
            myExc.value  # type: ignore
        )
