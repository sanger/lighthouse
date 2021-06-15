import requests
from flask import current_app as app


def get_automation_system_run_info_from_cherry_track(run_id: int) -> requests.Response:
    """Retrieve automation system run infomation from CherryTrack for the given run id

    Example record from CherryTrack:

    `  return {'id': 1, 'user_id': 'ab1', 'liquid_handler_serial_number': 'aLiquidHandlerSerialNumber'}`

    Args:
        run_id (int): The internal Mongo DB id of the automation system run

    Returns:
        requests.Response: the response from the request to CherryTrack.
    """
    # return requests.get(f"http://10.80.241.124:8000/automation-system-runs/{run_id}")
    return requests.get(f"{app.config['CHERRY_TRACK_URL']}/automation-system-runs/{run_id}")
