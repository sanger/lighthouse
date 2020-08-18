import logging
import time
from http import HTTPStatus

import pymysql
from sqlalchemy import create_engine # type: ignore

import pandas as pd  # type: ignore
import requests
from flask import current_app as app

from lighthouse import scheduler
from lighthouse.exceptions import ReportCreationError
from lighthouse.helpers.reports import (
    get_new_report_name_and_path, unpad_coordinate, map_labware_to_location
)
from lighthouse.utils import pretty

logger = logging.getLogger(__name__)

def create_report() -> str:
    """Creates a positve samples on site record using the samples collection and location
    information from labwhere.

    Returns:
        str -- filename of report created
    """
    logger.info("Creating positive samples report")
    start = time.time()

    # get samples collection
    samples = app.data.driver.db.samples
    samples_declarations = app.data.driver.db.samples_declarations

    logger.debug("Getting all positive samples")
    # filtering using case insensitive regex to catch "Positive" and "positive"
    results = samples.find(
        filter={"Result": {"$regex": "^positive", "$options": "i"}},
        projection={
            "_id": False,
            "source": True,
            "plate_barcode": True,
            "Root Sample ID": True,
            "Result": True,
            "Date Tested": True,
            "coordinate": True,
        },
    )

    # Latest declarations group by root_sample_id
    # Id is needed to control the group aggregation
    # Excel formatter required date without timezone
    declarations = samples_declarations.aggregate(
        [
            {"$sort": {"declared_at": -1}},
            {
                "$group": {
                    "_id": "$root_sample_id",
                    "Root Sample ID": {"$first": "$root_sample_id"},
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

    # converting to a dataframe to make it easy to join with data from labwhere
    positive_samples_df = pd.DataFrame.from_records(results)
    logger.info(f"{len(positive_samples_df.index)} positive samples")
    pretty(logger, positive_samples_df)

    # strip zeros out of the well coordinates
    positive_samples_df["coordinate"] = positive_samples_df["coordinate"].map(
        lambda coord: unpad_coordinate(coord)
    )
    # create 'plate and well' column for copy-pasting into Sequencescape submission, e.g. DN1234:A1
    positive_samples_df["plate and well"] = (
        positive_samples_df["plate_barcode"] + ":" + positive_samples_df["coordinate"]
    )

    logger.debug("Getting list of distinct plate barcodes")
    # for some reason we have some records (documents in mongo language) where the plate_barcode
    #   is empty so ignore those
    distinct_plate_barcodes = samples.distinct(
        "plate_barcode", {"plate_barcode": {"$nin": ["", None]}}
    )
    logger.info(f"{len(distinct_plate_barcodes)} distinct barcodes")

    logger.debug("Getting location barcodes from labwhere")
    labware_to_location_barcode_df = map_labware_to_location(distinct_plate_barcodes)

    logger.debug("Joining location data from labwhere")
    merged = positive_samples_df.merge(
        labware_to_location_barcode_df, how="left", on="plate_barcode"
    )

    declarations_records = [record for record in declarations]
    if len(declarations_records) > 0:
        logger.debug("Joining declarations")
        declarations_frame = pd.DataFrame.from_records(declarations_records)
        merged = merged.merge(declarations_frame, how="left", on="Root Sample ID")

        # Give a default value of Unknown to any entry that does not have a
        # sample declaration
        merged = merged.fillna({"Value In Sequencing": "Unknown"})

    pretty(logger, merged)

    report_name, report_path = get_new_report_name_and_path()

    logger.info(f"Writing results to {report_path}")

    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(report_path, engine="xlsxwriter")

    # Sheet2 contains all positive samples WITH location barcodes
    merged[merged.location_barcode.notnull()].to_excel(
        writer, sheet_name="POSITIVE SAMPLES WITH LOCATION", index=False
    )

    # Convert the dataframe to an XlsxWriter Excel object
    #  Sheet1 contains all positive samples with AND without location barcodes
    merged.to_excel(writer, sheet_name="ALL POSITIVE SAMPLES", index=False)

    # Close the Pandas Excel writer and output the Excel file
    writer.save()

    logger.info(f"Report creation complete in {round(time.time() - start, 2)}s")

    return report_name


def create_report_job():
    """Scheduler's job to create the report within the scheduler's app context.

    Returns:
        str -- filename of report created
    """
    logger.info("Starting create_report job")
    with scheduler.app.app_context():
        create_report()

def get_cherrypicked_samples(root_sample_ids):

    sql = ("select mlwh_sample.description as description"
                " FROM mlwarehouse.sample as mlwh_sample"
                " JOIN mlwh_events.subjects mlwh_events_subjects ON (mlwh_events_subjects.friendly_name = sanger_sample_id)"
                " JOIN mlwh_events.roles mlwh_events_roles ON (mlwh_events_roles.subject_id = mlwh_events_subjects.id)"
                " JOIN mlwh_events.events mlwh_events_events ON (mlwh_events_roles.event_id = mlwh_events_events.id)"
                " JOIN mlwh_events.event_types mlwh_events_event_types ON (mlwh_events_events.event_type_id = mlwh_events_event_types.id)"
                f" WHERE mlwh_sample.description IN ('{root_sample_ids}')"
                " AND mlwh_events_event_types.key = 'slf_cherrypicking'"
                " GROUP BY mlwh_sample.description")

    try:
        sql_engine = create_engine(f"mysql+pymysql://{app.config['MLWH_CONN_STRING']}", pool_recycle=3600)        
        db_connection = sql_engine.connect()
        frame = pd.read_sql(sql, db_connection)
        return frame
    except Exception as e:
        print("Error while connecting to MySQL", e)
        return None
    finally:
        db_connection.close()


