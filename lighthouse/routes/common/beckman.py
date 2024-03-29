import logging

from lighthouse.classes.beckman import Beckman
from lighthouse.constants.error_messages import ERROR_UNEXPECTED
from lighthouse.helpers.responses import internal_server_error, ok
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)


def get_robots() -> FlaskResponse:
    """Find information about the Beckman robots. Currently, this information lives in config.

    Note: This is the existing implementation, currently used for the v1 endpoint.

    Returns:
        FlaskResponse: the config for the robots configures with the corresponding HTTP status code.
    """
    logger.info("Fetching Beckman robot information")
    try:
        robots = Beckman.get_robots()

        return ok(errors=[], robots=robots)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(f"{ERROR_UNEXPECTED} while fetching Beckman robot information", robots=[])


def get_failure_types() -> FlaskResponse:
    """Get a list of the Beckman failure types.

    Note: This is the existing implementation, currently used for the v1 endpoint.

    Returns:
        FlaskResponse: a list of failure types if found or a list of errors with the corresponding HTTP status code.
    """
    logger.info("Fetching Beckman failure type information")
    try:
        failure_types = Beckman.get_failure_types()

        return ok(errors=[], failure_types=failure_types)
    except Exception as e:
        logger.exception(e)

        return internal_server_error(
            f"{ERROR_UNEXPECTED} while fetching Beckman failure type information", failure_types=[]
        )
