#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from http import HTTPStatus
from typing import Any, Dict, List

import requests
from flask import abort
from flask import current_app as app
from flask import json, jsonify, make_response
from requests.models import HTTPError

from lighthouse.constants.cherrypick_test_data import FIELD_CRAWLER_RUN_ID
from lighthouse.constants.error_messages import ERROR_CRAWLER_HTTP_ERROR
from lighthouse.constants.fields import FIELD_MONGO_ID

logger = logging.getLogger(__name__)


def inserted_cherrypick_test_data_hook(runs: List[Dict[str, Any]]) -> None:
    run_id = str(
        runs[0][FIELD_MONGO_ID]  # bulk inserting is disabled in the Eve domain settings, so there will only be one run
    )

    try:
        crawler_url = f"{app.config['CRAWLER_BASE_URL']}/v1/cherrypick-test-data"
        logger.info(f"Calling Crawler's generate data endpoint with run ID '{run_id}'")
        response = requests.post(crawler_url, json={FIELD_CRAWLER_RUN_ID: run_id})
        response.raise_for_status()  # Raise an exception if the status wasn't in the 200 range
    except HTTPError as error:
        errors_string = get_httperror_message(error)
        logger.error(f"Crawler gave error(s): {errors_string}")
        abort(
            make_response(
                jsonify(
                    {
                        "_status": "ERR",
                        "_error": {
                            "code": error.response.status_code,
                            "message": f"{ERROR_CRAWLER_HTTP_ERROR}: {errors_string}",
                        },
                    }
                ),
                error.response.status_code,
            )
        )
    except Exception as error:
        logger.exception(error)
        abort(
            make_response(
                jsonify(
                    {
                        "_status": "ERR",
                        "_error": {
                            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                            "message": str(error),
                        },
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        )


def get_httperror_message(error):
    try:
        response_json = error.response.json()
    except:
        return str(error)

    if isinstance(response_json, dict) and "errors" in response_json:
        return json.dumps(response_json["errors"])
    else:
        return str(error)
