import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore

from lighthouse.helpers.plates import add_cog_barcodes, create_post_body, get_samples, send_to_ss, get_positive_samples

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)
CORS(bp)

@bp.route("/plates/new", methods=["POST"])
def create_plate_from_barcode() -> Tuple[Dict[str, Any], int]:
    try:
        barcode = request.get_json()["barcode"]
        logger.info(f"Attempting to create a plate in SS from barcode: {barcode}")
    except (KeyError, TypeError) as e:
        logger.exception(e)
        return {"errors": ["POST request needs 'barcode' in body"]}, HTTPStatus.BAD_REQUEST

    try:
        # get samples for barcode
        samples = get_positive_samples(barcode)

        if not samples:
            return {"errors": ["No samples for this barcode: " + barcode]}, HTTPStatus.BAD_REQUEST

        # add COG barcodes to samples
        centre_prefix = add_cog_barcodes(samples)

        body = create_post_body(barcode, samples)

        response = send_to_ss(body)

        response_json = {
            "data": {
                "plate_barcode": samples[0]["plate_barcode"],
                "centre": centre_prefix,
                "number_of_positives": len(samples)
            }
        }

        # return the JSON and status code directly from SS (act as a proxy)
        return response_json, response.status_code
    except Exception as e:
        logger.exception(e)
        return {"errors": [type(e).__name__]}, HTTPStatus.INTERNAL_SERVER_ERROR
