from pytest import raises
import pytest
from lighthouse.classes.event_properties.exceptions import ValidationError, RetrievalError
from lighthouse.classes.event_properties.definitions import (
    UserID,
    RobotSerialNumber,
    RunID,
    PlateBarcode,
    SourcePlateUUID,
    BarcodeNoPlateMapData,
    SamplesFromSource,
    SamplesFromDestination,
    ControlsFromDestination,
    SamplesWithCogUkId,
    SourcePlatesFromDestination,
    FailureType,
)
from lighthouse.classes.event_properties.definitions.biosero import (
    RobotUUID,
    RunInfo,
    SamplesPickedFromSource,
    WellsFromDestination,
)

from unittest.mock import MagicMock, PropertyMock, patch
from lighthouse.classes.messages.warehouse_messages import WarehouseMessage
from lighthouse.classes.messages.sequencescape_messages import SequencescapeMessage
from lighthouse.constants.fields import (
    FIELD_EVENT_RUN_ID,
    FIELD_EVENT_ROBOT,
    FIELD_EVENT_USER_ID,
    FIELD_EVENT_BARCODE,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_FAILURE_TYPE,
    FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER,
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER
)
from http import HTTPStatus

SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS = [
    [RunID, FIELD_EVENT_RUN_ID, ["1234"], [None, "12 34", "12.34"]],
    [PlateBarcode, FIELD_EVENT_BARCODE, ["AA1234"], [None, "AA 1234", ""]],
    [UserID, FIELD_EVENT_USER_ID, ["user1", "user 1"], [None, ""]],
    [RobotSerialNumber, FIELD_EVENT_ROBOT, ["1234"], ["12 34", None, ""]],
    [BarcodeNoPlateMapData, FIELD_EVENT_BARCODE, ["AA1234", "", "something dodgy"], [None]],
    [FailureType, FIELD_FAILURE_TYPE, ["my_error"], [None, "", "my error"]],
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
def test_is_valid_for_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params

    for invalid in invalid_list:
        assert klass({field: invalid}).is_valid() is False

    for valid in valid_list:
        assert klass({field: valid}).is_valid() is True


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_errors_for_simple_event_property(app, params):
    klass, field, valid_list, invalid_list = params

    for invalid in invalid_list:
        assert len(klass({field: invalid}).errors) > 0

    for valid in valid_list:
        assert len(klass({field: valid}).errors) == 0


@pytest.mark.parametrize("params", SIMPLE_CLASS_VALID_PARAM_INVALID_PARAMS)
def test_add_to_warehouse(app, params):
    klass, field, valid_list, invalid_list = params

    for valid in valid_list:
        message = WarehouseMessage("mytype", "myuuid", "at some point")
        try:
            klass({field: valid}).add_to_warehouse_message(message)
        except Exception:
            pytest.fail("Error while adding to message ..")


def test_robot_uuid_new(app):
    assert RobotUUID(RobotSerialNumber({})) is not None
    assert RobotUUID(RobotSerialNumber({"test": "a test"})) is not None
    assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "a test"})) is not None


def test_robot_uuid_is_valid(app):
    assert RobotUUID(RobotSerialNumber({})).is_valid() is False
    assert RobotUUID(RobotSerialNumber({"test": "another test"})).is_valid() is False
    assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"})).is_valid() is True


def test_robot_uuid_value(app):
    with app.app_context():
        with raises(ValidationError):
            RobotUUID(RobotSerialNumber({})).value
            RobotUUID(RobotSerialNumber({"test": "another test"})).value

        with raises(RetrievalError):
            RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "1234"})).value

        uuid = app.config["BIOSERO_ROBOTS"]["CPA"]["uuid"]
        assert RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "CPA"})).value == uuid


