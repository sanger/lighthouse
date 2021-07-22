from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

bp = Blueprint("eve_routes", __name__)
CORS(bp)


def redirect_endpoint(base_url):
    # We need to include the rest of the URL from the request after the base
    redirect_url = base_url
    url_split = request.url.split(base_url)
    if len(url_split) > 1:
        redirect_url += url_split[1]

    return redirect(redirect_url, code=HTTPStatus.PERMANENT_REDIRECT)


@bp.route("/cherrypick-test-data", defaults={"path": ""}, methods=["GET", "POST"])
@bp.route("/cherrypick-test-data/<path:path>")
def cptd_redirects(path):
    return redirect_endpoint("/cherrypick-test-data")
