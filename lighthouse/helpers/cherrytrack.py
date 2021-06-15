import requests
from flask import current_app as app


def get_automation_system_run_info_from_cherrytrack(run_id: int) -> requests.Response:
    """Retrieve automation system run infomation from Cherrytrack for the given run id

    Example record from Cherrytrack:

    `return { 'data': {'id': 1, 'user_id': 'ab1', 'liquid_handler_serial_number': 'aLiquidHandlerSerialNumber'} }`

    Args:
        run_id (int): The internal Mongo DB id of the automation system run

    Returns:
        requests.Response: the response from the request to Cherrytrack.
    """
    # return requests.get(f"http://192.168.5.124:8000/automation-system-runs/{run_id}")
    return requests.get(f"{app.config['CHERRYTRACK_URL']}/automation-system-runs/{run_id}")


def get_samples_from_source_plate_barcode_from_cherrytrack(source_plate_barcode: str) -> requests.Response:
    """Retrieve samples infomation from Cherrytrack for the given source plate barcode

    Example record from Cherrytrack:

    `return {'data': [{'control': True, 'control_barcode': 'control_barcode', 'control_coordinate': 'control_coordinate', 'lab_id': 'lab_id', 'picked': True, 'rna_id': 'rna_id', 'robot_barcode': 'robot_barcode', 'run_id': 'run_id', 'sample_id': 'sample_id', 'source_barcode': 'aBarcode', 'source_coordinate': 'A1'}]}`

    Args:
        source_plate_barcode (string): The barcode of the source plate

    Returns:
        requests.Response: the response from the request to Cherrytrack.
    """
    # return requests.get(f"http://192.168.5.124:8000/source-plates/{source_plate_barcode}")
    return requests.get(f"{app.config['CHERRYTRACK_URL']}/source-plates/{source_plate_barcode}")
