from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.beckman import get_failure_types, get_robots
from lighthouse.routes.common.cherrypicked_plates import create_plate_from_barcode, fail_plate_from_barcode
from lighthouse.routes.common.plate_events import create_plate_event
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_beckman_routes", __name__)
CORS(bp)


@bp.get("/beckman/robots")
def get_robots_endpoint() -> FlaskResponse:
    return get_robots()


@bp.get("/beckman/failure-types")
def get_failure_types_endpoint() -> FlaskResponse:
    return get_failure_types()


@bp.get("/cherrypicked-plates/create")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    return create_plate_from_barcode()


@bp.get("/cherrypicked-plates/fail")
def fail_plate_from_barcode_endpoint() -> FlaskResponse:
    return fail_plate_from_barcode()


@bp.get("/plate-events/create")
def create_plate_event_endpoint() -> FlaskResponse:
    return create_plate_event()
