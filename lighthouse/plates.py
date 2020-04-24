import logging
from http import HTTPStatus

from flask import Blueprint
from flask import current_app as app
from flask import request

from lighthouse.helpers import confirm_cente, get_cog_barcodes, get_samples

logger = logging.getLogger(__name__)
# from .exceptions import BarcodeNotFoundError, BarcodesMismatchError, TubesCountError
# from .helper import handle_error, parse_tube_rack_csv, send_request_to_sequencescape, wrangle_tubes

bp = Blueprint("plates", __name__)


@bp.route("/plates/new", methods=["POST"])
def create_plate_from_barcode():
    logger.debug("create_plate_from_barcode()")

    try:
        plate_barcode = request.get_json()["plate_barcode"]
        logger.info(f"Looking for samples for plate with barcode: {plate_barcode}")
    except KeyError as e:
        logger.exception(e)
        return ""

    try:
        # get samples for barcode
        samples = get_samples(plate_barcode)

        if len(samples) == 0:
            # do something cleverer here
            return "No samples for this barcode"

        # get COG barcodes for samples
        samples_with_cog = get_cog_barcodes(samples)
        # create body for POST to SS
        # send POST request to SS

    except Exception as e:
        logger.exception(e)

    return f""
