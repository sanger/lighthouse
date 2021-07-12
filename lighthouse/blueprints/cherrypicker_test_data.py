import logging
from datetime import datetime, timezone

from flask import Blueprint, request
from flask_cors import CORS

from lighthouse.constants.general import ARG_ADD_TO_DART, ARG_PLATE_SPECS
from lighthouse.helpers.requests import get_required_params_from_json_body
from lighthouse.helpers.responses import bad_request, internal_server_error, ok
from lighthouse.types import EndpointParamsException, FlaskResponse

logger = logging.getLogger(__name__)

bp = Blueprint("cherrypicker-test-data", __name__)
CORS(bp)


@bp.post("/cherrypicker-test-data")
def generate_test_data() -> FlaskResponse:
    """Collect parameters for test plate data, add them to Mongo DB and call Crawler to generate the test data and
    insert it into the databases. The body of the request should be JSON with the following keys and corresponding
    values:

    `{ "plate_specs": "[[2, 48], [5, 96]]", "add_to_dart": true }`

    Returns:
        FlaskResponse -- A JSON response with one of the following status codes / formats:

    Status code 201 (Created) -- The test data was generated correctly and Mongo DB was updated with the barcode
    metadata:

    ```
    {
        "run_id": "0123456789ab0123456789ab",
        "timestamp": "2012-03-04T05:06:07.890123+00:00"
    }
    ```

    Status code 400 (Bad Request) -- The parameters listed for the body above were not populated or were invalid format:

    ```
    {
        "errors": [
            "Body key for 'plate_specs' was missing.",
            "Body key for 'add_to_dart' was missing."
        ],
        "timestamp": "2012-03-04T05:06:07.890123+00:00"
    }
    ```

    Status code 500 (Internal Server Error) -- There was a problem generating test data:

    ```
    {
        "errors": [ "There must be between 1 and 200 plates in a request." ],
        "timestamp": "2012-03-04T05:06:07.890123+00:00"
    }
    ```
    """
    logger.info("Started generating cherrypicker test data.")

    timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

    # Get the parameters from the JSON body
    try:
        add_to_dart, plate_specs = get_required_params_from_json_body(
            request.get_json(), (ARG_ADD_TO_DART, ARG_PLATE_SPECS), (bool, str)
        )
    except EndpointParamsException as e:
        logger.exception(e)
        return bad_request(str(e), timestamp=timestamp)

    logger.debug(add_to_dart)

    # Mock out two responses as a stub
    # TODO: Implement the correct behaviour here
    if add_to_dart:
        return ok(run_id="0123456789ab0123456789ab", timestamp=timestamp)
    else:
        return internal_server_error("There must be between 1 and 200 plates in a request.", timestamp=timestamp)
