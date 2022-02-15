from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

from lighthouse.routes.common.beckman import get_failure_types, get_robots
from lighthouse.routes.common.cherrypicked_plates import create_plate_from_barcode, fail_plate_from_barcode
from lighthouse.hooks.beckman_events import create_plate_event
from lighthouse.types import FlaskResponse

bp = Blueprint("beckman_v3_routes", __name__)
CORS(bp)
import logging
logger = logging.getLogger(__name__)

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


#@bp.get("/cherrypicked-plates/create")
@bp.get("/plate-events/create")
def create_plate_event_endpoint() -> FlaskResponse:
    logger.debug("BECKMAN_ENABLE_V3 create_plate_event_endpoint")
    return create_plate_event()


# @bp.get("/cherrypicked-plates/fail")
# def fail_plate_from_barcode_endpoint() -> FlaskResponse:
#     # return fail_plate_from_barcode()
#     pass