import logging
from http import HTTPStatus

from lighthouse.helpers.cherrytrack import (
    get_automation_system_run_info_from_cherrytrack,
    get_samples_from_source_plate_barcode_from_cherrytrack,
    get_wells_from_destination_barcode_from_cherrytrack,
)

logger = logging.getLogger(__name__)


class CherrytrackServiceMixin(object):
    def raise_error_from_response(self, response):
        json = response.json()
        if not (isinstance(json, dict)):
            raise Exception(f"Response from Cherrytrack is not a valid JSON: { json }")

        if json and ("errors" in json):
            raise Exception(f"Response from Cherrytrack is not OK: {','.join(json['errors'])}")
        else:
            raise Exception(f"Response from Cherrytrack is not OK: {response.text}")

    def get_run_info(self, run_id):
        logger.info(f"Getting automation system run info from Cherrytrack for run ID {run_id}")
        response = get_automation_system_run_info_from_cherrytrack(run_id)

        if response.status_code != HTTPStatus.OK:
            self.raise_error_from_response(response)

        return response.json()["data"]

    def get_samples_from_source_plates(self, source_barcode):
        logger.info(f"Getting samples info from Cherrytrack for source place barcode {source_barcode}")
        response = get_samples_from_source_plate_barcode_from_cherrytrack(source_barcode)
        if response.status_code != HTTPStatus.OK:
            self.raise_error_from_response(response)
        return response.json()["data"]["samples"]

    def filter_pickable_samples(self, sample):
        return sample["picked"]

    def get_wells_from_destination_plate(self, destination_barcode):
        logger.info(f"Getting samples info from Cherrytrack for destination place barcode '{destination_barcode}'")
        response = get_wells_from_destination_barcode_from_cherrytrack(destination_barcode)
        if response.status_code != HTTPStatus.OK:
            self.raise_error_from_response(response)

        return response.json()["data"]["wells"]
