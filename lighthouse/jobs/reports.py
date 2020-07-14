import logging
import time
from http import HTTPStatus

import pandas as pd  # type: ignore
import requests
from flask import current_app as app

from lighthouse import scheduler
from lighthouse.exceptions import ReportCreationError
from lighthouse.helpers.reports import get_new_report_name_and_path
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

    logger.debug("Getting list of distinct plate barcodes")
    # for some reason we have some records (documents in mongo language) where the plate_barcode
    #   is empty so ignore those
    distinct_plate_barcodes = samples.distinct(
        "plate_barcode", {"plate_barcode": {"$nin": ["", None]}}
    )
    logger.info(f"{len(distinct_plate_barcodes)} distinct barcodes")

    logger.debug("Getting location barcodes from labwhere")
    response = requests.post(
        f"http://{app.config['LABWHERE_URL']}/api/labwares/searches",
        json={"barcodes": distinct_plate_barcodes},
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
    if response.status_code == HTTPStatus.OK:
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
    else:
        raise ReportCreationError("Response from labwhere is not OK")


def create_report_job():
    """Scheduler's job to create the report within the scheduler's app context.

    Returns:
        str -- filename of report created
    """
    logger.info("Starting create_report job")
    with scheduler.app.app_context():
        create_report()
