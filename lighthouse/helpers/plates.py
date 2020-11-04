import logging
import re
from http import HTTPStatus
from typing import Any, Dict, List, Optional
import copy

import requests
from flask import current_app as app

from lighthouse.constants import (
    FIELD_COG_BARCODE,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_RNA_ID,
    FIELD_RESULT,
    FIELD_COORDINATE,
    FIELD_SOURCE,
    FIELD_PLATE_BARCODE,
    POSITIVE_SAMPLES_MONGODB_FILTER,
)
from lighthouse.exceptions import (
    DataError,
    MissingCentreError,
    MissingSourceError,
    MultipleCentresError,
)

from sqlalchemy.sql.expression import bindparam  # type: ignore
from sqlalchemy.sql.expression import and_  # type: ignore

from lighthouse.helpers.mlwh_db import create_mlwh_connection_engine, get_table
from lighthouse.helpers.dart_db import find_dart_source_samples_rows

logger = logging.getLogger(__name__)


class UnmatchedSampleError(Exception):
    pass


def add_cog_barcodes(samples: List[Dict[str, str]]) -> Optional[str]:

    centre_name = confirm_centre(samples)
    centre_prefix = get_centre_prefix(centre_name)
    num_samples = len(samples)

    logger.info(f"Getting COG-UK barcodes for {num_samples} samples")

    baracoda_url = (
        f"http://{app.config['BARACODA_URL']}"
        f"/barcodes_group/{centre_prefix}/new?count={num_samples}"
    )
    try:
        response = requests.post(baracoda_url)
        if response.status_code == HTTPStatus.CREATED:
            barcodes = response.json()["barcodes_group"]["barcodes"]
            for (sample, barcode) in zip(samples, barcodes):
                sample[FIELD_COG_BARCODE] = barcode
        else:
            raise Exception("Unable to create COG barcodes")
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access baracoda")

    # return centre prefix
    # TODO: I didn't know how else to get centre prefix?
    return centre_prefix


def get_centre_prefix(centre_name: str) -> Optional[str]:
    logger.debug(f"Getting the prefix for '{centre_name}'")
    try:
        #  get the centre collection
        centres = app.data.driver.db.centres

        # use a case insensitive search for the centre name
        filter = {"name": {"$regex": f"^(?i){centre_name}$"}}

        assert centres.count_documents(filter) == 1

        centre = centres.find_one(filter)

        prefix = centre["prefix"]

        logger.debug(f"Prefix for '{centre_name}' is '{prefix}'")

        return prefix
    except Exception as e:
        logger.exception(e)
        return None
    except AssertionError as e:
        logger.exception(e)
        raise DataError("Multiple centres with the same name")


