"""Connect to labwhere to update or retrieve location information

This file contains the following functions:

  * get_locations_from_labwhere - Make an API call to labwhere to get locations
  * set_locations_in_labwhere - Make an API call to labwhere to update locations
"""

import requests
from flask import current_app as app
from typing import List


def get_locations_from_labwhere(labware_barcodes):
    """Retrieve a location from labwhere
    Example record from labwhere:
    { 'barcode': 'GLA001024R', 'location_barcode': 'lw-uk-biocentre-box-gsw--98-14813'}
    """

    return requests.post(
        f"http://{app.config['LABWHERE_URL']}/api/labwares_by_barcode",
        json={"barcodes": labware_barcodes},
    )


def set_locations_in_labwhere(
    labware_barcodes: List[str], location_barcode: str, user_barcode: str
):
    """Record a scan event in labwhere for labware_barcodes

    Note: The labwhere API currently identifies users by their swipecard, however
    currently we only have access to the login when generating plate events.
    We can use the robot as a user instead, this has the advantage that:
      1) Its not open to user error
      2) There is reduced risk that the robot is not registered in labwhere
      3) We wont ascribe unloading the robot to the same user who loaded it
      4) It will not require changes to labwhere or additional user id validation

    Arguments:
        labware_barcodes {List[str]} - The source plate barcodes
        location_barcode {str} - The barcode of the locations to which the labwares have been transferred.
        user_barcode {str} - The swipecard/barcode for the user or robot associated with the scan.


    Returns:
        {requests.Response} -- The labwhere response object
    """

    return requests.post(
        f"http://{app.config['LABWHERE_URL']}/api/scans",
        json={
            "scan": {
                "user_code": user_barcode,
                "labware_barcodes": "\n".join(labware_barcodes),
                "location_barcode": location_barcode,
            }
        },
    )
