import requests
from flask import current_app as app

from lighthouse.helpers.cherrytrack import (
    get_automation_system_run_info_from_cherrytrack,
    get_samples_from_source_plate_barcode_from_cherrytrack,
)
import logging
from http import HTTPStatus

logger = logging.getLogger(__name__)


class ServiceCherrytrackMixin(object):
    def get_run_info(self, run_id):
        logger.info(f"Getting automation system run info from Cherrytrack for run ID {run_id}")
        response = get_automation_system_run_info_from_cherrytrack(run_id)

        if response.status_code != HTTPStatus.OK:
            raise Exception("Response from Cherrytrack is not OK")

        return response.json()["data"]

    def get_samples_from_source_plates(self, source_barcode):
        logger.info(f"Getting samples info from Cherrytrack for source place barcode {source_barcode}")
        response = get_samples_from_source_plate_barcode_from_cherrytrack(source_barcode)

        if response.status_code != HTTPStatus.OK:
            raise Exception("Response from Cherrytrack is not OK")

        return response.json()["data"]

    def filter_pickable_samples(self, sample):
        return not sample["picked"]
