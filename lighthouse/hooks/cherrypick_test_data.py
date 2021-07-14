#  https://docs.python-eve.org/en/stable/features.html#database-event-hooks
import logging
from http import HTTPStatus
from typing import Any, Dict, List

from flask import abort, jsonify, make_response

from lighthouse.constants.cherrypick_test_data import CPTD_STATUS_PENDING
from lighthouse.constants.fields import FIELD_CPTD_STATUS

logger = logging.getLogger(__name__)


def insert_cherrypick_test_data_hook(runs: List[Dict[str, Any]]) -> None:
    for run in runs:
        run[FIELD_CPTD_STATUS] = CPTD_STATUS_PENDING


def inserted_cherrypick_test_data_hook(runs: List[Dict[str, Any]]) -> None:
    # TODO: Assume we only receive one run
    for run in runs:
        try:
            # TODO: pass the run through to Crawler for processing
            pass
        except Exception as e:
            abort(
                make_response(
                    jsonify(
                        {
                            "_status": "ERR",
                            "_issues": [],  # TODO: return errors from Crawler
                            "_error": {
                                "code": HTTPStatus.INTERNAL_SERVER_ERROR,
                                "message": "The run creation has failed.",
                            },
                        }
                    ),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )
