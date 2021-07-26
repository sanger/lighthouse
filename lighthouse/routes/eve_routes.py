from http import HTTPStatus

from flask import Blueprint, redirect, request
from flask_cors import CORS

bp = Blueprint("eve_routes", __name__)
CORS(bp)


# Eve endpoints can only be configured to respond on a single versioned endpoint. We need to continue to support the
# endpoints served at the root of the server while also being able to serve on other versions of the API. This blueprint
# should be registered with the app multiple times such that it uses a url_prefix for the expected versions of the API.
# See the setup_routes method in the root __init__.py file. As endpoints defined below are reached nested under the
# version number specified in the url_prefix, this blueprint effectively removes the version number from the URL by
# generating a redirect response. The client is redirected to the equivalent endpoint at the server root where Eve is
# listening and picks up the request for a final response.


def redirect_endpoint(base_url):
    # We need to include the rest of the URL from the request after the base So if the requested URL is
    # https://lighthouse.sanger.ac.uk/v1/endpoint/some_ID?filter=a_filter the base_url passed in would just be
    # "/endpoint" and we need to retain everything after that base_url in the URL. We would want to construct a redirect
    # that goes to /endpoint/some_ID?filter=a_filter without the /v1 part of the request. So we split the request's URL
    # on the base_url provided and use everything after the first element of the split to form a new path to redirect
    # to.
    redirect_url = base_url
    url_split = request.url.split(base_url)
    if len(url_split) > 1:
        redirect_url += base_url.join(url_split[1:])

    return redirect(redirect_url, code=HTTPStatus.PERMANENT_REDIRECT)


@bp.route("/cherrypick-test-data", defaults={"path": ""}, methods=["GET", "POST"])
@bp.route("/cherrypick-test-data/<path:path>")
def cherrypick_test_data_redirects(path):
    return redirect_endpoint("/cherrypick-test-data")


@bp.route("/events", defaults={"path": ""}, methods=["GET", "POST"])
@bp.route("/events/<path:path>")
def events_redirects(path):
    return redirect_endpoint("/events")


@bp.route("/imports", defaults={"path": ""})
@bp.route("/imports/<path:path>")
def imports_redirects(path):
    return redirect_endpoint("/imports")


@bp.route("/priority_samples", defaults={"path": ""}, methods=["GET", "POST"])
@bp.route("/priority_samples/<path:path>", methods=["GET", "PATCH", "PUT"])
def priority_samples_redirects(path):
    return redirect_endpoint("/priority_samples")
