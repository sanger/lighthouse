import requests
from flask import current_app as app

from lighthouse.helpers.cherry_tracker import get_automation_system_run_info_from_cherry_track
import logging
from http import HTTPStatus

logger = logging.getLogger(__name__)


class ServiceCherryTrackerMixin(object):
    def get_run_info(self, run_id):
        """Retrieve automation system run infomation from CherryTrack for the given run id

        Example record from CherryTrack:

        `  return {'id': 1, 'user_id': 'ab1', 'liquid_handler_serial_number': 'aLiquidHandlerSerialNumber'}`

        Args:
            run_id (int): The internal Mongo DB id of the automation system run

        Returns:
            requests.Response: the response from the request to CherryTrack.
        """

        logger.info(f"Getting automation system run info from CherryTracker for run ID {run_id}")
        response = get_automation_system_run_info_from_cherry_track(run_id)

        if response.status_code != HTTPStatus.OK:
            raise Exception("Response from CherryTracker is not OK")

        return response.json()

    def get_samples_from_source_plates(self, run_id, barcode):
        return []

    def filter_pickable_samples(self, samples):
        return []
