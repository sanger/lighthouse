"""Connect to LabWhere to update or retrieve location information

This file contains the following functions:

  * get_locations_from_labwhere - Make an API call to LabWhere to get locations
  * set_locations_in_labwhere - Make an API call to LabWhere to update locations
"""

from typing import List

import requests
from flask import current_app as app


def get_locations_from_labwhere(labware_barcodes: List[str]) -> requests.Response:
    """Retrieve locations from LabWhere for the given labware barcodes

    Example record from LabWhere:

    `{ 'barcode': 'GLA001024R', 'location_barcode': 'lw-uk-biocentre-box-gsw--98-14813'}`

    Args:
        labware_barcodes (List[str]): The list of labware barcodes to search for in LabWhere.

    Returns:
        requests.Response: the response from the request to LabWhere.
    """
    return requests.post(
        f"{app.config['LABWHERE_URL']}/api/labwares_by_barcode?known=true",
        json={"barcodes": labware_barcodes},
    )


def set_locations_in_labwhere(
    labware_barcodes: List[str], location_barcode: str, user_barcode: str
) -> requests.Response:
    """Record a scan event in LabWhere for labware_barcodes

    Note: The LabWhere API currently identifies users by their swipecard, however currently we only have access to the
    login when generating plate events. We can use the robot as a user instead, this has the advantage that:
      1. Its not open to user error
      2. There is reduced risk that the robot is not registered in LabWhere
      3. We wont ascribe unloading the robot to the same user who loaded it
      4. It will not require changes to LabWhere or additional user id validation

    Arguments:
        labware_barcodes {List[str]} - The source plate barcodes
        location_barcode {str} - The barcode of the locations to which the labwares have been
                                 transferred.
        user_barcode {str} - The swipecard/barcode for the user or robot associated with the scan.


    Returns:
        {requests.Response} -- The LabWhere response object
    """
    return requests.post(
        f"{app.config['LABWHERE_URL']}/api/scans",
        json={
            "scan": {
                "user_code": user_barcode,
                "labware_barcodes": "\n".join(labware_barcodes),
                "location_barcode": location_barcode,
            }
        },
    )
