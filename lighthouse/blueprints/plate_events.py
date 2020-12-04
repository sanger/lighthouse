import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore

from lighthouse.messages.broker import Broker  # type: ignore
from lighthouse.helpers.plate_events import construct_event_message
from lighthouse.helpers.plate_event_callbacks import fire_callbacks
from lighthouse.helpers.events import get_routing_key


logger = logging.getLogger(__name__)

bp = Blueprint("plate-events", __name__)
CORS(bp)


@bp.route("/plate-events/create", methods=["GET"])
def create_plate_event() -> Tuple[Dict[str, Any], int]:
    try:
        event_type = request.args.get("event_type")
        if not event_type:
            logger.error(
                "Failed publishing plate event message: missing required 'event_type' parameter"
            )
            return {"errors": ["'event_type' is a required parameter"]}, HTTPStatus.BAD_REQUEST

        logger.info(f"Attempting to publish an '{event_type}' plate event message")
        logger.info("Attempting to construct the plate event message")
        errors, message = construct_event_message(event_type, request.args)
        if len(errors) > 0:
            logger.error(
                "Failed publishing plate event message: error(s) constructing event message: "
                f"{errors}"
            )
            return {"errors": errors}, HTTPStatus.INTERNAL_SERVER_ERROR

        # By this stage we know the event type is valid as we have been able to construct a message
        routing_key = get_routing_key(event_type)

        logger.info("Attempting to publish the constructed plate event message")
        broker = Broker()
        broker.connect()
        try:
            broker.publish(message, routing_key)
            broker.close_connection()
            logger.info(f"Successfully published a '{event_type}' plate event message")
            success, messages = fire_callbacks(message)
            if success:
                return ({"errors": []}, HTTPStatus.OK)
            else:
                logger.error("Failed to update labwhere", messages)
                return ({"errors": messages}, HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception:
            broker.close_connection()
            raise

    except Exception as e:
        logger.error("Failed publishing plate event message: an unexpected error occurred")
        logger.exception(e)
        return {
            "errors": ["An unexpected error occurred attempting to publish a plate event message"]
        }, HTTPStatus.INTERNAL_SERVER_ERROR
