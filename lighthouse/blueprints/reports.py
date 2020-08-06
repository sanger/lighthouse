import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore

from lighthouse.helpers.reports import get_reports_details, delete_reports
from lighthouse.jobs.reports import create_report

import json

logger = logging.getLogger(__name__)

bp = Blueprint("reports", __name__)
CORS(bp)


@bp.route("/reports", methods=["GET"])
def get_reports() -> Tuple[Dict[str, Any], int]:
    logger.debug("Getting reports")
    try:
        return {"reports": get_reports_details()}, HTTPStatus.OK
    except Exception as e:
        logger.exception(e)

        return {"errors": [type(e).__name__]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/reports/new", methods=["POST"])
def create_report_endpoint():
    try:
        report_name = create_report()
        return {"reports": get_reports_details(report_name)}, HTTPStatus.CREATED
    except Exception as e:
        logger.exception(e)

        return {"errors": [type(e).__name__]}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/delete_reports", methods=["POST"])
def delete_reports_endpoint():
    """A Flask route which accepts a list of report filenames and then deletes them
    from the reports path. 
    This endpoint should be json and the body should be in
    the format {"data":"filenames":["file1.xlsx","file2.xlsx", ...]}
    This is a POST request but is a destructive action but this does not need to be
    delete as it is not a REST resource.
    Arguments:
        None
    Returns:
        {}, HTTPStatus
    """
    try:
        delete_reports(request.json["data"]["filenames"])
        return {}, HTTPStatus.OK
    except Exception as e:
        logger.exception(e)
        return {"errors": [type(e).__name__]}, HTTPStatus.INTERNAL_SERVER_ERROR
