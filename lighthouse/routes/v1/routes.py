from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.plates import create_plate_from_barcode_v1, find_plate_from_barcode_v1
from lighthouse.routes.common.reports import create_report_v1, delete_reports_v1, get_reports_v1
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_routes", __name__)
CORS(bp)


@bp.post("/plates/new")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    return create_plate_from_barcode_v1()


@bp.get("/plates")
def find_plate_from_barcode_endpoint() -> FlaskResponse:
    return find_plate_from_barcode_v1()


@bp.get("/reports")
def get_reports_endpoint() -> FlaskResponse:
    return get_reports_v1()


@bp.post("/reports/new")
def create_report_endpoint() -> FlaskResponse:
    return create_report_v1()


@bp.post("/delete_reports")
def delete_reports_endpoint() -> FlaskResponse:
    return delete_reports_v1()
