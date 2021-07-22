from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

bp = Blueprint("eve_routes", __name__)
CORS(bp)


def redirect_endpoint(base_url):
    # We need to include any query parameters that might have been on the original request
    redirect_url = base_url
    query_split = request.url.split("?")
    if len(query_split) > 1:
        redirect_url += f"?{query_split[1]}"

    return redirect(redirect_url, code=HTTPStatus.PERMANENT_REDIRECT)


@bp.route("/cherrypick-test-data", methods=["GET", "POST"])
def cptd_redirect():
    return redirect_endpoint("/cherrypick-test-data")


@bp.get("/cherrypick-test-data/<test_id>")
def single_cptd_redirect(test_id):
    return redirect_endpoint(f"/cherrypick-test-data/{test_id}")
