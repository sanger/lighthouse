import logging
import time

import pandas as pd  # type: ignore
from flask import current_app as app

from lighthouse import scheduler
from lighthouse.helpers.reports import (
    get_new_report_name_and_path,
    unpad_coordinate,
    map_labware_to_location,
    get_all_positive_samples,
    add_cherrypicked_column,
    get_distinct_plate_barcodes,
    join_samples_declarations
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
    logger.debug("Getting all positive samples")
    samples = app.data.driver.db.samples
    positive_samples_df = get_all_positive_samples(samples)

    logger.debug("Getting location barcodes from labwhere")
    labware_to_location_barcode_df = map_labware_to_location(get_distinct_plate_barcodes(samples))

    logger.debug("Joining location data from labwhere")
    merged = positive_samples_df.merge(
        labware_to_location_barcode_df, how="left", on="plate_barcode"
    )

    merged = join_samples_declarations(merged)

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




