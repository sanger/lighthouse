import logging
from http import HTTPStatus

from flask import Blueprint, request
from flask_cors import CORS

from lighthouse.constants.error_messages import (
    ERROR_ADD_COG_BARCODES,
    ERROR_PLATES_CREATE,
    ERROR_UNEXPECTED_PLATES_CREATE,
    ERROR_UPDATE_MLWH_WITH_COG_UK_IDS,
)
from lighthouse.constants.general import ARG_EXCLUDE
from lighthouse.constants.fields import FIELD_PLATE_BARCODE
from lighthouse.helpers.general import get_fit_to_pick_samples_and_counts
from lighthouse.helpers.plates import (
    add_cog_barcodes,
    create_post_body,
    format_plate,
    send_to_ss_heron_plates,
    update_mlwh_with_cog_uk_ids,
)
from lighthouse.helpers.responses import bad_request, internal_server_error, ok
from lighthouse.types import FlaskResponse
from lighthouse.utils import pretty

logger = logging.getLogger(__name__)

bp = Blueprint("plates", __name__)
CORS(bp)


@bp.post("/plates/new")
def create_plate_from_barcode() -> FlaskResponse:
    """This endpoint attempts to create a plate in Sequencescape.

    Returns:
        FlaskResponse: the endpoints acts as proxy and returns the response and status code received from Sequencescape.
    """
    logger.info("Attempting to create a plate in Sequencescape")

    barcode = None
    if (request_json := request.get_json()) is not None:
        barcode = request_json.get("barcode")

    if request_json is None or barcode is None:
        return bad_request("POST request needs 'barcode' in body")

    try:
        # get samples for barcode
        (fit_to_pick_samples, count_fit_to_pick_samples, _, _, _) = get_fit_to_pick_samples_and_counts(barcode)

        if not fit_to_pick_samples:
            return bad_request(f"No fit to pick samples for this barcode: {barcode}")

        # add COG barcodes to samples
        try:
            centre_prefix = add_cog_barcodes(fit_to_pick_samples)
        except Exception as e:
            msg = f"{ERROR_PLATES_CREATE} {ERROR_ADD_COG_BARCODES} {barcode}"
            logger.error(msg)
            logger.exception(e)

            return bad_request(msg)

        body = create_post_body(barcode, fit_to_pick_samples)

        response = send_to_ss_heron_plates(body)

        if response.status_code == HTTPStatus.CREATED:
            response_json = {
                "data": {
                    "plate_barcode": fit_to_pick_samples[0][FIELD_PLATE_BARCODE],
                    "centre": centre_prefix,
                    "count_fit_to_pick_samples": count_fit_to_pick_samples,
                }
            }

            try:
                update_mlwh_with_cog_uk_ids(fit_to_pick_samples)
            except Exception as e:
                logger.error(ERROR_UPDATE_MLWH_WITH_COG_UK_IDS)
                logger.exception(e)

                return internal_server_error(ERROR_UPDATE_MLWH_WITH_COG_UK_IDS)
        else:
            response_json = response.json()

        # return the JSON and status code directly from Sequencescape (act as a proxy)
        return response_json, response.status_code
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED_PLATES_CREATE} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)


@bp.get("/plates")
def find_plate_from_barcode() -> FlaskResponse:
    """A route which returns information about a list of comma separated plates as specified
    in the 'barcodes' parameters. Default fields can be excluded from the response using the url
    param '_exclude'.

    For example:
    To fetch data for the plates with barcodes '123' and '456' and exclude field 'picked_samples':

    `GET /plates?barcodes=123,456,789&_exclude=picked_samples`

    `{"plates":
        [
            {
                "plate_barcode": "123",
                "has_plate_map": true,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
                "count_filtered_positive": 2,
                "count_fit_to_pick_samples": 2,
            },
            {
                "plate_barcode": "456",
                "has_plate_map": false,
                "count_must_sequence": 0,
                "count_preferentially_sequence": 0,
                "count_filtered_positive": 4,
                "count_fit_to_pick_samples": 4,
            },
        ]
    }`

    Returns:
        FlaskResponse: the response body and HTTP status code
    """
    logger.info("Finding plate from barcode")
    try:
        barcodes_arg = request.args.get("barcodes")
        barcodes_list = barcodes_arg.split(",") if barcodes_arg else []

        if len(barcodes_list) == 0:
            return bad_request("Please include a barcode list")

        exclude_props_arg = request.args.get(ARG_EXCLUDE)
        exclude_props = exclude_props_arg.split(",") if exclude_props_arg else []

        logger.debug(f"Barcodes to look for: {barcodes_arg}")
        plates = [format_plate(barcode, exclude_props=exclude_props) for barcode in barcodes_list]

        pretty(logger, plates)

        return ok(plates=plates)
    except Exception as e:
        logger.exception(e)
        # We don't use str(e) here to fetch the exception summary, because the exceptions we're most likely to see here
        #   aren't end-user-friendly
        return internal_server_error(f"Failed to lookup plates: {type(e).__name__}")
