import requests
from flask import current_app as app


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
        return requests.get(f"{app.config['CHERRY_TRACK_URL']}/automation-system-runs/{run_id}").json()

    def get_samples_from_source_plates(self, source_plates):
        return None

    def filter_pickable_samples(self, samples):
        return []