def test_robot_uuid_errors(app):
    with app.app_context():
        # After success
        robot = RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "CPA"}))
        robot.value
        assert len(robot.errors) == 0

        # After is_valid false
        robot = RobotUUID(RobotSerialNumber({FIELD_EVENT_ROBOT: "12 34"}))
        robot.is_valid()
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
                FIELD_EVENT_USER_ID: "user1",
                FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "aLiquidHandlerSerialNumber",
                FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
                "automation_system_name": "CPA",
            }
        }

        val = RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id})).value

        assert val == expected_response["data"]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize(
    "cherrytrack_run_info_response",
    [{"errors": ["Failed to get automation system run info for the given run id"]}],
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


def test_samples_picked_from_source_valid(app):
    assert (
        SamplesPickedFromSource(
            PlateBarcode({FIELD_EVENT_BARCODE: "aBarcode"}), RunID({FIELD_EVENT_RUN_ID: "5"})
        ).valid()
        is True
    )
    assert (
        SamplesPickedFromSource(
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
@pytest.mark.parametrize("destination_barcode", ["DS000010001"])
def test_samples_picked_from_source_value_successful(
    app,
    run_id,
    source_barcode,
    destination_barcode,
    cherrytrack_source_plates_response,
    mocked_responses,
    cherrytrack_mock_source_plates,
    samples_from_cherrytrack_into_mongo,
):
    with app.app_context():
        val = SamplesPickedFromSource(
            PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: run_id})
        ).value
        samples, _ = samples_from_cherrytrack_into_mongo

        for elem in val:
            del elem["_id"]
            del elem["Date Tested"]
        for elem in samples:
            del elem["_id"]
            del elem["Date Tested"]
        assert val == [samples[0], samples[2]]
        assert len(val) == 2


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["aUnknownBarcode"])
@pytest.mark.parametrize("destination_barcode", [""])
@pytest.mark.parametrize(
    "cherrytrack_source_plates_response",
    [{"errors": ["Failed to get samples for the given source plate barcode."]}],
)
@pytest.mark.parametrize("cherrytrack_mock_source_plates_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_samples_picked_from_source_value_unsuccessful(
    app, run_id, source_barcode, mocked_responses, cherrytrack_mock_source_plates
):
    with app.app_context():
        myExc = None
        with raises(Exception) as exc:
            myExc = exc
            SamplesPickedFromSource(
                PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: run_id})
            ).value

        assert "Response from Cherrytrack is not OK: Failed to get samples for the given source plate barcode." == str(
            myExc.value  # type: ignore
        )


@pytest.mark.parametrize("run_id", [1])
@pytest.mark.parametrize("source_barcode", ["aBarcodeWithNoSamples"])
@pytest.mark.parametrize("destination_barcode", [""])
@pytest.mark.parametrize(
    "cherrytrack_source_plates_response",
    [
        {
            "data": {
                "samples": [
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "",
                        "destination_coordinate": "",
                        "lab_id": "",
                        "picked": False,
                        "rna_id": "",
                        "lh_sample_uuid": "",
                        "source_barcode": "aBarcodeWithNoSamples",
                        "source_coordinate": "B1",
                        "type": "sample",
                    },
                    {
                        "automation_system_run_id": 1,
                        "destination_barcode": "",
                        "destination_coordinate": "",
                        "lab_id": "",
                        "picked": False,
                        "rna_id": "",
                        "lh_sample_uuid": "",
                        "source_barcode": "aBarcodeWithNoSamples",
                        "source_coordinate": "B2",
                        "type": "sample",
                    },
                ]
            }
        }
    ],
)
def test_samples_picked_from_source_no_lh_sample_uuids(
    app, run_id, source_barcode, mocked_responses, cherrytrack_mock_source_plates
):
    with app.app_context():
        with patch("lighthouse.classes.services.mongo.app.data.driver.db.samples") as samples_collection:
            val = SamplesPickedFromSource(
                PlateBarcode({FIELD_EVENT_BARCODE: source_barcode}), RunID({FIELD_EVENT_RUN_ID: run_id})
            ).value

            samples_collection.find.assert_not_called()
            assert val == []
            assert len(val) == 0


@pytest.mark.parametrize("source_barcode", ["DS000050001"])
def test_all_samples_successful(
    app,
    source_barcode,
    samples_from_cherrytrack_into_mongo,
):
    with app.app_context():
        val = SamplesFromSource(PlateBarcode({FIELD_EVENT_BARCODE: source_barcode})).value
        samples, _ = samples_from_cherrytrack_into_mongo

        for elem in val:
            del elem["_id"]
            del elem["Date Tested"]
        for elem in samples:
            del elem["_id"]
            del elem["Date Tested"]

        assert val == samples


@pytest.mark.parametrize("source_barcode", ["aUnknownBarcode"])
def test_all_samples_unsuccessful(app, source_barcode):
    with app.app_context():
        myExc = None
        obj = MagicMock()
        obj.is_valid.return_value = True
        type(obj).value = PropertyMock(side_effect=Exception("boom!"))
        try:
            SamplesFromSource(obj).value
        except Exception as exc:
            myExc = exc

        assert "boom!" == str(myExc)


def test_source_plate_uuid_new(app, source_plates):
    assert SourcePlateUUID(PlateBarcode({})) is not None
    assert SourcePlateUUID(PlateBarcode({"test": "a test"})) is not None
    assert SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "plate_123"})) is not None


