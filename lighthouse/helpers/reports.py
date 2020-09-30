import logging
import math
import os
import pathlib
import re
import requests
import pandas as pd  # type: ignore

import pymysql

# we only need the create_engine method
# but that can't be mocked
# can't seem to mock it at the top because
# it is outside the app context
import sqlalchemy  # type: ignore

from datetime import datetime
from typing import Dict, List, Tuple
from http import HTTPStatus

from lighthouse.exceptions import ReportCreationError
from lighthouse.utils import pretty

from flask import current_app as app

from lighthouse.constants import (
    FIELD_SOURCE,
    FIELD_PLATE_BARCODE,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_RESULT,
    FIELD_DATE_TESTED,
    FIELD_COORDINATE,
    CT_VALUE_LIMIT,
    POSITIVE_SAMPLES_MONGODB_FILTER
)

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
    response = get_locations_from_labwhere(labware_barcodes)

    if response.status_code != HTTPStatus.OK:
        raise ReportCreationError("Response from LabWhere is not OK")

    # create a plate_barcode to location_barcode mapping to join with samples
    # return none for samples where location barcode is not present
    labware_to_location_barcode = [
        {
            FIELD_PLATE_BARCODE: record["barcode"],
            "location_barcode": str(record["location_barcode"] or ""),
        }
        for record in response.json()
    ]

    labware_to_location_barcode_df = pd.DataFrame.from_records(labware_to_location_barcode)
    logger.info(f"{len(labware_to_location_barcode_df.index)} locations for plate barcodes found")
    pretty(logger, labware_to_location_barcode_df)

    return labware_to_location_barcode_df


def get_locations_from_labwhere(labware_barcodes):
    """
    Example record from labwhere:
    { 'barcode': 'GLA001024R', 'location_barcode': 'lw-uk-biocentre-box-gsw--98-14813'}
    """

    return requests.post(
        f"http://{app.config['LABWHERE_URL']}/api/labwares_by_barcode",
        json={"barcodes": labware_barcodes},
    )

def get_cherrypicked_samples(root_sample_ids, plate_barcodes):
    # Find which samples have been cherrypicked using MLWH & Events warehouse
    # Returns dataframe with 1 column, 'Root Sample ID', containing Root Sample ID of those that have been cherrypicked
    # TODO: move into external method.
    root_sample_id_string = "'" + "','".join(root_sample_ids) + "'"
    plate_barcodes_string = "'" + "','".join(plate_barcodes) + "'"

    ml_wh_db = app.config["ML_WH_DB"]
    events_wh_db = app.config["EVENTS_WH_DB"]

    sql = (
        f"select mlwh_sample.description as `{FIELD_ROOT_SAMPLE_ID}`"
        f" FROM {app.config['ML_WH_DB']}.sample as mlwh_sample"
        f" JOIN {app.config['ML_WH_DB']}.stock_resource mlwh_stock_resource ON (mlwh_sample.id_sample_tmp = mlwh_stock_resource.id_sample_tmp)"
        f" JOIN {app.config['EVENTS_WH_DB']}.subjects mlwh_events_subjects ON (mlwh_events_subjects.friendly_name = sanger_sample_id)"
        f" JOIN {app.config['EVENTS_WH_DB']}.roles mlwh_events_roles ON (mlwh_events_roles.subject_id = mlwh_events_subjects.id)"
        f" JOIN {app.config['EVENTS_WH_DB']}.events mlwh_events_events ON (mlwh_events_roles.event_id = mlwh_events_events.id)"
        f" JOIN {app.config['EVENTS_WH_DB']}.event_types mlwh_events_event_types ON (mlwh_events_events.event_type_id = mlwh_events_event_types.id)"
        f" WHERE mlwh_sample.description IN ({root_sample_id_string})"
        f" AND mlwh_stock_resource.labware_human_barcode IN ({plate_barcodes_string})"
        " AND mlwh_events_event_types.key = 'cherrypick_layout_set'"
        " GROUP BY mlwh_sample.description"
    )

    try:
        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{app.config['MLWH_CONN_STRING']}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()
        frame = pd.read_sql(sql, db_connection)
        return frame
    except Exception as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        db_connection.close()


