import logging
import math
import os
import pathlib
import re
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Dict, List, Optional, Tuple

import pandas as pd

# we only need the create_engine method
# but that can't be mocked
# can't seem to mock it at the top because
# it is outside the app context
import sqlalchemy
from flask import current_app as app
from pandas import DataFrame
from pymongo.collection import Collection

from lighthouse.constants.fields import (
    FIELD_COORDINATE,
    FIELD_DATE_TESTED,
    FIELD_FILTERED_POSITIVE,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
)
from lighthouse.exceptions import ReportCreationError
from lighthouse.helpers.labwhere import get_locations_from_labwhere
from lighthouse.sql_queries import SQL_MLWH_GET_CP_SAMPLES

logger = logging.getLogger(__name__)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent


def get_reports_details(filename: Optional[str] = None) -> List[Dict[str, str]]:
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
        report_pattern = re.compile(r"^\d{6}_\d{4}_(positives|fit_to_pick)_with_locations.xlsx$")
        reports = filter(report_pattern.match, files)

    return [
        {
            "filename": filename,
            "size": __get_file_size(REPORTS_PATH.joinpath(filename)),
            "created": datetime.fromtimestamp(os.path.getmtime(REPORTS_PATH.joinpath(filename))).strftime("%c"),
            "download_url": f"{app.config['DOWNLOAD_REPORTS_URL']}/{filename}",
        }
        for filename in reports
    ]


def get_new_report_name_and_path() -> Tuple[str, pathlib.PurePath]:
    """Get the name and path of a report which is being created.

    Returns:
        Tuple[str, pathlib.PurePath] -- filename and path of report being created
    """
    report_date = datetime.now().strftime("%y%m%d_%H%M")
    report_name = f"{report_date}_fit_to_pick_with_locations.xlsx"
    REPORTS_PATH = PROJECT_ROOT.joinpath(app.config["REPORTS_DIR"])
    report_path = REPORTS_PATH.joinpath(report_name)

    return report_name, report_path


# Strip any leading zeros from the coordinate
# eg. A01 => A1
def unpad_coordinate(coordinate):
    return re.sub(r"0(\d+)$", r"\1", coordinate) if (coordinate and isinstance(coordinate, str)) else coordinate


def delete_reports(filenames: List[str]) -> None:
    """Delete reports from the standard reports folder if they exist."""
    for filename in filenames:
        full_path = f"{app.config['REPORTS_DIR']}/{filename}"
        if os.path.isfile(full_path):
            os.remove(full_path)


def map_labware_to_location(labware_barcodes: List[str]) -> DataFrame:
    logger.info(f"Getting locations from LabWhere for {len(labware_barcodes)} barcodes")
    response = get_locations_from_labwhere(labware_barcodes)

    if response.status_code != HTTPStatus.OK:
        raise ReportCreationError("Response from LabWhere is not OK")

    # create a plate_barcode to location_barcode mapping to join with samples; return None for samples where location
    #   barcode is not present
    labware_to_location_barcode = [
        {
            FIELD_PLATE_BARCODE: record["barcode"],
            "location_barcode": str(record["location_barcode"] or ""),
        }
        for record in response.json()
    ]

    labware_to_location_barcode_df = pd.DataFrame.from_records(labware_to_location_barcode)

    logger.info(f"{len(labware_to_location_barcode_df.index)} locations for plate barcodes found")

    return labware_to_location_barcode_df


def get_cherrypicked_samples(root_sample_ids, plate_barcodes, chunk_size=50000):
    # Find which samples have been cherrypicked using MLWH & Events warehouse
    # Returns dataframe with 4 columns: those needed to uniquely identify the sample
    # resulting dataframe only contains those samples that have been cherrypicked
    # (= those that have an entry for the relevant event type in the event warehouse)
    # TODO: move into external method.

    try:
        # Create an empty DataFrame to merge into
        concat_frame = pd.DataFrame()

        chunk_root_sample_ids = [
            root_sample_ids[x : (x + chunk_size)] for x in range(0, len(root_sample_ids), chunk_size)  # noqa: E203
        ]

        mlwh_db = app.config["MLWH_DB"]

        sql_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{app.config['WAREHOUSES_RO_CONN_STRING']}/{mlwh_db}", pool_recycle=3600
        )
        db_connection = sql_engine.connect()

        for chunk_root_sample_id in chunk_root_sample_ids:
            params = {
                "root_sample_ids": tuple(chunk_root_sample_id),
                "plate_barcodes": tuple(plate_barcodes),
            }

            cherrypicked_frame = pd.read_sql(SQL_MLWH_GET_CP_SAMPLES, db_connection, params=params)

            # drop_duplicates is needed because the same 'root sample id' could pop up in two
            # different batches, and then it would retrieve the same rows for that root sample id
            # twice do reset_index after dropping duplicates to make sure the rows are numbered in
            # a way that makes sense
            concat_frame = concat_frame.append(cherrypicked_frame).drop_duplicates().reset_index(drop=True)

        return concat_frame
    except Exception as e:
        logger.error("Error while connecting to MySQL")
        logger.exception(e)
        return None
    finally:
        if db_connection is not None:
            logger.debug("Closing mlwh connection")
            db_connection.close()


