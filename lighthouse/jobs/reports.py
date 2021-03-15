import logging
import time

import pandas as pd
from flask import current_app as app

from lighthouse import scheduler
from lighthouse.constants.fields import FIELD_PLATE_BARCODE
from lighthouse.constants.general import REPORT_COLUMNS
from lighthouse.helpers.reports import (
    add_cherrypicked_column,
    get_distinct_plate_barcodes,
    get_fit_to_pick_samples,
    get_new_report_name_and_path,
    map_labware_to_location,
)

logger = logging.getLogger(__name__)


def create_report() -> str:
    """Creates a report for fit to pick samples which are on site. It uses the samples and priority_samples collection
    as well as retrieving location information from LabWhere.

    Returns:
        str -- filename of the report created.
    """
    logger.info("Creating fit to pick samples report")

    start = time.time()

    # get samples collection
    samples_collection = app.data.driver.db.samples
    fit_to_pick_samples_df = get_fit_to_pick_samples(samples_collection)

    logger.info("Getting location barcodes from LabWhere")
    labware_to_location_barcode_df = map_labware_to_location(get_distinct_plate_barcodes(samples_collection))

    logger.debug("Joining location data from LabWhere")
    merged = fit_to_pick_samples_df.merge(labware_to_location_barcode_df, how="left", on=FIELD_PLATE_BARCODE)

    merged = add_cherrypicked_column(merged)

    report_name, report_path = get_new_report_name_and_path()

    logger.info(f"Writing results to {report_path}")

    # Create a Pandas Excel writer using openpyxl as the engine
    writer = pd.ExcelWriter(report_path, engine="openpyxl")

    # Get the list (and order) of columns for the report from config otherwise fall back to pre-defined list
    columns = app.config.get("REPORT_COLUMNS", REPORT_COLUMNS)

    # Sheet 2 contains all fit to pick samples WITH location barcodes
    merged[merged.location_barcode.notnull()].to_excel(
        writer, sheet_name="FIT TO PICK WITH LOCATION", columns=columns, index=False
    )

    # Convert the dataframe to an openpyxl Excel object
    #  Sheet 1 contains all fit to pick samples with AND without location barcodes
    merged.to_excel(writer, sheet_name="ALL FIT TO PICK SAMPLES", columns=columns, index=False)

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
