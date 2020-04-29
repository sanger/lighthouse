import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request

from lighthouse.helpers import add_cog_barcodes, create_post_body, get_samples, send_to_ss

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)


@bp.route("/plates/new", methods=["POST"])
def create_plate_from_barcode() -> Tuple[Dict[str, Any], int]:
    logger.debug("create_plate_from_barcode()")

    try:
        plate_barcode = request.get_json()["plate_barcode"]
        logger.info(f"Looking for samples for plate with barcode: {plate_barcode}")
    except KeyError as e:
        logger.exception(e)
        return {"errors": ["POST request needs 'plate_barcode' in body"]}, HTTPStatus.BAD_REQUEST

    try:
        # get samples for barcode
        samples = get_samples(plate_barcode)

        if not samples:
            # do something cleverer here
            return {"errors": ["No samples for this barcode"]}, HTTPStatus.OK

        # add COG barcodes to samples
        add_cog_barcodes(samples)

        body = create_post_body(plate_barcode, samples)

        response = send_to_ss(body)

        return response.json(), response.status_code
    except Exception as e:
        logger.exception(e)
        return {"errors": [e]}, HTTPStatus.INTERNAL_SERVER_ERROR
