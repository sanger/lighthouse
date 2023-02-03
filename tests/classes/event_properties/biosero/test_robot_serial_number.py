from http import HTTPStatus

import pytest

from lighthouse.classes.event_properties.definitions import RunID
from lighthouse.classes.event_properties.definitions.biosero import RobotSerialNumber, RunInfo
from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER,
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME,
    FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER,
    FIELD_CHERRYTRACK_USER_ID,
    FIELD_EVENT_RUN_ID,
)


def test_robot_serial_number_valid(app):
    assert RobotSerialNumber(RunInfo(RunID({FIELD_EVENT_RUN_ID: 1}))).is_valid() is True


@pytest.mark.parametrize("run_id", [5])
def test_robot_serial_number_value_successful(app, run_id, mocked_responses, cherrytrack_mock_run_info):
    with app.app_context():
        expected_response = {
            "data": {
                "id": run_id,
                FIELD_CHERRYTRACK_USER_ID: "user1",
                FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "aLiquidHandlerSerialNumber",
                FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
                FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: "CPA",
            }
        }

        val = RobotSerialNumber(RunInfo(RunID({FIELD_EVENT_RUN_ID: run_id}))).value

        assert val == expected_response["data"][FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER]


@pytest.mark.parametrize("run_id", [5])
@pytest.mark.parametrize(
    "cherrytrack_run_info_response",
    [{"errors": ["Failed to get automation system run info for the given run id"]}],
)
@pytest.mark.parametrize("cherrytrack_mock_run_info_status", [HTTPStatus.INTERNAL_SERVER_ERROR])
def test_user_id_value_unsuccessful(app, mocked_responses, cherrytrack_mock_run_info):
    with app.app_context():
        exception = None
        robot = RobotSerialNumber(RunInfo(RunID({FIELD_EVENT_RUN_ID: 5})))
        try:
            robot.value
        except Exception as e:
            exception = e

        msg = "Response from Cherrytrack is not OK: Failed to get automation system run info for the given run id"
        assert msg == str(exception)
        assert ["Exception during retrieval: " + msg] == robot.errors
