import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4

import requests
from flask import current_app as app
from sqlalchemy.sql.expression import and_, bindparam

from lighthouse.constants.events import PLATE_EVENT_DESTINATION_CREATED, PLATE_EVENT_DESTINATION_FAILED
from lighthouse.constants.fields import (
    FIELD_BARCODE,
    FIELD_COG_BARCODE,
    FIELD_COORDINATE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_PLATE_BARCODE,
    FIELD_RESULT,
    FIELD_RNA_ID,
    FIELD_ROOT_SAMPLE_ID,
    FIELD_SOURCE,
    FIELD_SS_BARCODE,
    FIELD_SS_CONTROL,
    FIELD_SS_CONTROL_TYPE,
    FIELD_SS_COORDINATE,
    FIELD_SS_LAB_ID,
    FIELD_SS_NAME,
    FIELD_SS_PHENOTYPE,
    FIELD_SS_RESULT,
    FIELD_SS_SAMPLE_DESCRIPTION,
    FIELD_SS_SUPPLIER_NAME,
    FIELD_SS_UUID,
)
from lighthouse.exceptions import (
    DataError,
    MissingCentreError,
    MissingSourceError,
    MultipleCentresError,
    UnmatchedSampleError,
)
from lighthouse.helpers.dart import find_dart_source_samples_rows
from lighthouse.helpers.events import (
    construct_destination_plate_message_subject,
    construct_mongo_sample_message_subject,
    construct_robot_message_subject,
    construct_source_plate_message_subject,
    get_message_timestamp,
    get_robot_uuid,
)
from lighthouse.helpers.general import get_fit_to_pick_samples_and_counts
from lighthouse.helpers.mysql import create_mysql_connection_engine, get_table
from lighthouse.messages.message import Message
from lighthouse.types import SampleDoc

logger = logging.getLogger(__name__)


# TODO - Refactor:
# * move db calls (MLWH and Mongo) to separate files
# * consolidate small methods into larger ones if the small methods are not re-used elsewhere
# * make private methods obviously so, and don't explicitly test them
# On refactoring be careful to heed the WARNs in the code: not losing distributed functionality


