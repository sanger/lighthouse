import logging
from http import HTTPStatus

from flask import current_app as app
from flask import request

from lighthouse.constants.config import SS_FILTER_FIT_TO_PICK, SS_PLATE_TYPE_DEFAULT
from lighthouse.constants.error_messages import ERROR_UNEXPECTED_PLATES_CREATE
from lighthouse.constants.fields import FIELD_PLATE_BARCODE
from lighthouse.constants.general import ARG_EXCLUDE, ARG_TYPE, ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE
from lighthouse.helpers.cherrytrack import (
    get_samples_from_source_plate_barcode_from_cherrytrack,
    get_wells_from_destination_barcode_from_cherrytrack,
)
from lighthouse.helpers.general import get_fit_to_pick_samples_and_counts
from lighthouse.helpers.mongo import get_all_samples_for_source_plate, get_source_plate_uuid
from lighthouse.helpers.plates import (
    centre_prefixes_for_samples,
    create_post_body,
    format_plate,
    send_to_ss_heron_plates,
)
from lighthouse.helpers.responses import bad_request, internal_server_error, ok
from lighthouse.types import FlaskResponse
from lighthouse.utils import pretty

logger = logging.getLogger(__name__)


def create_plate_from_barcode() -> FlaskResponse:
    """This endpoint attempts to create a plate in Sequencescape.

    Note: This is the existing implementation, currently used for the v1 endpoint.

    Returns:
        FlaskResponse: the endpoints acts as proxy and returns the response and status code received from Sequencescape.
    """
    logger.info("Attempting to create a plate in Sequencescape")

    barcode = None
    if (request_json := request.get_json()) is not None:
        barcode = request_json.get("barcode")
        plate_type = request_json.get("type")

    if request_json is None or barcode is None:
        return bad_request("POST request needs 'barcode' in body")

    if plate_type is None:
        plate_type = SS_PLATE_TYPE_DEFAULT

    plate_configs = app.config["SS_PLATE_CONFIG"]
    if plate_type not in plate_configs.keys():
        return bad_request(f"POST request 'type' must be from the list: {', '.join(plate_configs.keys())}")

    try:
        plate_config = plate_configs[plate_type]
        if plate_config[SS_FILTER_FIT_TO_PICK]:
            return _create_fit_to_pick_plate_from_barcode(barcode, plate_config)
        else:
            return _create_plate_from_barcode(barcode, plate_config)
    except Exception as e:
        msg = f"{ERROR_UNEXPECTED_PLATES_CREATE} ({type(e).__name__})"
        logger.error(msg)
        logger.exception(e)

        return internal_server_error(msg)


def _create_fit_to_pick_plate_from_barcode(barcode: str, plate_config: dict) -> FlaskResponse:
    # get samples for barcode
    (fit_to_pick_samples, count_fit_to_pick_samples, _, _, _) = get_fit_to_pick_samples_and_counts(barcode)

    if not fit_to_pick_samples:
        return bad_request(f"No fit to pick samples for this barcode: {barcode}")

    body = create_post_body(barcode, plate_config, fit_to_pick_samples)

    response = send_to_ss_heron_plates(body)

    if response.status_code == HTTPStatus.CREATED:
        return {
            "data": {
                "plate_barcode": fit_to_pick_samples[0][FIELD_PLATE_BARCODE],
                "centre": centre_prefixes_for_samples(fit_to_pick_samples)[0],
                "count_fit_to_pick_samples": count_fit_to_pick_samples,
            }
        }, response.status_code
    else:
        # return the JSON and status code directly from Sequencescape (act as a proxy)
        return response.json(), response.status_code


def _create_plate_from_barcode(barcode: str, plate_config: dict) -> FlaskResponse:
    plate_uuid = get_source_plate_uuid(barcode)
    if plate_uuid is None:
        return bad_request(f"No plate exists for barcode: {barcode}")

    samples = get_all_samples_for_source_plate(plate_uuid)
    if not samples:
        return bad_request(f"No samples found on plate with barcode: {barcode}")

    body = create_post_body(barcode, plate_config, samples)

    response = send_to_ss_heron_plates(body)

    if response.status_code == HTTPStatus.CREATED:
        return {
            "data": {
                "plate_barcode": samples[0][FIELD_PLATE_BARCODE],
                "centre": centre_prefixes_for_samples(samples)[0],
                "count_samples": len(samples),
            }
        }, response.status_code
    else:
        # return the JSON and status code directly from Sequencescape (act as a proxy)
        return response.json(), response.status_code


