from pytest import raises
from lighthouse.classes.messages.event_properties import (  # type: ignore
    UserID,
    ValidationError,
    RobotSerialNumber,
    RobotUUID,
    RetrievalError,
    RunInfo,
    RunID,
    PlateBarcode,
    PickedSamplesFromSource,
)
import responses
from http import HTTPStatus


def test_user_id_new(app):
    with raises(ValidationError):
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


def test_user_id_errors(app):
    assert len(UserID({}).errors) > 0
    assert len(UserID({"test": "another test"}).errors) > 0
    assert len(UserID({"user_id": "1234"}).errors) == 0


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


def test_plate_barcode_valid(app):
    assert PlateBarcode({"barcode": "aBarcode"}).valid() is True


def test_plate_barcode_value(app):
    assert PlateBarcode({"barcode": "aBarcode"}).value == "aBarcode"


def test_run_id_valid(app):
    assert RunID({"automation_system_run_id": 1}).valid() is True


def test_run_id_value(app):
    assert RunID({"automation_system_run_id": 1}).value == 1


def test_run_info_valid(app):
    assert RunInfo(RunID({"automation_system_run_id": 1})).valid() is True


def test_run_info_value_successful(app, mocked_responses):
    with app.app_context():
        run_id = 2
        url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

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

        assert val == expected_response["data"]


def test_run_info_value_unsuccessful(app, mocked_responses):
    with app.app_context():
        run_id = 0
        url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"

        expected_response = None

        mocked_responses.add(
            responses.GET,
            url,
            json=expected_response,
            status=HTTPStatus.OK,
        )

        with raises(Exception):
            RunInfo(RunID({"automation_system_run_id": run_id})).value


def test_picked_samples_from_source_valid(app):
    assert (
        PickedSamplesFromSource(
            PlateBarcode({"barcode": "aBarcode"}), RunInfo(RunID({"automation_system_run_id": 1}))
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
            RunInfo(RunID({"automation_system_run_id": 1})),
        ).valid()
        is False
    )
    assert (
        PickedSamplesFromSource(
            PlateBarcode(
                {
                    "barcode": "aBarcode",
                }
            ),
            RunInfo(RunID({"mising_run_id": 1})),
        ).valid()
        is False
    )


def test_picked_samples_from_source_value_successful(app, mocked_responses):
    with app.app_context():
        source_barcode = "aBarcode"
        run_id = 1

        run_url = f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}"
        expected_run_response = {
            "data": {"id": run_id, "user_id": "ab1", "liquid_handler_serial_number": "aLiquidHandlerSerialNumber"}
        }
        mocked_responses.add(
            responses.GET,
            run_url,
            json=expected_run_response,
            status=HTTPStatus.OK,
        )

        source_plates_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_barcode}?run-id={run_id}"
        expected_source_plates_response = {
            "data": [
                {
                    "control": True,
                    "control_barcode": "control_barcode1",
                    "control_coordinate": "A1",
                    "lab_id": "lab_id",
                    "picked": True,
                    "rna_id": "rna_id1",
                    "robot_barcode": "robot_barcode",
                    "run_id": run_id,
                    "sample_id": "sample_id1",
                    "source_barcode": source_barcode,
                    "source_coordinate": "B1",
                },
                {
                    "control": True,
                    "control_barcode": "control_barcode2",
                    "control_coordinate": "A2",
                    "lab_id": "lab_id",
                    "picked": False,
                    "rna_id": "rna_id2",
                    "robot_barcode": "robot_barcode",
                    "run_id": run_id,
                    "sample_id": "sample_id2",
                    "source_barcode": source_barcode,
                    "source_coordinate": "B2",
                },
            ]
        }
        mocked_responses.add(
            responses.GET,
            source_plates_url,
            json=expected_source_plates_response,
            status=HTTPStatus.OK,
        )

        val = PickedSamplesFromSource(
            PlateBarcode({"barcode": source_barcode}), RunInfo(RunID({"automation_system_run_id": run_id}))
        ).value
        assert val == [expected_source_plates_response["data"][1]]
