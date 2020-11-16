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
    check_unmatched_sample_data,
    add_controls_to_samples,
    query_for_cherrypicked_samples,
    send_to_ss,
    update_mlwh_with_cog_uk_ids,
)

logger = logging.getLogger(__name__)

bp = Blueprint("cherrypicked-plates", __name__)
CORS(bp)


@bp.route("/cherrypicked-plates/create", methods=["POST"])
def create_plate_from_barcode() -> Tuple[Dict[str, Any], int]:
    try:
        barcode = request.get_json()["barcode"]
        logger.info(f"Attempting to create a plate in SS from barcode: {barcode}")
    except (KeyError, TypeError) as e:
        logger.exception(e)
        return {"errors": ["POST request needs 'barcode' in body"]}, HTTPStatus.BAD_REQUEST

    try:
        dart_samples = find_dart_source_samples_rows(barcode)
        if len(dart_samples) == 0:
            msg = "Failed to find sample data in DART for plate barcode: " + barcode
            logger.error(msg)
            return ({"errors": [msg]}, HTTPStatus.INTERNAL_SERVER_ERROR)

        mongo_samples = find_samples(query_for_cherrypicked_samples(dart_samples))

        if not mongo_samples:
            return {"errors": ["No samples for this barcode: " + barcode]}, HTTPStatus.BAD_REQUEST

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

        try:
            check_unmatched_sample_data(samples)
        except (Exception) as e:
            logger.exception(e)
            return (
                {
                    "errors": [
                        "Failed to find matching data in Mongo for DART samples on plate: "
                        + barcode
                    ]
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        all_samples = add_controls_to_samples(dart_samples, samples)

        mapped_samples = map_to_ss_columns(all_samples)

        body = create_cherrypicked_post_body(barcode, mapped_samples)

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
