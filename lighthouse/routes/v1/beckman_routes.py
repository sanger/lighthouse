from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.beckman import get_failure_types_v1, get_robots_v1
from lighthouse.routes.common.cherrypicked_plates import create_plate_from_barcode_v1, fail_plate_from_barcode_v1
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_beckman_routes", __name__)
CORS(bp)


@bp.get("/beckman/robots")
def get_robots() -> FlaskResponse:
    return get_robots_v1()


@bp.get("/beckman/failure-types")
def get_failure_types() -> FlaskResponse:
    return get_failure_types_v1()


@bp.get("/cherrypicked-plates/create")
def create_plate_from_barcode() -> FlaskResponse:  # noqa: C901
    return create_plate_from_barcode_v1()


@bp.get("/cherrypicked-plates/fail")
def fail_plate_from_barcode() -> FlaskResponse:
    return fail_plate_from_barcode_v1()
