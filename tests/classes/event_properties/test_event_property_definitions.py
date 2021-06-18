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
import responses
from http import HTTPStatus


def test_user_id_new(app):
    with raises(ValidationError):
        UserID(None)

    assert UserID({}) is not None
    assert UserID({"test": "another test"}) is not None
    assert UserID({FIELD_EVENT_USER_ID: "1234"}) is not None


def test_user_id_value(app):
    with raises(ValidationError):
        UserID({}).value
        UserID({"test": "another test"}).value

    assert UserID({FIELD_EVENT_USER_ID: "1234"}).value == "1234"


def test_user_id_validate(app):
    assert UserID({}).validate() is False
    assert UserID({"test": "another test"}).validate() is False
    assert UserID({FIELD_EVENT_USER_ID: "1234"}).validate() is True


def test_user_id_errors(app):
    assert len(UserID({}).errors) > 0
    assert len(UserID({"test": "another test"}).errors) > 0
    assert len(UserID({FIELD_EVENT_USER_ID: "1234"}).errors) == 0


def test_robot_serial_number_new(app):
    assert RobotSerialNumber({}) is not None
    assert RobotSerialNumber({"test": "a test"}) is not None
    assert RobotSerialNumber({FIELD_EVENT_ROBOT: "a test"}) is not None


def test_robot_serial_number_validate(app):
    assert RobotSerialNumber({}).validate() is False
    assert RobotSerialNumber({"test": "another test"}).validate() is False
    assert RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"}).validate() is True


def test_robot_serial_number_value(app):
    with raises(ValidationError):
        RobotSerialNumber({}).value
        RobotSerialNumber({"test": "another test"}).value

    assert RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"}).value == "1234"


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


def test_plate_barcode_valid(app):
    assert PlateBarcode({FIELD_EVENT_BARCODE: "aBarcode"}).valid() is True


def test_plate_barcode_value(app):
    assert PlateBarcode({FIELD_EVENT_BARCODE: "aBarcode"}).value == "aBarcode"


def test_run_id_valid(app):
    assert RunID({FIELD_EVENT_RUN_ID: 1}).valid() is True


def test_run_id_value(app):
    assert RunID({FIELD_EVENT_RUN_ID: 1}).value == 1


def test_run_info_valid(app):
    assert RunInfo(RunID({FIELD_EVENT_RUN_ID: 1})).valid() is True


def test_run_info_value_successful(app, mocked_responses):
    with app.app_context():
        run_id = 2
        url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

        expected_response = {
            "data": {
                "id": run_id,
                FIELD_EVENT_USER_ID: "ab1",
                "liquid_handler_serial_number": "aLiquidHandlerSerialNumber",
            }
        }

        mocked_responses.add(
            responses.GET,
            url,
            json=expected_response,
            status=HTTPStatus.OK,
        )

        val = RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id})).value

        assert val == expected_response["data"]


def test_run_info_value_unsuccessful(app, mocked_responses):
    with app.app_context():
        run_id = 0
        url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

        expected_response = {"data": {"errors": ["Failed to get automation system run info for the given run id"]}}

        mocked_responses.add(
            responses.GET,
            url,
            json=expected_response,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        myExc = None
        with raises(Exception) as exc:
            myExc = exc
            RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id})).value
        msg = "Response from Cherrytrack is not OK: Failed to get automation system run info for the given run id"
        assert msg == str(myExc.value)  # type: ignore


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
