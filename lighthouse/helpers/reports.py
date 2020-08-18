import logging
import math
import os
import pathlib
import re
import requests
import pandas as pd  # type: ignore

from datetime import datetime
from typing import Dict, List, Tuple
from http import HTTPStatus

from lighthouse.exceptions import ReportCreationError
from lighthouse.utils import pretty

from flask import current_app as app

logger = logging.getLogger(__name__)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent


def get_reports_details(filename: str = None) -> List[Dict[str, str]]:
    """Get the details of reports, including:
    - size
    - created timestamp
    - download URL - should point to where the files will be hosted from

    Keyword Arguments:
        filename {str} -- if filename is provided, only this report's details will be returned
        (default: {None})

    Returns:
        List[Dict[str, str]] -- list of report details
    """
    logger.debug("Getting reports' details")

    REPORTS_PATH = PROJECT_ROOT.joinpath(app.config["REPORTS_DIR"])

    if filename:
        reports = iter([filename])
    else:
        (_, _, files) = next(os.walk(REPORTS_PATH))

        # we only want files which match the report naming convention
        report_pattern = re.compile(r"^\d{6}_\d{4}_positives_with_locations.xlsx$")
        reports = filter(report_pattern.match, files)

    return [
        {
            "filename": filename,
            "size": get_file_size(REPORTS_PATH.joinpath(filename)),
            "created": datetime.fromtimestamp(
                os.path.getmtime(REPORTS_PATH.joinpath(filename))
            ).strftime("%c"),
            "download_url": f"{app.config['DOWNLOAD_REPORTS_URL']}/{filename}",
        }
        for filename in reports
    ]


def get_file_size(file_path: pathlib.PurePath) -> str:
    """Get the size of a file in a human friendly format.

    Arguments:
        file_path {pathlib.PurePath} -- path to the file in question

    Returns:
        str -- file size in human friendly format
    """
    size_in_bytes = os.path.getsize(file_path)

    return convert_size(size_in_bytes)


def convert_size(size_in_bytes: int) -> str:
    """Converts the size of a file (in bytes) to a human friendly format.

    Based on: https://stackoverflow.com/a/14822210

    Arguments:
        size_in_bytes {int} -- size of file in bytes

    Returns:
        str -- file size in human friendly format
    """
    if size_in_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)

    return f"{s} {size_name[i]}"


def get_new_report_name_and_path() -> Tuple[str, pathlib.PurePath]:
    """Get the name and path of a report which is being created.

    Returns:
        Tuple[str, pathlib.PurePath] -- filename and path of report being created
    """
    report_date = datetime.now().strftime("%y%m%d_%H%M")
    report_name = f"{report_date}_positives_with_locations.xlsx"
    REPORTS_PATH = PROJECT_ROOT.joinpath(app.config["REPORTS_DIR"])
    report_path = REPORTS_PATH.joinpath(report_name)

    return report_name, report_path


# Stip any leading zeros from the coordinate
# eg. A01 => A1
def unpad_coordinate(coordinate):
    return (
        re.sub(r"0(\d+)$", r"\1", coordinate)
        if (coordinate and isinstance(coordinate, str))
        else coordinate
    )


def delete_reports(filenames):
    """delete reports from the standard reports folder if they exist.

    Returns:
        Nothing.
    """
    for filename in filenames:
        full_path = f"{app.config['REPORTS_DIR']}/{filename}"
        if os.path.isfile(full_path):
            os.remove(full_path)


def map_labware_to_location(labware_barcodes):
    response = requests.post(
        f"http://{app.config['LABWHERE_URL']}/api/labwares/searches",
        json={"barcodes": labware_barcodes},
    )
    """
    Example record from labwhere:
    {'audits': '/api/labwares/GLA001024R/audits',
    'barcode': 'GLA001024R',
    'created_at': 'Tuesday May 26 2020 16:13',
    'location': {'audits': '/api/locations/lw-uk-biocentre-box-gsw--98-14813/audits',
                'barcode': 'lw-uk-biocentre-box-gsw--98-14813',
                'children': '/api/locations/lw-uk-biocentre-box-gsw--98-14813/children',
                'columns': 0,
                'container': True,
                'created_at': 'Thursday May  7 2020 11:29',
                'id': 14813,
                'labwares': '/api/locations/lw-uk-biocentre-box-gsw--98-14813/labwares',
                'location_type_id': 7,
                'name': 'UK Biocentre box GSW  98',
                'parent': '/api/locations/lw-glasgow-barcodes-14715',
                'parentage': 'Sanger / Ogilvie / Glasgow Barcodes',
                'rows': 0,
                'status': 'active',
                'updated_at': 'Thursday May  7 2020 11:29'},
    'updated_at': 'Tuesday May 26 2020 16:13'}
    """
    logger.debug(response)

    if response.status_code != HTTPStatus.OK:
        raise ReportCreationError("Response from labwhere is not OK")

    # create a plate_barcode to location_barcode mapping to join with samples
    # return none for samples where location barcode is not present
    labware_to_location_barcode = [
        {
            "plate_barcode": record["barcode"],
            "location_barcode": record["location"].get("barcode", ""),
        }
        for record in response.json()
    ]

    labware_to_location_barcode_df = pd.DataFrame.from_records(labware_to_location_barcode)
    logger.info(
        f"{len(labware_to_location_barcode_df.index)} locations for plate barcodes found"
    )
    pretty(logger, labware_to_location_barcode_df)

    return labware_to_location_barcode_df
