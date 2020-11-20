import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore

from lighthouse.messages.broker import Broker  # type: ignore
from lighthouse.messages.message import Message  # type: ignore

from lighthouse.helpers.plate_events import (
    construct_event_message,
)

logger = logging.getLogger(__name__)

bp = Blueprint("plate-events", __name__)
CORS(bp)


@bp.route("/plate-events/create", methods=["GET"])
def create_plate_event() -> Tuple[Dict[str, Any], int]:
    try:
        # attempt to extract the event type
        event_type = request.args.get("event_type", "")
        if len(event_type) == 0:
            return {"errors": ["'event_type' is a required parameter"]}, HTTPStatus.BAD_REQUEST

        logger.info(f"Attempting to create an '{event_type}' event message")
        errors, message = construct_event_message(event_type, request.args)
        if len(errors) > 0:
            return {"errors": errors}, HTTPStatus.INTERNAL_SERVER_ERROR

        logger.info(f"Attempting to publish the '{event_type}' event message")
        broker = Broker()
        broker.connect()
        broker.publish(message)
        broker.close_connection()
        logger.info(f"Successfully published the '{event_type}' event message")
    except Exception as e:
        logger.exception(e)
        return {
            "errors": ["An unexpected error occurred attempting to publish a plate event message"]
        }, HTTPStatus.INTERNAL_SERVER_ERROR

    return ({}, HTTPStatus.OK)
