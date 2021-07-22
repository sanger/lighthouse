from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.plates import create_plate_from_barcode_v1, find_plate_from_barcode_v1
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_routes", __name__)
CORS(bp)


@bp.post("/plates/new")
def create_plate_from_barcode() -> FlaskResponse:
    return create_plate_from_barcode_v1()


@bp.get("/plates")
def find_plate_from_barcode() -> FlaskResponse:
    return find_plate_from_barcode_v1()
