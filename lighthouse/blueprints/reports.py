import logging

from flask import Blueprint, request
from flask_cors import CORS

from lighthouse.constants.error_messages import ERROR_UNEXPECTED
from lighthouse.helpers.reports import delete_reports, get_reports_details
from lighthouse.helpers.responses import created, internal_server_error, ok
from lighthouse.jobs.reports import create_report
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("reports", __name__)
CORS(bp)


@bp.get("/reports")
def get_reports() -> FlaskResponse:
    """Gets a list of all the available reports.

    Returns:
        FlaskResponse: list of report details and an HTTP status code.
    """
    logger.info("Getting reports")
    try:
        reports = get_reports_details()

        return ok(reports=reports)
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)


@bp.post("/reports/new")
def create_report_endpoint() -> FlaskResponse:
    """Creates a new report.

    Returns:
        FlaskResponse: details of the report just created or a list of errors with the corresponding HTTP status code.
    """
    logger.info("Creating a new report")
    try:
        report_name = create_report()

        report_details = get_reports_details(report_name)

        return created(reports=report_details)
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)


@bp.post("/delete_reports")
def delete_reports_endpoint() -> FlaskResponse:
    """A route which accepts a list of report filenames and then deletes them from the reports path.
    This endpoint should be JSON and the body should be in the format:

    `{"data":"filenames":["file1.xlsx","file2.xlsx", ...]}`

    This is a POST request but is a destructive action but this does not need to be delete as it is not a REST resource.

    Returns:
        FlaskResponse: empty response body for OK; otherwise details of any errors and the corresponding HTTP status
        code.
    """
    logger.info("Attempting to delete report(s)")
    try:
        delete_reports(request.get_json()["data"]["filenames"])

        return ok()
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)
