from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

from lighthouse.types import FlaskResponse
from lighthouse.hooks.beckman_events import create_plate_event

bp = Blueprint("beckman_v3_routes", __name__)
CORS(bp)


def redirect_endpoint(base_url):
   
    redirect_url = base_url
    return redirect(redirect_url, code=HTTPStatus.PERMANENT_REDIRECT)


@bp.get("/plate-events/create")
def create_plate_event_endpoint() -> FlaskResponse:
    return create_plate_event()


@bp.get("/cherrypicked-plates/create")
def create_plate_from_barcode_endpoint() -> FlaskResponse:
    # return create_plate_from_barcode()
    pass


@bp.get("/cherrypicked-plates/fail")
def fail_plate_from_barcode_endpoint() -> FlaskResponse:
    # return fail_plate_from_barcode()
    pass