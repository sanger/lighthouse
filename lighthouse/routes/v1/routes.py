from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.plates import (
    create_plate_from_barcode,
    find_plate_from_barcode,
    find_cherrytrack_plate_from_barcode,
    get_control_locations,
)
from lighthouse.routes.common.reports import create_report, delete_reports, get_reports
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_routes", __name__)
CORS(bp)


@bp.post("/plates/new")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    return create_plate_from_barcode()


@bp.get("/plates")
def find_plate_from_barcode_endpoint() -> FlaskResponse:
    return find_plate_from_barcode()


@bp.get("/plates/cherrytrack")
def find_cherrytrack_plate_from_barcode_endpoint() -> FlaskResponse:
    return find_cherrytrack_plate_from_barcode()


@bp.get("/reports")
def get_reports_endpoint() -> FlaskResponse:
    return get_reports()


@bp.post("/reports/new")
def create_report_endpoint() -> FlaskResponse:
    return create_report()


@bp.post("/delete_reports")
def delete_reports_endpoint() -> FlaskResponse:
    return delete_reports()


# Put in this file as this is used as the root routes,
# so there is no prefix
# which is what was agreed with Beckman
# Otherwise, could move to v1_beckman_routes
# which has /v1 url_prefix
@bp.post("/pickings")
def get_control_locations_endpoint() -> FlaskResponse:
    return get_control_locations()
