from flask import Blueprint, request
from flask_cors import CORS

from lighthouse.types import FlaskResponse

from lighthouse.constants.fields import FIELD_EVENT_TYPE
from lighthouse.classes.beckman_v3 import Beckman

from lighthouse.hooks.beckman_events import create_plate_event
from lighthouse.routes.v1.beckman_routes import (
    fail_plate_from_barcode_endpoint as v1_fail_plate_from_barcode,
    create_plate_from_barcode_endpoint as v1_create_plate_from_barcode,
    get_failure_types_endpoint as v1_get_failure_types,
    get_robots_endpoint as v1_get_robots,
)

from lighthouse.helpers.responses import internal_server_error, bad_request

bp = Blueprint("v3_beckman_routes", __name__)
CORS(bp)


@bp.get("/beckman/robots")
def get_robots_endpoint() -> FlaskResponse:
    return v1_get_robots()


@bp.get("/beckman/failure-types")
def get_failure_types_endpoint() -> FlaskResponse:
    return v1_get_failure_types()


@bp.get("/plate-events/create")
def create_plate_event_endpoint() -> FlaskResponse:
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


@bp.get("/cherrypicked-plates/create")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    return v1_create_plate_from_barcode()


@bp.get("/cherrypicked-plates/fail")
def fail_plate_from_barcode_endpoint() -> FlaskResponse:
    return v1_fail_plate_from_barcode()