def find_plate_from_barcode() -> FlaskResponse:
    """A route which returns information about a list of comma separated plates as specified
    in the 'barcodes' parameters. Default fields can be excluded from the response using the url
    param '_exclude'.

    Note: This is the existing implementation, currently used for the v1 endpoint.

    ### Source plate example
    To fetch data for the source plates with barcodes '123' and '456' and exclude field 'picked_samples' from the
    output:

    #### Query:
    ```
    GET /plates?barcodes=123,456&_exclude=picked_samples
    ```

    #### Response:
    ```json
    {"plates":
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
    }
    ```

    ### Destination plate example
    To fetch data for the destination plates with barcodes 'destination_123' and 'destination_456':

    #### Query:
    ```
    GET /plates?barcodes=destination_123,destination_456&_type=destination
    ```

    #### Response:
    ```json
    {"plates":
        [
            {
                "plate_barcode": "destination_123",
                "plate_exists": true,
            },
            {
                "plate_barcode": "destination_456",
                "plate_exists": false,
            },
        ]
    }
    ```

    Returns:
        FlaskResponse: the response body and HTTP status code
    """
    logger.info("Finding plate from barcode")
    try:
        barcodes_arg = request.args.get("barcodes")
        barcodes_list = barcodes_arg.split(",") if barcodes_arg else []

        assert len(barcodes_list) > 0, "Include a list of barcodes separated by commas (,) in the request"

        plate_type = request.args.get(ARG_TYPE, ARG_TYPE_SOURCE)
        assert plate_type in (
            ARG_TYPE_SOURCE,
            ARG_TYPE_DESTINATION,
        ), f"Plate type needs to be either '{ARG_TYPE_SOURCE}' or '{ARG_TYPE_DESTINATION}'"

        exclude_props_arg = request.args.get(ARG_EXCLUDE)
        exclude_props = exclude_props_arg.split(",") if exclude_props_arg else []

        logger.debug(f"{plate_type} plate(s) barcodes to look for: {barcodes_arg}")

        plates = [
            format_plate(barcode, exclude_props=exclude_props, plate_type=plate_type) for barcode in barcodes_list
        ]

        pretty(logger, plates)

        return ok(plates=plates)
    except AssertionError as e:
        return bad_request(str(e))
    except Exception as e:
        logger.exception(e)
        # We don't use str(e) here to fetch the exception summary, because the exceptions we're most likely to see here
        #   aren't end-user-friendly
        return internal_server_error(f"Failed to lookup plates: {type(e).__name__}")


def find_cherrytrack_plate_from_barcode() -> FlaskResponse:
    logger.info("Finding cherry track plate from barcode")
    try:
        barcode = request.args.get("barcode") or ""

        assert len(barcode) > 0, "Include a barcode in the request"

        plate_type = request.args.get(ARG_TYPE) or ""

        logger.debug(f"{plate_type} plate barcode to look for: {barcode}")

        if plate_type == ARG_TYPE_SOURCE:
            response = get_samples_from_source_plate_barcode_from_cherrytrack(barcode)
        elif plate_type == ARG_TYPE_DESTINATION:
            response = get_wells_from_destination_barcode_from_cherrytrack(barcode)
        else:
            raise AssertionError(f"Plate type needs to be either '{ARG_TYPE_SOURCE}' or '{ARG_TYPE_DESTINATION}'")

        response_json = response.json()

        if response_json.get("errors") is not None:
            return internal_server_error(response_json.get("errors"))

        return ok(plate=response_json)
    except AssertionError as e:
        return bad_request(str(e))
    except Exception as e:
        logger.exception(e)
        return internal_server_error(f"Failed to lookup plate: {str(e)}")
