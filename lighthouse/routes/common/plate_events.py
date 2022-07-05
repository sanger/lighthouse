from flask import request

from lighthouse.classes.beckman_v3 import Beckman
from lighthouse.constants.fields import FIELD_EVENT_TYPE
from lighthouse.helpers.responses import bad_request, internal_server_error
from lighthouse.types import FlaskResponse


def create_plate_event() -> FlaskResponse:
    event_type = request.args.get(FIELD_EVENT_TYPE, type=str)
    if event_type is None or (event_type == ""):
        return bad_request([f"Unrecognised event type '{event_type}'"])

    if event_type in [
        Beckman.EVENT_SOURCE_UNRECOGNISED,
        Beckman.EVENT_SOURCE_COMPLETED,
        Beckman.EVENT_SOURCE_ALL_NEGATIVES,
        Beckman.EVENT_SOURCE_NO_PLATE_MAP_DATA,
    ]:
        return create_plate_event()

    return internal_server_error([f"Unrecognised event type '{event_type}'"])
