#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from collections import namedtuple
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Iterable, List, Optional, Tuple, cast
from uuid import uuid4

from flask import abort, jsonify, make_response, request
from flask.wrappers import Request

from lighthouse.classes.automation_system import AutomationSystem
from lighthouse.classes.beckman_v3 import Beckman
from lighthouse.constants.fields import (
    FIELD_EVENT_BARCODE,
    FIELD_EVENT_ROBOT,
    FIELD_EVENT_TYPE,
    FIELD_EVENT_USER_ID,
    FIELD_EVENT_UUID,
)
from lighthouse.helpers.responses import ok
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)


def create_event_dict(request: Request, required_params: Tuple[str, ...]) -> Dict[str, Any]:
    """Construct event dict with the required params

    Args:
        request (Request): the request

    Returns:
        Dict[str, ...]: the event dict with the required parameters
    """
    params: List[str] = [FIELD_EVENT_TYPE, FIELD_EVENT_ROBOT, FIELD_EVENT_USER_ID]

    event_type, robot_serial_number, user_id = get_required_params(request, required_params)

    Event = namedtuple("Event", params)  # type: ignore
    event = Event(event_type, robot_serial_number, user_id)._asdict()  # type: ignore

    event["_created"] = datetime.now()
    barcode = request.args.get("barcode", default=None, type=str)
    if barcode is not None:
        event[FIELD_EVENT_BARCODE] = barcode
    event[FIELD_EVENT_UUID] = str(uuid4())

    return event


def get_required_params(request: Request, required_params: Tuple[str, ...]) -> Tuple[str, ...]:
    """Get the required parameters parsed from the URL of the request; in the order they were provided.

    Args:
        request (Request): the request which contains the parameters to be extracted from.
        required_params (Tuple[str, ...]): the parameters to extract and test.

    Raises:
        Exception: if any of the required parameters are missing or empty.

    Returns:
        Tuple[str, ...]: the parameters extracted from the request, in the order provided.
    """
    logger.info(f"Extracting the following parameters from the request: {required_params}")

    def extract_and_test(param: str) -> Optional[str]:
        # extract the parameter from the request
        param_from_req = request.args.get(param, type=str)

        # check that the value is not None or an empty string
        if param_from_req is not None and param_from_req:
            return param_from_req

        return None

    required_params_dict = {param: extract_and_test(param) for param in required_params}

    #  get a list of all those which have not been set, i.e. empty strings
    missing_params = list(filter(lambda param: required_params_dict.get(param) is None, required_params_dict))

    if missing_params:
        formatted_missing_params = "'{0}'".format("', '".join(missing_params))

        raise Exception(f"GET request needs {formatted_missing_params} in URL")

    return tuple(cast(Iterable[str], required_params_dict.values()))


def create_plate_event() -> FlaskResponse:
    """/v1/plate-events/create beckman endpoint to publish a plate event message to the RabbitMQ broker.

    Returns:
        FlaskResponse: if successful, return an empty list of errors and an OK status; otherwise, a list of errors and
        the corresponding HTTP status code.
    """
    required_params = (FIELD_EVENT_TYPE, FIELD_EVENT_ROBOT, FIELD_EVENT_USER_ID)

    write_exception_error = False
    plate_event = None
    try:
        event = create_event_dict(request, required_params)
        automation_system = AutomationSystem.AutomationSystemEnum.BECKMAN
        # Assume we only receive one event

        beckman = Beckman()
        event_type = event.get(FIELD_EVENT_TYPE)

        if event_type is None or not isinstance(event_type, str) or not event_type:
            raise Exception("Cannot determine event type in hook")

        logger.info(
            f"Attempting to process a '{event_type}' plate event message received from {automation_system.name}"
        )

        plate_event = beckman.get_plate_event(event_type)
        plate_event.initialize_event(event)
        write_exception_error = True

        if plate_event.is_valid():
            plate_event.process_event()

        plate_event.process_errors()
        if len(plate_event.errors) > 0:
            write_exception_error = False
            raise Exception("The processing of the event failed.")

        return ok(errors=[])

    except Exception as e:
        if write_exception_error:
            if plate_event is not None:
                plate_event.process_exception(e)

        message = str(e)
        issues: Any = None

        if plate_event is not None and hasattr(plate_event, "errors"):
            issues = plate_event.errors
        else:
            issues = [message]

        abort(
            make_response(
                jsonify(
                    {
                        "_status": "ERR",
                        "_issues": issues,
                        "_error": {
                            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                            "message": message,
                        },
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        )
