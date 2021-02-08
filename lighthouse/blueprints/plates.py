import logging
from http import HTTPStatus
from typing import Any, Dict, Tuple

from flask import Blueprint, request
from flask_cors import CORS  # type: ignore
from lighthouse.constants import FIELD_PLATE_BARCODE
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    create_post_body,
    get_positive_samples,
    get_positive_samples_count,
    has_sample_data,
    send_to_ss,
    update_mlwh_with_cog_uk_ids,
)

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
        try:
            centre_prefix = add_cog_barcodes(samples)
        except (Exception) as e:
            logger.exception(e)
            return (
                {"errors": ["Failed to add COG barcodes to plate: " + barcode]},
                HTTPStatus.BAD_REQUEST,
            )

        body = create_post_body(barcode, samples)

        response = send_to_ss(body)

        if response.ok:
            response_json = {
                "data": {
                    "plate_barcode": samples[0][FIELD_PLATE_BARCODE],
                    "centre": centre_prefix,
                    "number_of_positives": len(samples),
                }
            }

            try:
                update_mlwh_with_cog_uk_ids(samples)
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


def format_plate(barcode: str) -> Dict[str, Any]:
    """Used by flask route /plates to format each plate
    Arguments:
        barcode
    Returns:
        {}, HTTPStatus
    """
    plate_map = has_sample_data(barcode)
    number_of_positives = get_positive_samples_count(barcode) if plate_map else None

    return {
        "plate_barcode": barcode,
        "plate_map": plate_map,
        "number_of_positives": number_of_positives,
    }


@bp.route("/plates", methods=["GET"])
def find_plate_from_barcode() -> Tuple[Dict[str, Any], int]:
    """A Flask route which returns information about a list of plates as
    specified in the barcodes parameters.
    For example:
    GET http://host:port/plates?barcodes[]=123&barcodes[]=456&barcodes[]=789
    To fetch data for 123,456 and 789
    This endpoint responds with json and the body is in the format
    {"plates":[{"barcode":"12345","plate_map":true,"number_of_positives":0}]}
    Arguments:
        None
    Returns:
        {}, HTTPStatus
    """
    barcodes = request.args.getlist("barcodes[]")
    try:
        plates = [format_plate(barcode) for barcode in barcodes]
        return {"plates": plates}, HTTPStatus.OK
    except Exception as e:
        logger.exception(e)
        # We don't use str(e) here to fetch the exception summary, because
        # the exceptions we're most likely to see here aren't end-user-friendly
        exception_type = type(e).__name__
        return {"errors": [f"Failed to lookup plates: {exception_type}"]}, HTTPStatus.INTERNAL_SERVER_ERROR