def get_all_positive_samples(samples):

    logger.debug("Getting all positive samples")
    # filtering using case insensitive regex to catch "Positive" and "positive"
    results = samples.find(
        filter = POSITIVE_SAMPLES_MONGODB_FILTER,
        projection = {
            "_id": False,
            FIELD_SOURCE: True,
            FIELD_PLATE_BARCODE: True,
            FIELD_ROOT_SAMPLE_ID: True,
            FIELD_RESULT: True,
            FIELD_DATE_TESTED: True,
            FIELD_COORDINATE: True,
        },
    )

    # converting to a dataframe to make it easy to join with data from labwhere
    positive_samples_df = pd.DataFrame.from_records(results)
    logger.info(f"{len(positive_samples_df.index)} positive samples")
    pretty(logger, positive_samples_df)

    # strip zeros out of the well coordinates
    positive_samples_df[FIELD_COORDINATE] = positive_samples_df[FIELD_COORDINATE].map(
        lambda coord: unpad_coordinate(coord)
    )

    # create 'plate and well' column for copy-pasting into Sequencescape submission, e.g. DN1234:A1
    positive_samples_df["plate and well"] = (
        positive_samples_df[FIELD_PLATE_BARCODE] + ":" + positive_samples_df[FIELD_COORDINATE]
    )

    return positive_samples_df


def add_cherrypicked_column(existing_dataframe):
    root_sample_ids = existing_dataframe[FIELD_ROOT_SAMPLE_ID].to_list()
    plate_barcodes = existing_dataframe["plate_barcode"].unique()

    cherrypicked_samples_df = get_cherrypicked_samples(root_sample_ids, plate_barcodes)
    cherrypicked_samples_df["LIMS submission"] = "Yes"

    existing_dataframe = existing_dataframe.merge(
        cherrypicked_samples_df, how="left", on=FIELD_ROOT_SAMPLE_ID
    )
    existing_dataframe = existing_dataframe.fillna({"LIMS submission": "No"})

    return existing_dataframe


def get_distinct_plate_barcodes(samples):

    logger.debug("Getting list of distinct plate barcodes")
    # for some reason we have some records (documents in mongo language) where the plate_barcode
    #   is empty so ignore those
    # TODO: abstract into new method
    distinct_plate_barcodes = samples.distinct(
        FIELD_PLATE_BARCODE, {FIELD_PLATE_BARCODE: {"$nin": ["", None]}}
    )
    logger.info(f"{len(distinct_plate_barcodes)} distinct barcodes")

    return distinct_plate_barcodes


def join_samples_declarations(positive_samples):

    samples_declarations = app.data.driver.db.samples_declarations

    # Latest declarations group by root_sample_id
    # Id is needed to control the group aggregation
    # Excel formatter required date without timezone
    declarations = samples_declarations.aggregate(
        [
            {"$sort": {"declared_at": -1}},
            {
                "$group": {
                    "_id": "$root_sample_id",
                    FIELD_ROOT_SAMPLE_ID: {"$first": "$root_sample_id"},
                    "Value In Sequencing": {"$first": "$value_in_sequencing"},
                    "Declared At": {
                        "$first": {
                            "$dateToString": {"date": "$declared_at", "format": "%Y-%m-%dT%H:%M:%S"}
                        }
                    },
                }
            },
            {"$unset": "_id"},
        ]
    )

    declarations_records = [record for record in declarations]

    if len(declarations_records) > 0:
        logger.debug("Joining declarations")
        declarations_frame = pd.DataFrame.from_records(declarations_records)
        results = positive_samples.merge(declarations_frame, how="left", on=FIELD_ROOT_SAMPLE_ID)

        # Give a default value of Unknown to any entry that does not have a
        # sample declaration
        results = results.fillna({"Value In Sequencing": "Unknown"})
        return results

    return positive_samples