def find_samples(query: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    samples = app.data.driver.db.samples

    samples_for_barcode = list(samples.find(query))

    logger.info(f"Found {len(samples_for_barcode)} samples")

    return samples_for_barcode


# TODO: remove once we are sure that we dont need anything other than positives
def get_samples(plate_barcode: str) -> Optional[List[Dict[str, Any]]]:

    samples_for_barcode = find_samples({FIELD_PLATE_BARCODE: plate_barcode})

    return samples_for_barcode


def get_positive_samples(plate_barcode: str) -> Optional[List[Dict[str, Any]]]:
    query_filter = copy.deepcopy(POSITIVE_SAMPLES_MONGODB_FILTER)
    query_filter[FIELD_PLATE_BARCODE] = plate_barcode

    samples_for_barcode = find_samples(query_filter)

    return samples_for_barcode


def query_for_cherrypicked_samples(rows):
    mongo_query = []
    for row in rows:
        sample_query = {
            FIELD_ROOT_SAMPLE_ID: row.root_sample_id,
            FIELD_RNA_ID: row.rna_id,
        }
        mongo_query.append(sample_query)
    return ({"$or": mongo_query},)
    {"$bucket": {"groupBy"}}


def filter_samples_with_conditions(samples, conditions):
    samples


def build_joined_rows_with_samples(rows, samples):
    for row in rows:
        samples[FIELD_ROOT_SAMPLE_ID]


def get_cherrypicked_samples(barcode):
    rows = find_dart_source_samples_rows(app, barcode)
    samples = find_samples(query_for_cherrypicked_samples(rows))

    joined_structure = join_rows_with_samples(rows, samples)

    return samples


def confirm_centre(samples: List[Dict[str, str]]) -> str:
    """Confirm that the centre for all the samples is populated and the same and return the centre
    name

    Arguments:
        samples {List} -- the list of samples to check

    Returns:
        str -- the name of the centre for these samples
    """
    logger.debug("confirm_centre()")

    try:
        # check that the 'source' field has a valid name
        for sample in samples:
            if not sample[FIELD_SOURCE]:
                raise MissingCentreError(sample)

        # create a set from the 'source' field to check we only have 1 unique centre for these
        #   samples
        centre_set = {sample[FIELD_SOURCE] for sample in samples}
    except KeyError:
        raise MissingSourceError()
    else:
        if len(centre_set) > 1:
            raise MultipleCentresError()

    return centre_set.pop()


def create_post_body(barcode: str, samples: List[Dict[str, str]]) -> Dict[str, Any]:
    logger.debug(f"Creating POST body to send to SS for barcode '{barcode}'")

    wells_content = {}
    for sample in samples:
        for key, value in sample.items():
            if key.strip() == FIELD_RESULT:
                phenotype = value

            if key.strip() == FIELD_ROOT_SAMPLE_ID:
                description = value

        assert phenotype is not None
        assert sample[FIELD_COG_BARCODE] is not None

        well = {
            "content": {
                "phenotype": phenotype.strip().lower(),
                "supplier_name": sample[FIELD_COG_BARCODE],
                "sample_description": description,
            }
        }
        wells_content[sample[FIELD_COORDINATE]] = well

    body = {
        "barcode": barcode,
        "purpose_uuid": app.config["SS_UUID_PLATE_PURPOSE"],
        "study_uuid": app.config["SS_UUID_STUDY"],
        "wells": wells_content,
    }

    return {"data": {"type": "plates", "attributes": body}}


def send_to_ss(body: Dict[str, Any]) -> requests.Response:
    ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

    logger.info(f"Sending {body} to {ss_url}")

    headers = {"X-Sequencescape-Client-Id": app.config["SS_API_KEY"]}

    try:
        response = requests.post(ss_url, json=body, headers=headers)
        logger.debug(response.status_code)
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access SS")

    return response


def update_mlwh_with_cog_uk_ids(samples: List[Dict[str, str]]) -> None:
    """Update the MLWH to write the COG UK barcode for each sample.

    Arguments:
        samples {List[Dict[str, str]]} -- list of samples to be updated
    """
    if len(samples) == 0:
        return None

    # assign db_connection to avoid UnboundLocalError in 'finally' block, in case of exception
    db_connection = None
    try:
        data = []
        for sample in samples:
            # using 'b_' prefix for the keys because bindparam() doesn't allow you to use the real column names
            data.append(
                {
                    "b_root_sample_id": sample[FIELD_ROOT_SAMPLE_ID],
                    "b_rna_id": sample[FIELD_RNA_ID],
                    "b_result": sample[FIELD_RESULT],
                    "b_cog_uk_id": sample[FIELD_COG_BARCODE],
                }
            )

        sql_engine = create_mlwh_connection_engine(
            app.config["MLWH_RW_CONN_STRING"], app.config["ML_WH_DB"]
        )
        table = get_table(sql_engine, app.config["MLWH_LIGHTHOUSE_SAMPLE_TABLE"])

        stmt = (
            table.update()
            .where(
                and_(
                    table.c.root_sample_id == bindparam("b_root_sample_id"),
                    table.c.rna_id == bindparam("b_rna_id"),
                    table.c.result == bindparam("b_result"),
                )
            )
            .values(cog_uk_id=bindparam("b_cog_uk_id"))
        )
        db_connection = sql_engine.connect()

        results = db_connection.execute(stmt, data)

        rows_matched = results.rowcount
        if rows_matched != len(samples):
            msg = f"""
            Updating MLWH {app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} table with COG UK ids was only partially successful.
            Only {rows_matched} of the {len(samples)} samples had matches in the MLWH {app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} table.
            """
            logger.error(msg)
            raise UnmatchedSampleError(msg)
    except (Exception) as e:
        msg = f"""
        Error while updating MLWH {app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} table with COG UK ids.
        {type(e).__name__}: {str(e)}
        """
        logger.error(msg)
        raise
    finally:
        if db_connection is not None:
            db_connection.close()
