import logging
import time
from http import HTTPStatus

import pandas as pd  # type: ignore
import requests
from flask import current_app as app

from lighthouse import scheduler
from lighthouse.exceptions import ReportCreationError
from lighthouse.helpers.reports import (
    get_new_report_name_and_path, 
    unpad_coordinate, 
    map_labware_to_location, 
    get_cherrypicked_samples,
    get_all_positive_samples,
    add_cherrypicked_column,
    get_distinct_plate_barcodes
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
    # TODO: abstract into new methods
    samples = app.data.driver.db.samples
    samples_declarations = app.data.driver.db.samples_declarations

    logger.debug("Getting all positive samples")
    positive_samples_df = get_all_positive_samples()

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

    logger.debug("Getting location barcodes from labwhere")
    labware_to_location_barcode_df = map_labware_to_location(get_distinct_plate_barcodes())

    logger.debug("Joining location data from labwhere")
    merged = positive_samples_df.merge(
        labware_to_location_barcode_df, how="left", on="plate_barcode"
    )

    # TODO: abstract into new method
    declarations_records = [record for record in declarations]
    if len(declarations_records) > 0:
        logger.debug("Joining declarations")
        declarations_frame = pd.DataFrame.from_records(declarations_records)
        merged = merged.merge(declarations_frame, how="left", on="Root Sample ID")

        # Give a default value of Unknown to any entry that does not have a
        # sample declaration
        merged = merged.fillna({"Value In Sequencing": "Unknown"})

    pretty(logger, merged)

    merged = add_cherrypicked_column(merged)

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




