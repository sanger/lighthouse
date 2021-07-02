import requests
from flask import current_app as app


def get_automation_system_run_info_from_cherrytrack(run_id: int) -> requests.Response:
    """Retrieve automation system run infomation from Cherrytrack for the given run id

    Example record from Cherrytrack:

    `return { 'data': {'id': 1, 'user_id': 'u', 'liquid_handler_serial_number': 'aLiquidHandlerSerialNumber'} }`

    Args:
        run_id (int): The internal Mongo DB id of the automation system run

    Returns:
        requests.Response: the response from the request to Cherrytrack.
    """
    return requests.get(f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}")


def get_samples_from_source_plate_barcode_from_cherrytrack(source_plate_barcode: str) -> requests.Response:
    """Retrieve samples infomation from Cherrytrack for the given source plate barcode

    Example record from Cherrytrack:

    `return `

    Args:
        source_plate_barcode (string): The barcode of the source plate

    Returns:
        requests.Response: the response from the request to Cherrytrack.
    """
    return requests.get(f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_plate_barcode}")


def get_wells_from_destination_barcode_from_cherrytrack(destination_plate_barcode: str) -> requests.Response:
    return requests.get(f"{app.config['CHERRYTRACK_URL']}/destination-plates/{destination_plate_barcode}")
