from pytest import raises
from lighthouse.classes.event_properties.interfaces import ValidationError, RetrievalError
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
            "data": {"id": run_id, FIELD_EVENT_USER_ID: "ab1", "liquid_handler_serial_number": "aLiquidHandlerSerialNumber"}
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

        myExc = ""
        with raises(Exception) as exc:
            myExc = exc
            RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id})).value

        assert (
            "Response from Cherrytrack is not OK: Failed to get automation system run info for the given run id"
            == str(myExc.value)
        )


def test_picked_samples_from_source_valid(app):
    assert PickedSamplesFromSource(
        PlateBarcode({FIELD_EVENT_BARCODE: "aBarcode"}), RunID({FIELD_EVENT_RUN_ID: "5"})
    ).valid() is True
    assert (
        PickedSamplesFromSource(
            PlateBarcode(
                {
                    "missing_barcode_field": "aBarcode",
                }
            ),
            RunID({FIELD_EVENT_RUN_ID: "5"})
        ).valid()
        is False
    )


def test_picked_samples_from_source_value_successful(app, mocked_responses):
    with app.app_context():
        source_barcode = "DS000050001"

        source_plates_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_barcode}"
        expected_source_plates_response = {
            "data": [
                {
                    "automation_system_run_id": "",
                    "destination_barcode": "",
                    "destination_coordinate": "",
                    "destination_plate_well_id": "",
                    "lab_id": "MK",
                    "picked": False,
                    "rna_id": "RNA-S-00005-00000072",
                    "sample_id": "e1007f3c-cdce-4274-a1f1-d455f03618a3",
                    "source_barcode": "DS000050001",
                    "source_coordinate": "A1",
                    "source_plate_well_id": 472,
                },
                {
                    "automation_system_run_id": "5",
                    "destination_barcode": "DN00000005",
                    "destination_coordinate": "C12",
                    "destination_plate_well_id": "420",
                    "lab_id": "MK",
                    "picked": True,
                    "rna_id": "RNA-S-00005-00000011",
                    "sample_id": "81e5967c-2499-47a7-9c1d-57b61b565cc0",
                    "source_barcode": "DS000050001",
                    "source_coordinate": "A2",
                    "source_plate_well_id": 411,
                },
                {
                    "automation_system_run_id": "5",
                    "destination_barcode": "DN00000005",
                    "destination_coordinate": "C11",
                    "destination_plate_well_id": "419",
                    "lab_id": "MK",
                    "picked": True,
                    "rna_id": "RNA-S-00005-00000010",
                    "sample_id": "67155efa-9a88-4c50-aa34-c5e8cc8714a3",
                    "source_barcode": "DS000050001",
                    "source_coordinate": "A3",
                    "source_plate_well_id": 410,
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
            PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: "5"})
        ).value
        assert val == expected_source_plates_response["data"][1:]
        assert len(val) == 2


def test_picked_samples_from_source_value_unsuccessful(app, mocked_responses):
    with app.app_context():
        source_barcode = "aUnknownBarcode"

        source_plates_url = f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_barcode}"
        expected_source_plates_response = {
            "data": {"errors": ["Failed to get samples for the given source plate barcode."]}
        }
        mocked_responses.add(
            responses.GET,
            source_plates_url,
            json=expected_source_plates_response,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        myExc = ""
        with raises(Exception) as exc:
            myExc = exc
            PickedSamplesFromSource(
                PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: "5"})
            ).value

        assert "Response from Cherrytrack is not OK: Failed to get samples for the given source plate barcode." == str(
            myExc.value
        )