def get_fit_to_pick_samples(samples_collection: Collection) -> DataFrame:
    """Get all the samples (documents) from mongo which meet the fit to pick rules and are from a specific date.

    Args:
        samples_collection (Collection): the samples collection.

    Returns:
        DataFrame: a pandas DataFrame with the fit to pick samples.
    """
    logger.debug("Getting all fit to pick samples from a specific date")

    # The projection defines which fields are present in the documents from the output of the mongo
    # query
    projection = {
        "_id": False,
        FIELD_SOURCE: True,
        FIELD_PLATE_BARCODE: True,
        FIELD_ROOT_SAMPLE_ID: True,
        FIELD_RESULT: True,
        FIELD_DATE_TESTED: True,
        FIELD_COORDINATE: True,
    }

    # Stage for mongo aggregation pipeline
    STAGE_MATCH_FILTERED_POSITIVE = {
        "$match": {
            # 1. We are only interested filtered positive samples
            FIELD_FILTERED_POSITIVE: True,
            # 2. We are only interested in documents which have a valid date
            FIELD_DATE_TESTED: {"$exists": True, "$nin": [None, ""]},
        }
    }

    # The pipeline defines stages which execute in sequence
    pipeline: List[Dict] = [
        # 1. First run the positive match stage
        STAGE_MATCH_FILTERED_POSITIVE,
        # 2. We only want documents which have valid dates that we can compare against
        {"$match": {FIELD_DATE_TESTED: {"$type": "date", "$gte": report_query_window_start()}}},
        # 3. Define which fields to have in the output documents
        {"$project": projection},
    ]

    # Perform an aggregation using the defined pipeline - this will run through the pipeline
    # "stages" in sequence
    results = samples_collection.aggregate(pipeline)

    # converting to a dataframe to make it easy to join with data from LabWhere
    fit_to_pick_samples_df = pd.DataFrame.from_records(results)

    logger.info(f"{len(fit_to_pick_samples_df.index)} fit to pick samples")

    # strip zeros out of the well coordinates
    fit_to_pick_samples_df[FIELD_COORDINATE] = fit_to_pick_samples_df[FIELD_COORDINATE].map(
        lambda coord: unpad_coordinate(coord)
    )

    # create 'plate and well' column for copy-pasting into Sequencescape submission, e.g. DN1234:A1
    fit_to_pick_samples_df["plate and well"] = (
        fit_to_pick_samples_df[FIELD_PLATE_BARCODE] + ":" + fit_to_pick_samples_df[FIELD_COORDINATE]
    )

    return fit_to_pick_samples_df


def add_cherrypicked_column(existing_dataframe):
    root_sample_ids = existing_dataframe[FIELD_ROOT_SAMPLE_ID].to_list()
    plate_barcodes = existing_dataframe["plate_barcode"].unique()

    cherrypicked_samples_df = get_cherrypicked_samples(root_sample_ids, plate_barcodes)
    cherrypicked_samples_df["LIMS submission"] = "Yes"

    logger.info(f"{len(cherrypicked_samples_df.index)} cherrypicked samples")

    # The result value in the phenotype in MLWH.sample is all lowercase,
    # because it is converted in create_post_body in helpers/plates.py,
    # whereas in the original data in MongoDB and MLWH.lighthouse_sample it is capitalised
    existing_dataframe["Result_lower"] = existing_dataframe["Result"].str.lower()

    existing_dataframe = existing_dataframe.merge(
        cherrypicked_samples_df,
        how="left",
        on=[FIELD_ROOT_SAMPLE_ID, FIELD_PLATE_BARCODE, "Result_lower", FIELD_COORDINATE],
    )
    # Fill any empty cells for the column with 'No' (those that do not have cherrypicking events)
    existing_dataframe = existing_dataframe.fillna({"LIMS submission": "No"})

    # remove the extra column we merged on as no longer needed
    existing_dataframe = existing_dataframe.drop(columns=["Result_lower"])

    return existing_dataframe


def get_distinct_plate_barcodes(samples_collection: Collection) -> List[str]:

    logger.debug("Getting list of distinct plate barcodes")

    # We have some records (documents in mongo language) where the plate_barcode is empty so ignore those
    # TODO: abstract into new method
    distinct_plate_barcodes: List[str] = samples_collection.distinct(
        FIELD_PLATE_BARCODE, {FIELD_PLATE_BARCODE: {"$nin": ["", None]}}
    )

    logger.info(f"{len(distinct_plate_barcodes)} distinct barcodes")

    return distinct_plate_barcodes


def report_query_window_start() -> datetime:
    """Return the start date for the report window.
    Returns:
        datetime: start date for the report window
    """
    window_size = app.config["REPORT_WINDOW_SIZE"]
    logger.debug(f"Current report window size: {window_size} days")

    start = datetime.now() + timedelta(days=-window_size)
    logger.info(f"Report starting from: {start.strftime('%d/%m/%Y')}")

    return datetime(year=start.year, month=start.month, day=start.day)


# Private, not explicitly tested methods


def __get_file_size(file_path: pathlib.PurePath) -> str:
    """Get the size of a file in a human friendly format.

    Arguments:
        file_path {pathlib.PurePath} -- path to the file in question

    Returns:
        str -- file size in human friendly format
    """
    size_in_bytes = os.path.getsize(file_path)

    return __convert_size(size_in_bytes)


def __convert_size(size_in_bytes: int) -> str:
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
