import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore
from flask import current_app as app


logger = logging.getLogger(__name__)

bp = Blueprint("beckman", __name__)
CORS(bp)


@bp.route("/beckman/robots", methods=["GET"])
def get_robots() -> Tuple[Dict[str, Any], int]:
    try:
        logger.info("Fetching information for Beckman robots")
        robots_config = app.config.get("BECKMAN_ROBOTS", None)
        if robots_config is None:
            logger.error("Failed fetching Beckman robot information: no config found")
            return {
                "errors": ["No information exists for any Beckman robots"],
                "robots": [],
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        robots = [{"name": v["name"], "serial_number": k} for k, v in robots_config.items()]
        logger.info("Successfully fetched Beckman robot information")
        return {"errors": [], "robots": robots}, HTTPStatus.OK
    except Exception as e:
        logger.error("Failed fetching information for Beckman robots")
        logger.exception(e)
        return {
            "errors": ["An unexpected error occurred fetching Beckman robot information"],
            "robots": [],
        }, HTTPStatus.INTERNAL_SERVER_ERROR