def classify_samples_by_centre(samples: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    classified_samples = {}  # type: ignore
    for sample in samples:
        centre_name = sample[FIELD_SOURCE]
        if centre_name in classified_samples:
            classified_samples[centre_name].append(sample)
        else:
            classified_samples[centre_name] = [sample]
    return classified_samples


def add_cog_barcodes_from_different_centres(samples: List[Dict[str, str]]) -> List[str]:
    # Divide samples in centres and call add_cog_barcodes for each group
    classified_samples = classify_samples_by_centre(samples)

    for centre_name in classified_samples:
        add_cog_barcodes(classified_samples[centre_name])

    return list(classified_samples.keys())


def add_cog_barcodes(samples):
    centre_name = __confirm_centre(samples)
    centre_prefix = get_centre_prefix(centre_name)
    num_samples = len(samples)

    logger.info(f"Getting COG-UK barcodes for {num_samples} samples")

    baracoda_url = f"http://{app.config['BARACODA_URL']}" f"/barcodes_group/{centre_prefix}/new?count={num_samples}"

    retries = app.config["BARACODA_RETRY_ATTEMPTS"]
    success_operation = False
    except_obj = None

    while retries > 0:
        try:
            logger.debug(f"Attempting POST to {baracoda_url}")
            response = requests.post(baracoda_url)
            if response.status_code == HTTPStatus.CREATED:
                success_operation = True
                retries = 0
                barcodes = response.json()["barcodes_group"]["barcodes"]
                for (sample, barcode) in zip(samples, barcodes):
                    sample[FIELD_COG_BARCODE] = barcode
            else:
                retries = retries - 1
                logger.error("Unable to create COG barcodes")
                logger.error(response.json())
                except_obj = Exception("Unable to create COG barcodes")
        except requests.ConnectionError:
            retries = retries - 1
            logger.error("Unable to access baracoda")
            except_obj = requests.ConnectionError("Unable to access baracoda")

    if not success_operation and except_obj is not None:
        raise except_obj

    # TODO: I didn't know how else to get centre prefix?
    return centre_prefix


def get_centre_prefix(centre_name):
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


def find_samples(query: Dict[str, Any] = None) -> Optional[List[SampleDoc]]:
    """Query the samples collection with the given query.

    WARN - on refactoring this be careful not to lose the distributed functionality where None or empty DART rows
    returns None

    Arguments:
        query (Dict[str, Any], optional): a mongo query. Defaults to None.

    Returns:
        Optional[List[SampleDoc]]: list of samples
    """
    if query is None:
        return None

    samples_collection = app.data.driver.db.samples

    samples = list(samples_collection.find(query))

    logger.info(f"{len(samples)} samples found from samples collection")

    return samples


def row_is_normal_sample(row):
    control_value = getattr(row, FIELD_DART_CONTROL)
    return control_value is None or control_value == "NULL" or control_value == ""


def rows_without_controls(rows):
    return list(filter(lambda x: row_is_normal_sample(x), rows))


def rows_with_controls(rows):
    return list(filter(lambda x: not row_is_normal_sample(x), rows))


def query_for_cherrypicked_samples(rows: Optional[List[SampleDoc]]) -> Optional[Dict[str, Any]]:
    if rows is None or not rows:
        return None

    return {
        "$or": [
            {
                FIELD_ROOT_SAMPLE_ID: getattr(row, FIELD_DART_ROOT_SAMPLE_ID),
                FIELD_RNA_ID: getattr(row, FIELD_DART_RNA_ID),
                FIELD_LAB_ID: getattr(row, FIELD_DART_LAB_ID),
                FIELD_RESULT: {"$regex": "^positive", "$options": "i"},
            }
            for row in rows_without_controls(rows)
        ]
    }


def equal_row_and_sample(row, sample):
    return (
        (sample[FIELD_ROOT_SAMPLE_ID] == getattr(row, FIELD_DART_ROOT_SAMPLE_ID))
        and (sample[FIELD_RNA_ID] == getattr(row, FIELD_DART_RNA_ID))
        and (sample[FIELD_LAB_ID] == getattr(row, FIELD_DART_LAB_ID))
        and sample[FIELD_RESULT].lower() == "positive"
    )


def find_sample_matching_row(row, samples):
    return next((sample for sample in samples if equal_row_and_sample(row, sample)), None)


def join_rows_with_samples(rows, samples):
    return [
        {"row": row_to_dict(row), "sample": find_sample_matching_row(row, samples)}
        for row in rows_without_controls(rows)
    ]


def add_controls_to_samples(rows, samples):
    control_samples = [{"row": row_to_dict(row), "sample": None} for row in rows_with_controls(rows)]
    return samples + control_samples


def check_matching_sample_numbers(rows, samples):
    return len(samples) == len(rows_without_controls(rows))


def row_to_dict(row):
    columns = [
        FIELD_DART_DESTINATION_BARCODE,
        FIELD_DART_DESTINATION_COORDINATE,
        FIELD_DART_SOURCE_BARCODE,
        FIELD_DART_SOURCE_COORDINATE,
        FIELD_DART_CONTROL,
        FIELD_DART_ROOT_SAMPLE_ID,
        FIELD_DART_RNA_ID,
        FIELD_DART_LAB_ID,
    ]
    obj = {}
    for column in columns:
        obj[column] = getattr(row, column)
    return obj


def create_post_body(barcode: str, samples: List[Dict[str, str]]) -> Dict[str, Any]:
    logger.debug(f"Creating POST body to send to Sequencescape for barcode: {barcode}")

    wells_content = {}
    phenotype = None
    description = None
    for sample in samples:
        print(sample)
        for key, value in sample.items():
            if key.strip() == FIELD_RESULT:
                phenotype = value

            if key.strip() == FIELD_ROOT_SAMPLE_ID:
                description = value

        assert phenotype is not None
        assert sample[FIELD_COG_BARCODE] is not None

        well = {
            "content": {
                FIELD_SS_PHENOTYPE: phenotype.strip().lower(),
                FIELD_SS_SUPPLIER_NAME: sample[FIELD_COG_BARCODE],
                FIELD_SS_SAMPLE_DESCRIPTION: description,
                FIELD_SS_UUID: sample[FIELD_LH_SAMPLE_UUID]

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


def send_to_ss_heron_plates(body: Dict[str, Any]) -> requests.Response:
    """Send JSON body to the Sequencescape /heron/plates endpoint. This should create the plate in Sequencescape.

    Arguments:
        body (Dict[str, Any]): the info of the plate to create in Sequencescape.

    Raises:
        requests.ConnectionError: if a connection to Sequencescape is not able to be made.

    Returns:
        requests.Response: the response from Sequencescape.
    """
    ss_url = f"http://{app.config['SS_HOST']}/api/v2/heron/plates"

    logger.info(f"Sending request to: {ss_url}")

    headers = {"X-Sequencescape-Client-Id": app.config["SS_API_KEY"]}

    try:
        response = requests.post(ss_url, json=body, headers=headers)

        logger.debug(f"Response status code: {response.status_code}")

        return response
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access Sequencescape")


def update_mlwh_with_cog_uk_ids(samples: List[Dict[str, str]]) -> None:
    """Update the MLWH lighthouse_sample table with the COG UK barcode for each sample.

    Arguments:
        samples {List[Dict[str, str]]} -- list of samples to be updated.
    """
    logger.info("Attempting to update the lighthouse_sample table in the MLWH with the COG UK barcodes")

    if not samples:
        logger.warn("No samples")
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

        sql_engine = create_mysql_connection_engine(app.config["WAREHOUSES_RW_CONN_STRING"], app.config["MLWH_DB"])
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
        logger.info(f"{rows_matched} rows updated in MLWH")

        if rows_matched != len(samples):
            msg = (
                f"Updating MLWH {app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} table with COG UK ids was only partially "
                f"successful. Only {rows_matched} of the {len(samples)} samples had matches in the MLWH "
                f"{app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} table."
            )
            logger.error(msg)

            raise UnmatchedSampleError(msg)
    except Exception as e:
        logger.error(
            f"({type(e).__name__}: {str(e)}) Error while updating MLWH {app.config['MLWH_LIGHTHOUSE_SAMPLE_TABLE']} "
            "table with COG UK ids."
        )
        raise
    finally:
        if db_connection is not None:
            db_connection.close()


def map_to_ss_columns(samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mapped_samples = []

    for sample in samples:
        mapped_sample = {}

        mongo_row = sample["sample"]
        dart_row = sample["row"]

        try:
            if dart_row[FIELD_DART_CONTROL]:
                mapped_sample[FIELD_SS_SUPPLIER_NAME] = __supplier_name_for_dart_control(dart_row)
                mapped_sample[FIELD_SS_CONTROL] = True
                mapped_sample[FIELD_SS_CONTROL_TYPE] = dart_row[FIELD_DART_CONTROL]
                mapped_sample[FIELD_SS_UUID] = str(uuid4())
            else:
                mapped_sample[FIELD_SS_NAME] = mongo_row[FIELD_RNA_ID]
                mapped_sample[FIELD_SS_SAMPLE_DESCRIPTION] = mongo_row[FIELD_ROOT_SAMPLE_ID]
                mapped_sample[FIELD_SS_SUPPLIER_NAME] = mongo_row[FIELD_COG_BARCODE]
                mapped_sample[FIELD_SS_PHENOTYPE] = "positive"
                mapped_sample[FIELD_SS_RESULT] = mongo_row[FIELD_RESULT]
                mapped_sample[FIELD_SS_UUID] = mongo_row[FIELD_LH_SAMPLE_UUID]
                mapped_sample[FIELD_SS_LAB_ID] = mongo_row[FIELD_LAB_ID]

            mapped_sample[FIELD_SS_COORDINATE] = dart_row[FIELD_DART_DESTINATION_COORDINATE]
            mapped_sample[FIELD_SS_BARCODE] = dart_row[FIELD_DART_DESTINATION_BARCODE]
        except KeyError as e:
            logger.error(
                f"({type(e).__name__}: {str(e)}) Error while mapping database columns to Sequencescape columns for "
                f"sample with {FIELD_ROOT_SAMPLE_ID}: {mongo_row[FIELD_ROOT_SAMPLE_ID]}"
            )
            raise
        mapped_samples.append(mapped_sample)
    return mapped_samples


def create_cherrypicked_post_body(
    user_id,
    barcode,
    samples,
    robot_serial_number,
    source_plates,
):
    logger.debug(f"Creating POST body to send to Sequencescape for cherrypicked plate with barcode '{barcode}'")

    wells_content = {}
    for sample in samples:

        content = {}

        if FIELD_SS_CONTROL in sample:
            content[FIELD_SS_SUPPLIER_NAME] = sample[FIELD_SS_SUPPLIER_NAME]
            content[FIELD_SS_CONTROL] = sample[FIELD_SS_CONTROL]
            content[FIELD_SS_CONTROL_TYPE] = sample[FIELD_SS_CONTROL_TYPE].lower()
            content[FIELD_SS_UUID] = sample[FIELD_SS_UUID]
        else:
            content[FIELD_SS_NAME] = sample[FIELD_SS_NAME]
            content[FIELD_SS_PHENOTYPE] = sample[FIELD_SS_PHENOTYPE]
            content[FIELD_SS_SUPPLIER_NAME] = sample[FIELD_SS_SUPPLIER_NAME]
            content[FIELD_SS_SAMPLE_DESCRIPTION] = sample[FIELD_SS_SAMPLE_DESCRIPTION]
            content[FIELD_SS_UUID] = sample[FIELD_SS_UUID]

        wells_content[sample[FIELD_SS_COORDINATE]] = {"content": content}

    subjects = []
    subjects.append(__robot_subject(robot_serial_number))
    subjects.extend(__mongo_source_plate_subjects(source_plates))
    subjects.extend(__ss_sample_subjects(samples))

    events = [
        {
            "event": {
                "user_identifier": user_id,
                "event_type": PLATE_EVENT_DESTINATION_CREATED,
                "subjects": subjects,
                "metadata": {},
                "lims": app.config["RMQ_LIMS_ID"],
            }
        }
    ]

    body = {
        "barcode": barcode,
        "purpose_uuid": app.config["SS_UUID_PLATE_PURPOSE_CHERRYPICKED"],
        "study_uuid": app.config["SS_UUID_STUDY_CHERRYPICKED"],
        "wells": wells_content,
        "events": events,
    }

    return {"data": {"type": "plates", "attributes": body}}


# WARN - on refactoring, be careful not to lose the distributed functionality where
# None or empty samples returns None
def get_source_plates_for_samples(samples):
    barcodes = get_unique_plate_barcodes(samples)
    return find_source_plates(query_for_source_plate_uuids(barcodes))


def find_source_plates(query: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
    if query is None:
        return None

    source_plates = app.data.driver.db.source_plates

    source_plate_documents = list(source_plates.find(query))

    logger.info(f"Found {len(source_plate_documents)} source plates")

    return source_plate_documents


def get_unique_plate_barcodes(samples):
    return list({sample[FIELD_PLATE_BARCODE] for sample in samples})


def query_for_source_plate_uuids(barcodes):
    if not barcodes:  # checks for None and empty list
        return None

    return {"$or": [{FIELD_BARCODE: barcode} for barcode in barcodes]}


def construct_cherrypicking_plate_failed_message(
    barcode: str, user_id: str, robot_serial_number: str, failure_type: str
) -> Tuple[List[str], Optional[Message]]:
    try:
        subjects, errors = [], []

        # Add robot and destination plate subjects
        subjects.append(__robot_subject(robot_serial_number))
        subjects.append(construct_destination_plate_message_subject(barcode))

        # Try to add sample and source plate subjects
        dart_samples = None
        try:
            dart_samples = find_dart_source_samples_rows(barcode)
        except Exception as e:
            # a failed DART connection is valid:
            # it may be caused by the failure the user is trying to record
            logger.info(f"Failed to connect to DART: {e}")

        if dart_samples is None:
            # still send message, but inform caller that DART connection could not be made
            msg = (
                f"There was an error connecting to DART for destination plate '{barcode}'. "
                "As this may be due to the failure you are reporting, a destination plate failure "
                "has still been recorded, but without sample and source plate information"
            )
            logger.info(msg)
            errors.append(msg)
        elif len(dart_samples) == 0:
            # still send message, but inform caller that no samples were in the destination plate
            msg = (
                f"No samples were found in DART for destination plate '{barcode}'. As this may be "
                "due to the failure you are reporting, a destination plate failure has still been "
                "recorded, but without sample and source plate information"
            )
            logger.info(msg)
            errors.append(msg)
        else:
            mongo_samples = find_samples(query_for_cherrypicked_samples(dart_samples))
            if mongo_samples is None:
                return [f"No sample data found in Mongo matching DART samples in plate '{barcode}'"], None

            if not check_matching_sample_numbers(dart_samples, mongo_samples):
                return [f"Mismatch in destination and source sample data for plate '{barcode}'"], None

            # Add sample subjects for control and non-control DART entries
            dart_control_rows = [row_to_dict(row) for row in rows_with_controls(dart_samples)]
            subjects.extend([__sample_subject_for_dart_control_row(r) for r in dart_control_rows])
            subjects.extend([construct_mongo_sample_message_subject(s) for s in mongo_samples])

            # Add source plate subjects
            source_plates = get_source_plates_for_samples(mongo_samples)
            if not source_plates:
                return [f"No source plate data found in Mongo for DART samples in plate '{barcode}'"], None

            subjects.extend(__mongo_source_plate_subjects(source_plates))

        # Construct message
        message_content = {
            "event": {
                "uuid": str(uuid4()),
                "event_type": PLATE_EVENT_DESTINATION_FAILED,
                "occured_at": get_message_timestamp(),
                "user_identifier": user_id,
                "subjects": subjects,
                "metadata": {"failure_type": failure_type},
            },
            "lims": app.config["RMQ_LIMS_ID"],
        }
        return errors, Message(message_content)
    except Exception as e:
        logger.error("Failed to construct a cherrypicking plate failed message")
        logger.exception(e)
        return [
            "An unexpected error occurred attempting to construct the cherrypicking plate " f"failed event message: {e}"
        ], None


# Private methods


def __ss_sample_subjects(samples):
    subjects = []
    for sample in samples:
        if FIELD_SS_CONTROL in sample:
            subject = {
                "role_type": "control",
                "subject_type": "sample",
                "friendly_name": __ss_control_friendly_name(sample),
                "uuid": sample[FIELD_SS_UUID],
            }
        else:
            subject = {
                "role_type": "sample",
                "subject_type": "sample",
                "friendly_name": __ss_sample_friendly_name(sample),
                "uuid": sample[FIELD_SS_UUID],
            }
        subjects.append(subject)
    return subjects


def __ss_control_friendly_name(sample):
    return f"{sample[FIELD_SS_SUPPLIER_NAME]}"


def __ss_sample_friendly_name(sample):
    return "__".join(
        [
            sample[FIELD_SS_SAMPLE_DESCRIPTION],
            sample[FIELD_SS_NAME],
            sample[FIELD_SS_LAB_ID],
            sample[FIELD_SS_RESULT],
        ]
    )


def __supplier_name_for_dart_control(dart_row):
    return (
        f"{dart_row[FIELD_DART_CONTROL]} control: {dart_row[FIELD_DART_SOURCE_BARCODE]}_"
        f"{dart_row[FIELD_DART_SOURCE_COORDINATE]}"
    )


def __mongo_source_plate_subjects(source_plates):
    return [
        construct_source_plate_message_subject(plate[FIELD_BARCODE], plate[FIELD_LH_SOURCE_PLATE_UUID])
        for plate in source_plates
    ]


def __robot_subject(robot_serial_number):
    robot_uuid = get_robot_uuid(robot_serial_number)
    if not robot_uuid:
        raise KeyError(f"Unable to find events information for robot: {robot_serial_number}")

    return construct_robot_message_subject(robot_serial_number, robot_uuid)


def __confirm_centre(samples: List[Dict[str, str]]) -> str:
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


def __sample_subject_for_dart_control_row(dart_control_row: Dict[str, str]) -> Dict[str, str]:
    return {
        "role_type": "control",
        "subject_type": "sample",
        "friendly_name": __supplier_name_for_dart_control(dart_control_row),
        "uuid": str(uuid4()),
    }


def format_plate(barcode: str) -> Dict[str, Union[str, bool, Optional[int]]]:
    """Used by flask route /plates to format each plate. Determines whether there is sample data for the barcode and if
    so, how many samples meet the fit to pick rules.

    Arguments:
        barcode (str): barcode of plate to get sample information for.

    Returns:
        Dict[str, Union[str, bool, Optional[int]]]: sample information for the plate barcode
    """
    logger.info(f"Getting information for plate with barcode: {barcode}")

    (
        fit_to_pick_samples,
        count_fit_to_pick_samples,
        count_must_sequence,
        count_preferentially_sequence,
        count_filtered_positive,
    ) = get_fit_to_pick_samples_and_counts(barcode)

    return {
        "plate_barcode": barcode,
        "has_plate_map": fit_to_pick_samples is not None and len(fit_to_pick_samples) > 0,
        "count_fit_to_pick_samples": count_fit_to_pick_samples if count_fit_to_pick_samples is not None else 0,
        "count_must_sequence": count_must_sequence if count_must_sequence is not None else 0,
        "count_preferentially_sequence": count_preferentially_sequence
        if count_preferentially_sequence is not None
        else 0,
        "count_filtered_positive": count_filtered_positive if count_filtered_positive is not None else 0,
    }
