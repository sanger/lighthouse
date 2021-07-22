from http import HTTPStatus

from flask import Blueprint, redirect
from flask_cors import CORS

bp = Blueprint("eve_routes", __name__)
CORS(bp)


@bp.route("/cherrypick-test-data", methods=["GET", "POST"])
def cptd_redirect():
    return redirect("/cherrypick-test-data", code=HTTPStatus.PERMANENT_REDIRECT)


@bp.get("/cherrypick-test-data/<test_id>")
def single_cptd_redirect(test_id):
    return redirect(f"/cherrypick-test-data/{test_id}", code=HTTPStatus.PERMANENT_REDIRECT)
