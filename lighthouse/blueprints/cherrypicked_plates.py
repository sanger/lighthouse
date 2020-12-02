import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore
from flask import current_app as app
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    create_cherrypicked_post_body,
    find_dart_source_samples_rows,
    find_samples,
    join_rows_with_samples,
    map_to_ss_columns,
    check_matching_sample_numbers,
    add_controls_to_samples,
    query_for_cherrypicked_samples,
    send_to_ss,
    update_mlwh_with_cog_uk_ids,
    get_source_plates_for_samples,
    construct_cherrypicking_plate_failed_message,
)
from lighthouse.messages.broker import Broker  # type:ignore
from lighthouse.helpers.events import get_routing_key
from lighthouse.constants import PLATE_EVENT_DESTINATION_FAILED

logger = logging.getLogger(__name__)

bp = Blueprint("cherrypicked-plates", __name__)
CORS(bp)


# TODO - reduce method length/complexity
@bp.route("/cherrypicked-plates/create", methods=["GET"])
def create_plate_from_barcode() -> Tuple[Dict[str, Any], int]:

    try:
        user_id = request.args.get("user_id", "")
        if len(user_id) == 0:
            return bad_request_response_with_error("GET request needs 'user_id' in url")

        barcode = request.args.get("barcode", "")
        if len(barcode) == 0:
            return bad_request_response_with_error("GET request needs 'barcode' in url")

        robot_serial_number = request.args.get("robot", "")
        if len(robot_serial_number) == 0:
            return bad_request_response_with_error("GET request needs 'robot' in url")

        logger.info(f"Attempting to create a plate in SS from barcode: {barcode}")
    except (KeyError, TypeError) as e:
        logger.exception(e)
        return bad_request_response_with_error("Missing/invalid query parameters in url")

    try:
        dart_samples = find_dart_source_samples_rows(barcode)
        if len(dart_samples) == 0:
            msg = "Failed to find sample data in DART for plate barcode: " + barcode
            logger.error(msg)
            return internal_server_error_response_with_error(msg)

        mongo_samples = find_samples(query_for_cherrypicked_samples(dart_samples))

        if not mongo_samples:
            return bad_request_response_with_error("No samples for this barcode: " + barcode)

        if not check_matching_sample_numbers(dart_samples, mongo_samples):
            msg = f"Mismatch in destination and source sample data for plate '{barcode}'"
            logger.error(msg)
            return internal_server_error_response_with_error(msg)

        # add COG barcodes to samples
        try:
            centre_prefix = add_cog_barcodes(mongo_samples)
        except (Exception) as e:
            logger.exception(e)
            return bad_request_response_with_error(
                "Failed to add COG barcodes to plate: " + barcode
            )

        samples = join_rows_with_samples(dart_samples, mongo_samples)

        all_samples = add_controls_to_samples(dart_samples, samples)

        mapped_samples = map_to_ss_columns(all_samples)

        source_plates = get_source_plates_for_samples(mongo_samples)

        if not source_plates:
            return bad_request_response_with_error(
                "No source plate UUIDs for source plates of plate: " + barcode
            )

        body = create_cherrypicked_post_body(
            user_id, barcode, mapped_samples, robot_serial_number, source_plates
        )

        response = send_to_ss(body)

        if response.ok:
            response_json = {
                "data": {
                    "plate_barcode": barcode,
                    "centre": centre_prefix,
                    "number_of_positives": len(samples),
                }
            }

            try:
                update_mlwh_with_cog_uk_ids(mongo_samples)
            except (Exception) as e:
                logger.exception(e)
                return internal_server_error_response_with_error(
                    "Failed to update MLWH with COG UK ids. The samples should have "
                    "been successfully inserted into Sequencescape."
                )
        else:
            response_json = response.json()

        # return the JSON and status code directly from SS (act as a proxy)
        return response_json, response.status_code
    except Exception as e:
        logger.exception(e)
        return internal_server_error_response_with_error(type(e).__name__)


@bp.route("/cherrypicked-plates/fail", methods=["GET"])
def fail_plate_from_barcode() -> Tuple[Dict[str, Any], int]:
    try:
        barcode = request.args.get("barcode", "")
        user_id = request.args.get("user_id", "")
        robot_serial_number = request.args.get("robot", "")
        failure_type = request.args.get("failure_type", "")
        logger.info(f"Attempting to publish a '{PLATE_EVENT_DESTINATION_FAILED}' message")
        if any(len(x) == 0 for x in [barcode, user_id, robot_serial_number, failure_type]):
            logger.error("Failed recording cherrypicking plate failure: missing required inputs")
            return bad_request_response_with_error(
                "'barcode', 'user_id', 'robot' and 'failure_type' "
                "are required to record a cherrypicked plate failure"
            )

        if failure_type not in list(app.config["BECKMAN_FAILURE_TYPES"].keys()):
            logger.error("Failed recording cherrypicking plate failure: unknown failure type")
            return bad_request_response_with_error(
                f"'{failure_type}' is not a known cherrypicked plate failure type"
            )

        errors, message = construct_cherrypicking_plate_failed_message(
            barcode, user_id, robot_serial_number, failure_type
        )
        if len(errors) > 0:
            logger.error(
                "Failed recording cherrypicking plate failure: "
                f"error(s) constructing event message: {errors}"
            )
            return {"errors": errors}, HTTPStatus.INTERNAL_SERVER_ERROR

        routing_key = get_routing_key(PLATE_EVENT_DESTINATION_FAILED)

        logger.info("Attempting to publish the destination failed event message")
        broker = Broker()
        broker.connect()
        try:
            broker.publish(message, routing_key)
            broker.close_connection()
            logger.info(f"Successfully published a '{PLATE_EVENT_DESTINATION_FAILED}' message")
            return {"errors": []}, HTTPStatus.OK
        except Exception:
            broker.close_connection()
            raise
    except Exception as e:
        logger.error("Failed recording cherrypicking plate failure: an unexpected error occurred")
        logger.exception(e)
        return {
            "errors": [
                "An unexpected error occurred attempting to record cherrypicking plate failure"
            ]
        }, HTTPStatus.INTERNAL_SERVER_ERROR


def bad_request_response_with_error(error):
    return {"errors": [error]}, HTTPStatus.BAD_REQUEST


def internal_server_error_response_with_error(error):
    return {"errors": [error]}, HTTPStatus.INTERNAL_SERVER_ERROR