def test_source_plate_uuid_is_valid(app, source_plates):
    assert SourcePlateUUID(PlateBarcode({})).is_valid() is False
    assert SourcePlateUUID(PlateBarcode({"test": "another test"})).is_valid() is False
    assert SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "plate_123"})).is_valid() is True


def test_source_plate_uuid_value(app, source_plates):
    with app.app_context():
        with raises(ValidationError):
            SourcePlateUUID(PlateBarcode({})).value
            SourcePlateUUID(PlateBarcode({"test": "another test"})).value

        with raises(Exception):
            SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "1234"})).value

        uuid = source_plates[0][FIELD_LH_SOURCE_PLATE_UUID]

        assert SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "plate_123"})).value == uuid


def test_source_plate_uuid_errors(app, source_plates):
    with app.app_context():
        # After success
        source_plate_property = SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "plate_123"}))
        source_plate_property.value
        assert len(source_plate_property.errors) == 0

        # After is_valid false
        source_plate_property = SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "plate _123"}))
        source_plate_property.is_valid()
        assert len(source_plate_property.errors) > 0

        # After retrieval error
        source_plate_property = SourcePlateUUID(PlateBarcode({FIELD_EVENT_BARCODE: "1234"}))
        with raises(Exception):
            source_plate_property.value

        assert len(source_plate_property.errors) > 0


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_wells_from_destination_value_gets_value(
    app,
    run_id,
    destination_barcode,
    mocked_responses,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
):
    with app.app_context():
        val = WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode})).value
        assert val == cherrytrack_destination_plate_response["data"]["wells"]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "cherrytrack_destination_plate_response",
    [{"data": {"wells": [{"destination_coordinate": "H1"}, {"destination_coordinate": "H1"}]}}],
)
def test_wells_from_destination_value_fails_with_duplicated_wells(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    cherrytrack_destination_plate_response,
    mocked_responses,
    cherrytrack_mock_destination_plate,
):
    with app.app_context():
        instance = WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        assert instance.is_valid() is True
        assert instance.errors == []

        with pytest.raises(Exception):
            instance.value

        assert instance.is_valid() is False
        assert instance.errors == [
            "Exception during retrieval: Some coordinates have clashing samples/controls: {'H1'}"
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_all_samples_from_destination_value_gets_value(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mocked_responses,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
):
    with app.app_context():
        val = SamplesFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        ).value
        samples, _ = samples_from_cherrytrack_into_mongo

        for sample in val.values():
            del sample["_id"]
            del sample["Date Tested"]
        for sample in samples:
            del sample["_id"]
            del sample["Date Tested"]
        assert val == {"H08": samples[0], "H12": samples[2]}


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "cherrytrack_destination_plate_response",
    [{"data": {"wells": [{"type": "sample", "lh_sample_uuid": "unknown", "destination_coordinate": "H1"}]}}],
)
def test_all_samples_from_destination_value_fails_with_unknown_samples(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    cherrytrack_destination_plate_response,
    mocked_responses,
    cherrytrack_mock_destination_plate,
):
    with app.app_context():
        instance = SamplesFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        )
        assert instance.is_valid() is True
        assert instance.errors == []

        with pytest.raises(Exception):
            instance.value

        assert instance.is_valid() is False
        assert instance.errors == [
            (
                "Exception during retrieval: Some samples cannot be obtained because they are not present"
                " in Mongo. Please review: ['unknown']"
            )
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "cherrytrack_destination_plate_response",
    [
        {
            "data": {
                "wells": [
                    {"type": "sample", "lh_sample_uuid": "uuid1", "destination_coordinate": "H1"},
                    {"type": "sample", "lh_sample_uuid": "uuid2", "destination_coordinate": "H2"},
                    {"type": "sample", "lh_sample_uuid": "uuid1", "destination_coordinate": "H3"},
                ]
            }
        }
    ],
)
def test_all_samples_from_destination_value_fails_with_duplicated_samples(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    cherrytrack_destination_plate_response,
    mocked_responses,
    cherrytrack_mock_destination_plate,
):
    with app.app_context():
        instance = SamplesFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        )
        assert instance.is_valid() is True
        assert instance.errors == []

        with pytest.raises(Exception):
            instance.value

        assert instance.is_valid() is False
        assert instance.errors == [
            ("Exception during retrieval: There is duplication in the lh sample uuids provided: ['uuid1']")
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_all_controls_from_destination_value_gets_value(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mocked_responses,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
):
    with app.app_context():
        wells = cherrytrack_destination_plate_response["data"]["wells"]
        val = ControlsFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        ).value

        assert val == {"E10": wells[2], "E11": wells[3]}


