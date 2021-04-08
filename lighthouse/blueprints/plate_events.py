import logging

from flask import Blueprint, request
from flask_cors import CORS

from lighthouse.constants.error_messages import (
    ERROR_MISSING_PARAMETERS,
    ERROR_PLATE_EVENT_PUBLISH,
    ERROR_UNEXPECTED_PLATE_EVENT_PUBLISH,
)
from lighthouse.helpers.events import get_routing_key
from lighthouse.helpers.plate_event_callbacks import fire_callbacks
from lighthouse.helpers.plate_events import construct_event_message
from lighthouse.helpers.requests import get_required_params
from lighthouse.helpers.responses import bad_request, internal_server_error, ok
from lighthouse.messages.broker import Broker
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("plate-events", __name__)
CORS(bp)


@bp.route("/plate-events/create", methods=["GET"])
def create_plate_event() -> FlaskResponse:
    """This endpoint attempts to publish a plate event message to the RabbitMQ broker.

    Returns:
        FlaskResponse: if successful, return an empty list of errors and an OK status; otherwise, a list of errors and
        the corresponding HTTP status code.
    """
    logger.info("Attempting to publish a plate event message")
    try:
        # we only ask for one parameter so get the first one of the returned tuple
        event_type = get_required_params(request, ("event_type",))[0]
    except Exception as e:
        logger.error(f"{ERROR_PLATE_EVENT_PUBLISH} {ERROR_MISSING_PARAMETERS}")
        logger.exception(e)

        return bad_request(str(e))

    try:
        logger.info(f"Attempting to publish an '{event_type}' plate event message")

        errors, message = construct_event_message(event_type, request.args)

        if len(errors) > 0 or message is None:
            logger.error(f"{ERROR_PLATE_EVENT_PUBLISH} error(s) constructing event message: " f"{errors}")
            # HERE
            # return internal_server_error(errors)
            return internal_server_error(errors)

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
                return ok(errors=[])
            else:
                logger.error("Failed to update LabWhere", messages)

                return internal_server_error(messages)
        except Exception:
            broker.close_connection()

            raise
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED_PLATE_EVENT_PUBLISH} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)
