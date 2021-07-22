from flask import Blueprint
from flask_cors import CORS

from lighthouse.routes.common.beckman import get_failure_types_v1, get_robots_v1
from lighthouse.types import FlaskResponse

bp = Blueprint("v1_beckman_routes", __name__)
CORS(bp)


@bp.get("/beckman/robots")
def get_robots() -> FlaskResponse:
    get_robots_v1()


@bp.get("/beckman/failure-types")
def get_failure_types() -> FlaskResponse:
    get_failure_types_v1()
