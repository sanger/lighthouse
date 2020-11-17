import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore

logger = logging.getLogger(__name__)

bp = Blueprint("plate-events", __name__)
CORS(bp)


@bp.route("/plate-events/create", methods=["GET"])
def create_plate_event() -> Tuple[Dict[str, Any], int]:
    try:
        barcode = request.args.get("barcode", "")
        event_type = request.args.get("event_type", "")
        if len(barcode) == 0 or len(event_type) == 0:
            return {
                "errors": ["GET request needs 'barcode' and 'event_type' in url"]
            }, HTTPStatus.BAD_REQUEST
        else:
            logger.info(
                f"Attempting to create a '{event_type}' event for plate with barcode '{barcode}'"
            )
    except Exception as e:
        logger.exception(e)
        return {
            "errors": [
                "An error occurred attempting to determine 'barcode' and 'event_type' from "
                "url parameters"
            ]
        }, HTTPStatus.INTERNAL_SERVER_ERROR

    # TODO - implement

    return ({}, HTTPStatus.OK)
