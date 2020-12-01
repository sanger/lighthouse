"""Connect to labwhere to update or retrieve location information

This file contains the following functions:

  * get_locations_from_labwhere - Make an API call to labwhere
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

