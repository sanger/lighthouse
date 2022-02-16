from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

from lighthouse.types import FlaskResponse

from lighthouse.constants.fields import FIELD_EVENT_TYPE
from lighthouse.classes.beckman_v3 import Beckman

from lighthouse.hooks.beckman_events import create_plate_event
from lighthouse.routes.common.beckman import get_failure_types, get_robots
from lighthouse.routes.common.cherrypicked_plates import create_plate_from_barcode, fail_plate_from_barcode
from lighthouse.routes.common.plate_events import create_plate_event as v1_create_plate_event

bp = Blueprint("beckman_v3_routes", __name__)
CORS(bp)


@bp.get("/beckman/robots")
def get_robots_endpoint() -> FlaskResponse:
    return get_robots()


@bp.get("/beckman/failure-types")
def get_failure_types_endpoint() -> FlaskResponse:
    return get_failure_types()


@bp.get("/plate-events/create")
def create_plate_event_endpoint() -> FlaskResponse:
    event_type = request.args.get(FIELD_EVENT_TYPE, type=str)
    if event_type in [Beckman.EVENT_SOURCE_UNRECOGNISED, Beckman.EVENT_SOURCE_COMPLETED]:
        return create_plate_event()
    return v1_create_plate_event()


@bp.get("/cherrypicked-plates/create")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    return create_plate_from_barcode()


@bp.get("/cherrypicked-plates/fail")
def fail_plate_from_barcode_endpoint() -> FlaskResponse:
    return fail_plate_from_barcode()