@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "cherrytrack_destination_plate_response",
    [
        {
            "data": {
                "wells": [
                    {"type": "control", "control": "negative", "destination_coordinate": "H1"},
                    {"type": "control", "control": "negative", "destination_coordinate": "H2"},
                ]
            }
        }
    ],
)
def test_all_controls_from_destination_value_fails_with_missing_controls(
    app,
    destination_barcode,
    mocked_responses,
    cherrytrack_mock_destination_plate,
):
    with app.app_context():
        instance = ControlsFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        )
        assert instance.is_valid() is True
        assert instance.errors == []

        with pytest.raises(Exception):
            instance.value

        assert instance.is_valid() is False
        assert instance.errors == [
            ("Exception during retrieval: We were expecting one positive and one negative control to be present.")
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "baracoda_mock_responses",
    [
        {
            "TC1": {"barcodes_group": {"id": 1, "barcodes": ["COGUK1", "COGUK2"]}},
        }
    ],
)
def test_samples_with_cog_uk_id_from_destination_add_to_warehouse(
    app,
    run_id,
    centres,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mlwh_samples_in_cherrytrack,
    mocked_responses,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
    baracoda_mock_barcodes_group,
    baracoda_mock_responses,
):
    with app.app_context():
        samples, _ = samples_from_cherrytrack_into_mongo
        instance = SamplesWithCogUkId(
            SamplesFromDestination(WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode})))
        )
        message = WarehouseMessage("mytype", "myuuid", "at some point")
        instance.add_to_warehouse_message(message)
        assert message._subjects == [
            {
                "friendly_name": "aRootSampleId1__DS000050001_A01__centre_1__Positive",
                "role_type": "sample",
                "subject_type": "sample",
                "uuid": "aLighthouseUUID1",
            },
            {
                "friendly_name": "aRootSampleId3__DS000050001_A03__centre_1__Positive",
                "role_type": "sample",
                "subject_type": "sample",
                "uuid": "aLighthouseUUID3",
            },
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["DS000050001"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
@pytest.mark.parametrize(
    "baracoda_mock_responses",
    [
        {
            "TC1": {"barcodes_group": {"id": 1, "barcodes": ["COGUK1", "COGUK2"]}},
        }
    ],
)
def test_samples_with_cog_uk_ids_from_destination_add_to_sequencescape(
    app,
    run_id,
    centres,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mlwh_samples_in_cherrytrack,
    mocked_responses,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
    baracoda_mock_barcodes_group,
    baracoda_mock_responses,
):
    with app.app_context():
        samples, _ = samples_from_cherrytrack_into_mongo
        instance = SamplesWithCogUkId(
            SamplesFromDestination(WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode})))
        )
        message = SequencescapeMessage()
        instance.add_to_sequencescape_message(message)
        assert message._contents == {
            "H08": {
                "content": {
                    "name": "DS000050001_A01",
                    "phenotype": "Positive",
                    "sample_description": "aRootSampleId1",
                    "supplier_name": "COGUK1",
                    "uuid": "aLighthouseUUID1",
                }
            },
            "H12": {
                "content": {
                    "name": "DS000050001_A03",
                    "phenotype": "Positive",
                    "sample_description": "aRootSampleId3",
                    "supplier_name": "COGUK2",
                    "uuid": "aLighthouseUUID3",
                }
            },
        }


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_source_plates_from_destination_value_gets_value(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mocked_responses,
    source_plates,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
):
    with app.app_context():
        val = SourcePlatesFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        ).value

        for elem in val:
            del elem["_id"]

        assert val == [
            {"Lab ID": "lab_1", "barcode": "plate_123", "lh_source_plate_uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc"}
        ]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize("source_barcode", ["plate_123"])
@pytest.mark.parametrize("destination_barcode", ["HT-1234"])
def test_source_plates_from_destination_add_to_warehouse(
    app,
    run_id,
    destination_barcode,
    samples_from_cherrytrack_into_mongo,
    mocked_responses,
    source_plates,
    cherrytrack_mock_destination_plate,
    cherrytrack_destination_plate_response,
):
    with app.app_context():
        instance = SourcePlatesFromDestination(
            WellsFromDestination(PlateBarcode({FIELD_EVENT_BARCODE: destination_barcode}))
        )

        message = WarehouseMessage("mytype", "myuuid", "at some point")
        instance.add_to_warehouse_message(message)
        assert message._subjects == [
            {
                "role_type": "cherrypicking_source_labware",
                "subject_type": "plate",
                "friendly_name": "plate_123",
                "uuid": "a17c38cd-b2df-43a7-9896-582e7855b4cc",
            }
        ]
