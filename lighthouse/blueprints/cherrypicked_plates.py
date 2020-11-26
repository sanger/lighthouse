import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore
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
    get_source_plate_id_mappings,
)

logger = logging.getLogger(__name__)

bp = Blueprint("cherrypicked-plates", __name__)
CORS(bp)


@bp.route("/cherrypicked-plates/create", methods=["GET"])
def create_plate_from_barcode() -> Tuple[Dict[str, Any], int]:

    try:
        user_id = request.args.get("user_id", "UNKNOWN")

        barcode = request.args.get("barcode", "")
        if len(barcode) == 0:
            return missing_barcode_url_error()

        robot_serial_number = request.args.get("robot", "")
        if len(robot_serial_number) == 0:
            return missing_robot_number_url_error()

        logger.info(f"Attempting to create a plate in SS from barcode: {barcode}")
    except (KeyError, TypeError) as e:
        logger.exception(e)
        return invalid_url_error()

    try:
        dart_samples = find_dart_source_samples_rows(barcode)
        if len(dart_samples) == 0:
            msg = "Failed to find sample data in DART for plate barcode: " + barcode
            logger.error(msg)
            return ({"errors": [msg]}, HTTPStatus.INTERNAL_SERVER_ERROR)

        mongo_samples = find_samples(query_for_cherrypicked_samples(dart_samples))

        if not mongo_samples:
            return {"errors": ["No samples for this barcode: " + barcode]}, HTTPStatus.BAD_REQUEST

        try:
            check_matching_sample_numbers(dart_samples, mongo_samples)
        except (Exception) as e:
            logger.exception(e)
            return (
                {
                    "errors": [
                        "Mismatch in destination and source sample data for plate: " + barcode
                    ]
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        # add COG barcodes to samples
        try:
            centre_prefix = add_cog_barcodes(mongo_samples)
        except (Exception) as e:
            logger.exception(e)
            return (
                {"errors": ["Failed to add COG barcodes to plate: " + barcode]},
                HTTPStatus.BAD_REQUEST,
            )

        samples = join_rows_with_samples(dart_samples, mongo_samples)

        all_samples = add_controls_to_samples(dart_samples, samples)

        mapped_samples = map_to_ss_columns(all_samples)

        plate_id_mappings = get_source_plate_id_mappings(mongo_samples)

        if not plate_id_mappings:
            return {
                "errors": ["No source plate UUIDs for source plates of plate: " + barcode]
            }, HTTPStatus.BAD_REQUEST

        body = create_cherrypicked_post_body(
            user_id, barcode, mapped_samples, robot_serial_number, plate_id_mappings
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
                return (
                    {
                        "errors": [
                            (
                                "Failed to update MLWH with COG UK ids. The samples should have "
                                "been successfully inserted into Sequencescape."
                            )
                        ]
                    },
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
        else:
            response_json = response.json()

        # return the JSON and status code directly from SS (act as a proxy)
        return response_json, response.status_code
    except Exception as e:
        logger.exception(e)
        return {"errors": [type(e).__name__]}, HTTPStatus.INTERNAL_SERVER_ERROR


def invalid_url_error():
    return {"errors": ["Missing/invalid query parameters in url"]}, HTTPStatus.BAD_REQUEST


def missing_barcode_url_error():
    return {"errors": ["GET request needs 'barcode' in url"]}, HTTPStatus.BAD_REQUEST


def missing_robot_number_url_error():
    return {"errors": ["GET request needs 'robot' in url"]}, HTTPStatus.BAD_REQUEST
