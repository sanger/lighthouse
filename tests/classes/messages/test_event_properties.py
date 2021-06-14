from pytest import raises
from lighthouse.classes.messages.event_properties import UserID, PickedSamplesFromSource, RunInfo, RunID
import responses
from http import HTTPStatus


def test_user_id_new(app):
    with raises(Exception):
        UserID(None)

    assert UserID({}) is not None
    assert UserID({"test": "another test"}) is not None
    assert UserID({"user_id": "1234"}) is not None


def test_user_id_value(app):
    assert UserID({}).value is None
    assert UserID({"test": "another test"}).value is None
    assert UserID({"user_id": "1234"}).value == "1234"


def test_user_id_valid(app):
    assert UserID({}).valid() is False
    assert UserID({"test": "another test"}).valid() is False
    assert UserID({"user_id": "1234"}).valid() is True


def test_run_id_valid(app):
    assert RunID({"run_id": 1}).valid() is True


def test_run_id_value(app):
    assert RunID({"run_id": 1}).value is 1


def test_run_info_valid(app):
    assert RunInfo(RunID({"run_id": 1})).valid() is True


def test_run_info_value_successful(app, mocked_responses):
    run_id = 2
    url = f"http://10.80.241.124:8000/automation-system-runs/{run_id}"

    expected_response = {
        "data": {"id": run_id, "user_id": "ab1", "liquid_handler_serial_number": "aLiquidHandlerSerialNumber"}
    }

    mocked_responses.add(
        responses.GET,
        url,
        json=expected_response,
        status=HTTPStatus.OK,
    )

    val = RunInfo(RunID({"run_id": run_id})).value

    assert val == expected_response


def test_run_info_value_unsuccessful(app, mocked_responses):
    run_id = 0
    url = f"http://10.80.241.124:8000/automation-system-runs/{run_id}"

    expected_response = None

    mocked_responses.add(
        responses.GET,
        url,
        json=expected_response,
        status=HTTPStatus.OK,
    )

    with raises(Exception):
        RunInfo(RunID({"run_id": run_id})).value


# def test_picked_samples_from_source(app):
# assert PickedSamplesFromSource({"barcode_property": "1", "run_property": "1"}).valid() is False
# assert (
#     PickedSamplesFromSource({"barcode_property": "PlateBarcode", run_property: {run_id_property: "1"}}).valid is True
# )
