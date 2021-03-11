import logging

from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_cors import CORS

from lighthouse.constants.error_messages import (
    ERROR_CHERRYPICKED_CREATE,
    ERROR_CHERRYPICKED_FAILURE_RECORD,
    ERROR_MISSING_PARAMETERS,
    ERROR_SAMPLE_DATA_MISMATCH,
    ERROR_SAMPLE_DATA_MISSING,
    ERROR_SAMPLES_MISSING_UUIDS,
    ERROR_UNEXPECTED_CHERRYPICKING_CREATE,
    ERROR_UNEXPECTED_CHERRYPICKING_FAILURE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)
from lighthouse.constants.events import PLATE_EVENT_DESTINATION_FAILED
from lighthouse.constants.general import ARG_BARCODE, ARG_FAILURE_TYPE, ARG_ROBOT_SERIAL, ARG_USER_ID
from lighthouse.helpers.events import get_routing_key
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    add_controls_to_samples,
    check_matching_sample_numbers,
    construct_cherrypicking_plate_failed_message,
    create_cherrypicked_post_body,
    find_dart_source_samples_rows,
    find_samples,
    get_source_plates_for_samples,
    join_rows_with_samples,
    map_to_ss_columns,
    query_for_cherrypicked_samples,
    send_to_ss_heron_plates,
    update_mlwh_with_cog_uk_ids,
)
from lighthouse.helpers.requests import get_required_params
from lighthouse.helpers.responses import bad_request, internal_server_error, ok
from lighthouse.messages.broker import Broker
from lighthouse.types import FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("cherrypicked-plates", __name__)
CORS(bp)


@bp.route("/cherrypicked-plates/create", methods=["GET"])
def create_plate_from_barcode() -> FlaskResponse:  # noqa: C901
    """This endpoint attempts to create a plate in Sequencescape. The arguments provided extract data from the DART
    and mongo databases, add COG UK barcodes and then call Sequencescape to attempt to create a plate and samples.

    Returns:
        FlaskResponse: If the call to Sequencescape was made, this response acts as a proxy as it returns the response
        and HTTP status code which is received back. If any errors occur on the way, it returns with a list of errors
        and the corresponding HTTP code.
    """
    logger.info("Attempting to create a plate in Sequencescape")
    try:
        user_id, barcode, robot_serial_number = get_required_params(
            request, (ARG_USER_ID, ARG_BARCODE, ARG_ROBOT_SERIAL)
        )
    except Exception as e:
        logger.error(f"{ERROR_CHERRYPICKED_CREATE} {ERROR_MISSING_PARAMETERS}")
        logger.exception(e)

        return bad_request(str(e))

    try:
        dart_samples = find_dart_source_samples_rows(barcode)
        if len(dart_samples) == 0:
            msg = f"{ERROR_SAMPLE_DATA_MISSING} {barcode}"
            logger.error(msg)

            return internal_server_error(msg)

        mongo_samples = find_samples(query_for_cherrypicked_samples(dart_samples))

        if not mongo_samples:
            return bad_request(f"No samples for this barcode: {barcode}")

        if not check_matching_sample_numbers(dart_samples, mongo_samples):
            msg = f"{ERROR_SAMPLE_DATA_MISMATCH} {barcode}"
            logger.error(msg)

            return internal_server_error(msg)

        # add COG barcodes to samples
        try:
            centre_prefix = add_cog_barcodes(mongo_samples)
        except Exception as e:
            logger.exception(e)

            return bad_request(f"Failed to add COG barcodes to plate: {barcode}")

        samples = join_rows_with_samples(dart_samples, mongo_samples)

        all_samples = add_controls_to_samples(dart_samples, samples)

        mapped_samples = map_to_ss_columns(all_samples)

        source_plates = get_source_plates_for_samples(mongo_samples)

        if not source_plates:
            return bad_request(f"{ERROR_SAMPLES_MISSING_UUIDS} {barcode}")

        body = create_cherrypicked_post_body(user_id, barcode, mapped_samples, robot_serial_number, source_plates)

        response = send_to_ss_heron_plates(body)

        if response.ok:
            response_json = {
                "data": {
                    "plate_barcode": barcode,
                    "centre": centre_prefix,
                    "number_of_fit_to_pick": len(samples),
                }
            }

            try:
                update_mlwh_with_cog_uk_ids(mongo_samples)
            except Exception as e:
                logger.exception(e)

                return internal_server_error(ERROR_UPDATE_MLWH_WITH_COG_UK_IDS)
        else:
            response_json = response.json()

        # return the JSON and status code directly from Sequencescape (act as a proxy)
        return response_json, response.status_code
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED_CHERRYPICKING_CREATE} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)


@bp.route("/cherrypicked-plates/fail", methods=["GET"])
def fail_plate_from_barcode() -> FlaskResponse:
    """This endpoints attempts to publish an event to the event warehouse when a failure occurs when a destination plate
    is not created successfully.

    Returns:
        FlaskResponse: If the message is published successfully return with an OK otherwise return the error messages
        and the corresponding HTTP status code.
    """
    logger.info(f"Attempting to publish a '{PLATE_EVENT_DESTINATION_FAILED}' message")
    try:
        required_args = (ARG_USER_ID, ARG_BARCODE, ARG_ROBOT_SERIAL, ARG_FAILURE_TYPE)
        user_id, barcode, robot_serial_number, failure_type = get_required_params(request, required_args)
    except Exception as e:
        logger.error(f"{ERROR_CHERRYPICKED_FAILURE_RECORD} {ERROR_MISSING_PARAMETERS}")
        logger.exception(e)

        return bad_request(str(e))
    try:
        if failure_type not in app.config["BECKMAN_FAILURE_TYPES"]:
            logger.error(f"{ERROR_CHERRYPICKED_FAILURE_RECORD} unknown failure type")

            return bad_request(f"'{failure_type}' is not a known cherrypicked plate failure type")

        errors, message = construct_cherrypicking_plate_failed_message(
            barcode, user_id, robot_serial_number, failure_type
        )

        if message is None:
            logger.error(f"{ERROR_CHERRYPICKED_FAILURE_RECORD} error(s) constructing event message: {errors}")

            return internal_server_error(errors)

        routing_key = get_routing_key(PLATE_EVENT_DESTINATION_FAILED)

        logger.info("Attempting to publish the destination failed event message")
        broker = Broker()
        broker.connect()
        try:
            broker.publish(message, routing_key)
            broker.close_connection()
            logger.info(f"Successfully published a '{PLATE_EVENT_DESTINATION_FAILED}' message")

            return ok(errors=errors)

        except Exception:
            broker.close_connection()
            raise
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED_CHERRYPICKING_FAILURE} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)
