import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint
from flask_cors import CORS  # type: ignore

from lighthouse.helpers.reports import get_reports_details
from lighthouse.jobs.reports import create_report

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
