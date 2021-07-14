#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from http import HTTPStatus
from typing import Any, Dict, List

import requests
from flask import abort
from flask import current_app as app
from flask import jsonify, make_response

from lighthouse.constants.cherrypick_test_data import (
    CPTD_STATUS_PENDING,
    FIELD_CRAWLER_RUN_ID,
)
from lighthouse.constants.error_messages import (
    ERROR_CRAWLER_INTERNAL_SERVER_ERROR,
)
from lighthouse.constants.fields import FIELD_CPTD_STATUS, FIELD_MONGO_ID

logger = logging.getLogger(__name__)


def insert_cherrypick_test_data_hook(runs: List[Dict[str, Any]]) -> None:
    for run in runs:
        run[FIELD_CPTD_STATUS] = CPTD_STATUS_PENDING


def inserted_cherrypick_test_data_hook(runs: List[Dict[str, Any]]) -> None:
    run_id = runs[0][FIELD_MONGO_ID]  # bulk inserting is disabled so there will only be one

    try:
        crawler_url = f"{app.config['CRAWLER_BASE_URL']}/cherrypick-test-data"
        logger.debug(crawler_url)
        response = requests.post(crawler_url, json={FIELD_CRAWLER_RUN_ID: str(run_id)})
        response.raise_for_status()  # Raise an exception if the status wasn't in the 200 range
    except Exception as e:
        abort(
            make_response(
                jsonify(
                    {
                        "_status": "ERR",
                        "_issues": [str(e)],
                        "_error": {
                            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                            "message": ERROR_CRAWLER_INTERNAL_SERVER_ERROR,
                        },
                    }
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        )
