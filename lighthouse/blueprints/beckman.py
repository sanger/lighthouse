import logging

from flask import Blueprint
from flask import current_app as app
from flask_cors import CORS

from lighthouse.constants.error_messages import ERROR_FAILURE_TYPE_CONFIG, ERROR_ROBOT_CONFIG, ERROR_UNEXPECTED
from lighthouse.helpers.responses import internal_server_error, ok
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("beckman", __name__)
CORS(bp)


@bp.route("/beckman/robots", methods=["GET"])
def get_robots() -> FlaskResponse:
    """Find information about the Beckman robots. Currently, this information lives in config.

    Returns:
        FlaskResponse: the config for the robots configures with the corresponding HTTP status code.
    """
    logger.info("Fetching Beckman robot information")
    try:
        robots_config = app.config.get("BECKMAN_ROBOTS")
        if robots_config is None:
            logger.error(f"{ERROR_ROBOT_CONFIG} no config found")

            return internal_server_error("No information exists for any Beckman robots", robots=[])

        robots = [{"name": v["name"], "serial_number": k} for k, v in robots_config.items()]

        logger.info("Successfully fetched Beckman robot information")

        return ok(errors=[], robots=robots)
    except Exception as e:
        logger.error(f"{ERROR_ROBOT_CONFIG} {type(e).__name__}")
        logger.exception(e)

        return internal_server_error(f"{ERROR_UNEXPECTED} while fetching Beckman robot information", robots=[])


@bp.route("/beckman/failure-types", methods=["GET"])
def get_failure_types() -> FlaskResponse:
    """Get a list of the Beckman failure types.

    Returns:
        FlaskResponse: a list of failure types if found or a list of errors with the corresponding HTTP status code.
    """
    logger.info("Fetching Beckman failure type information")
    try:
        failure_types_config = app.config.get("BECKMAN_FAILURE_TYPES")

        if failure_types_config is None or not isinstance(failure_types_config, dict):
            logger.error(f"{ERROR_FAILURE_TYPE_CONFIG} no config found")

            return internal_server_error("No information exists for any Beckman failure types", failure_types=[])

        failure_types = [{"type": k, "description": v} for k, v in failure_types_config.items()]

        logger.info("Successfully fetched Beckman failure type information")

        return ok(errors=[], failure_types=failure_types)
    except Exception as e:
        logger.error(f"{ERROR_FAILURE_TYPE_CONFIG} {type(e).__name__}")
        logger.exception(e)

        return internal_server_error(f"{ERROR_UNEXPECTED} while fetching Beckman failure type information", robots=[])
