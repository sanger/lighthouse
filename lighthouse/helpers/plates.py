import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union, cast
from uuid import uuid4

import requests
from eve import Eve
from flask import current_app as app

from lighthouse.classes.beckman import Beckman
from lighthouse.constants.events import PE_BECKMAN_DESTINATION_CREATED, PE_BECKMAN_DESTINATION_FAILED
from lighthouse.constants.fields import (
    FIELD_BARCODE,
    FIELD_COG_BARCODE,
    FIELD_COORDINATE,
    FIELD_DART_CONTROL,
    FIELD_DART_DESTINATION_BARCODE,
    FIELD_DART_DESTINATION_COORDINATE,
    FIELD_DART_LAB_ID,
    FIELD_DART_LH_SAMPLE_UUID,
    FIELD_DART_RNA_ID,
    FIELD_DART_ROOT_SAMPLE_ID,
    FIELD_DART_SOURCE_BARCODE,
    FIELD_DART_SOURCE_COORDINATE,
    FIELD_LAB_ID,
    FIELD_LH_SAMPLE_UUID,
    FIELD_LH_SOURCE_PLATE_UUID,
    FIELD_PLATE_BARCODE,
    FIELD_PLATE_LOOKUP_LAB_ID,
    FIELD_PLATE_LOOKUP_RNA_ID,
    FIELD_PLATE_LOOKUP_SAMPLE_ID,
    FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_PADDED,
    FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_UNPADDED,
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
    FIELD_SS_SAMPLE_DESCRIPTION,
    FIELD_SS_SUPPLIER_NAME,
    FIELD_SS_UUID,
)
from lighthouse.constants.general import ARG_TYPE_DESTINATION, ARG_TYPE_SOURCE, BIOSCAN_PLATE_PURPOSE
from lighthouse.exceptions import DataError, MissingCentreError, MissingSourceError, MultipleCentresError
from lighthouse.helpers.dart import find_dart_source_samples_rows
from lighthouse.helpers.events import (
    construct_destination_plate_message_subject,
    construct_mongo_sample_message_subject,
    construct_robot_message_subject,
    construct_source_plate_message_subject,
    get_message_timestamp,
)
from lighthouse.helpers.general import get_fit_to_pick_samples_and_counts, has_plate_map_data
from lighthouse.helpers.reports import unpad_coordinate
from lighthouse.messages.message import Message
from lighthouse.types import SampleDoc, SampleDocs

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


def centre_prefixes_for_samples(samples: List[Dict[str, str]]) -> List[str]:
    return list(classify_samples_by_centre(samples).keys())


def get_centre_prefix(centre_name):
    logger.debug(f"Getting the prefix for '{centre_name}'")
    try:
        #  get the centre collection
        centres = cast(Eve, app).data.driver.db.centres

        # use a case insensitive search for the centre name
        filter = {"name": {"$regex": f"^(?i){centre_name}$"}}

        assert centres.count_documents(filter) == 1

        centre = centres.find_one(filter)

        prefix = centre["prefix"]

        logger.debug(f"Prefix for '{centre_name}' is '{prefix}'")

        return prefix
    except AssertionError as e:
        logger.exception(e)
        raise DataError("Multiple centres with the same name")
    except Exception as e:
        logger.exception(e)
        return None


def find_samples(query: Optional[Dict[str, Any]] = None) -> Optional[List[SampleDoc]]:
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

    samples_collection = cast(Eve, app).data.driver.db.samples

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
        "$or": [{FIELD_LH_SAMPLE_UUID: getattr(row, FIELD_DART_LH_SAMPLE_UUID)} for row in rows_without_controls(rows)]
    }


def equal_row_and_sample(row, sample):
    return sample[FIELD_LH_SAMPLE_UUID] == getattr(row, FIELD_DART_LH_SAMPLE_UUID)


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
                FIELD_SS_UUID: sample[FIELD_LH_SAMPLE_UUID],
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
    ss_url = f"{app.config['SS_URL']}/api/v2/heron/plates"

    logger.info(f"Sending request to: {ss_url}")

    headers = {"X-Sequencescape-Client-Id": app.config["SS_API_KEY"]}

    try:
        response = requests.post(ss_url, json=body, headers=headers)

        logger.debug(f"Response status code: {response.status_code}")

        return response
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access Sequencescape")


# TODO (DPL-572) move this class to another file?
class ControlLocations:
    def __init__(self, included: list) -> None:
        self.included = included

    def _get_sample_control_type(self, sample_id: list) -> Optional[str]:
        # Get the first sample
        sample = next(elem for elem in self.included if elem["type"] == "samples" and elem["id"] == sample_id)

        # Return the control type of the sample, if sample is a control
        return sample["attributes"]["control_type"] if sample["attributes"]["control"] is True else None

    def _get_control_types_for_aliquots(self, aliquot_ids: list) -> List[str]:
        # Get aliquots from included data
        aliquots = [elem for elem in self.included if elem["type"] == "aliquots" and elem["id"] in aliquot_ids]

        # Get the sample ids for the aliquot
        sample_ids = [aliquot["relationships"]["sample"]["data"]["id"] for aliquot in aliquots]
        control_types = [self._get_sample_control_type(id) for id in sample_ids]

        # Filter out any None control types
        return [ct for ct in control_types if ct is not None]

    def get_control_locations(self) -> dict:
        def get_control_type_for_well(well):
            # Get the aliquots ids for the well
            aliquot_ids = [aliquot["id"] for aliquot in well["relationships"]["aliquots"]["data"]]
            control_types = self._get_control_types_for_aliquots(aliquot_ids)

            # We expect there to only be one control per well
            return control_types[0] if len(control_types) == 1 else None

        # Get wells from included data
        wells = [elem for elem in self.included if elem["type"] == "wells"]

        # For each well, get the control type for the well
        # Create dict with key: well position, and value: control type
        # control_types = { "A1": "pcr pos", "B1": None, .....}
        control_types = {well["attributes"]["position"]["name"]: get_control_type_for_well(well) for well in wells}

        # Filter out any wells which are not controls
        return {k: v for (k, v) in control_types.items() if v is not None}


def covert_json_response_into_dict(barcode: str, json) -> dict:
    # Validate plate data exists
    if len(json["data"]) == 0:
        return {"data": None, "error": f"There is no plate data for barcode '{barcode}'"}

    # Validate plate purpose is as expected
    # plate_purpose = None
    if (included := json["included"]) is not None:
        purposes = [elem for elem in included if elem["type"] == "purposes"]

        # Validate only one plate pupose exists
        # TODO (DPL-572): check if is this needed? Could there ever be more than one purpose?
        if len(purposes) != 1:
            return {"data": None, "error": f"There should only be one purpose for barcode '{barcode}'"}

        purpose_name = purposes[0]["attributes"]["name"]

        if purpose_name != BIOSCAN_PLATE_PURPOSE:
            return {"data": None, "error": f"Incorrect purpose '{purpose_name}' for barcode '{barcode}'"}

        # Validate samples exists for plate
        samples = [elem for elem in included if elem["type"] == "samples"]
        if len(samples) == 0:
            return {"data": None, "error": f"There are no samples for barcode '{barcode}'"}

    # Instantiate wrapper class
    control_locations = ControlLocations(included)

    # Perform data processing, to retrieve well controls
    control_info = control_locations.get_control_locations()
    # { well_position: control_type } e.g.  {'A1': 'pcr positive', 'B1': 'pcr negative'}

    # Get the well position, for the +ve and -ve control types
    positive_control_position = [k for (k, v) in control_info.items() if v == "pcr positive"]
    negative_control_position = [k for (k, v) in control_info.items() if v == "pcr negative"]

    # Validate only one positive and one negative controls exist
    if len(positive_control_position) > 1 or len(negative_control_position) > 1:
        return {
            "data": None,
            "error": f"There should be only one positive and one negative control for barcode '{barcode}'",
        }

    # Validate both controls exist
    if len(positive_control_position) != 1 or len(negative_control_position) != 1:
        return {"data": None, "error": f"Missing positive or negative control for barcode '{barcode}'"}

    # Convert data into expected format for Beckman
    # This response was defined by the Beckman SAT
    locations = {
        "barcode": barcode,
        "positive_control": positive_control_position[0],
        "negative_control": negative_control_position[0],
    }

    return {"data": locations, "error": None}


def get_from_ss_plates_samples_info(plate_barcode: str) -> requests.Response:
    ss_url: str = f"{app.config['SS_URL']}/api/v2/labware"

    try:
        params = {"filter[barcode]": plate_barcode, "include": "purpose,receptacles.aliquots.sample"}
        response = requests.get(f"{ss_url}", params=params)

        logger.debug(f"Response status code: {response.status_code}")

        assert "data" in response.json(), f"Expected 'data' in response: {response.json()}"

        return response
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access Sequencescape")


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
                mapped_sample[FIELD_SS_PHENOTYPE] = mongo_row[FIELD_RESULT].strip().lower()
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
                "event_type": PE_BECKMAN_DESTINATION_CREATED,
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


def find_source_plates(query: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
    if query is None:
        return None

    source_plates = cast(Eve, app).data.driver.db.source_plates

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
                "event_type": PE_BECKMAN_DESTINATION_FAILED,
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
            sample[FIELD_SS_PHENOTYPE],
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
    robot_uuid = Beckman.get_robot_uuid(robot_serial_number)
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


def source_plate_field_generators(
    barcode: str,
) -> Dict[str, Callable[[], Union[str, bool, SampleDocs, Optional[int]]]]:
    """Creates an ungenerated response for a source plate lookup by creating lambda functions that can be called when
    the associated field is needed.

    Arguments:
        barcode (str): barcode of plate to get information for.

    Returns:
        Dict[str, Callable[[], Union[str, bool, SampleDocs, Optional[int]]]]: dict with lambda expresions to
        calculate the associated field when needed.
    """
    (
        fit_to_pick_samples,
        count_fit_to_pick_samples,
        count_must_sequence,
        count_preferentially_sequence,
        count_filtered_positive,
    ) = get_fit_to_pick_samples_and_counts(barcode)

    return {
        "plate_barcode": lambda: barcode,
        "has_plate_map": lambda: has_plate_map_data(barcode),
        "count_fit_to_pick_samples": lambda: (
            count_fit_to_pick_samples if count_fit_to_pick_samples is not None else 0
        ),
        "count_must_sequence": lambda: (count_must_sequence if count_must_sequence is not None else 0),
        "count_preferentially_sequence": lambda: (
            count_preferentially_sequence if count_preferentially_sequence is not None else 0
        ),
        "count_filtered_positive": lambda: (count_filtered_positive if count_filtered_positive is not None else 0),
        "pickable_samples": lambda: list(
            map(pickable_sample_attributes, cast(Iterable[SampleDoc], fit_to_pick_samples))
        ),
    }


def destination_plate_field_generators(
    barcode: str,
) -> Dict[str, Callable[[], Union[str, bool]]]:
    """Creates an ungenerated response for a destination plate lookup by creating lambda functions that can be called
    when the associated field is needed.

    Arguments:
        barcode (str): barcode of plate to get information for.

    Returns:
        Dict[str, Callable[[], Union[str, bool]]]: dict with lambda expresions to calculate the associated field when
        needed.
    """
    return {
        "plate_barcode": lambda: barcode,
        "plate_exists": lambda: plate_exists_in_ss(barcode),
    }


def plate_exists_in_ss(barcode: str) -> bool:
    """Check if a plate with given barcode exists in Sequencescape.

    Arguments:
        barcode (str): barcode of plate to get information for.

    Returns:
        bool: True if the plate exists, False otherwise.
    """
    logger.debug("plate_exists_in_ss()")
    try:
        ss_url: str = app.config["SS_URL"]
        params = {
            "filter[barcode]": barcode,
        }
        response = requests.get(f"{ss_url}/api/v2/labware", params=params)

        logger.debug(f"Response status code: {response.status_code}")

        assert "data" in response.json(), f"Expected 'data' in response: {response.json()}"

        if response.json()["data"]:
            return True

        return False
    except requests.ConnectionError:
        raise requests.ConnectionError("Unable to access Sequencescape")


def format_plate(
    barcode: str, exclude_props: Optional[List[str]] = None, plate_type: Optional[str] = ARG_TYPE_SOURCE
) -> Dict[str, Union[str, bool, SampleDocs, Optional[int]]]:
    """Used by flask route /plates to format each plate. Determines whether there is sample data for the barcode and if
    so, how many samples meet the fit to pick rules.
    It accepts a exclude_props argument to exclude certain fields from the response if they are not needed.

    Arguments:
        barcode (str): barcode of plate to get sample information for.
        exclude_props Optional[List[str]]: list of fields to exclude from the resulting object

    Returns:
        Dict[str, Union[str, bool, Optional[int]]]: sample information for the plate barcode
    """
    logger.info(f"Getting information for plate with barcode: {barcode}")

    # To solve default mutable arguments issue:
    # <https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/>
    exclude_props = exclude_props if exclude_props is not None else []

    # Obtain an dict with lambda expressions to generate required fields
    renderable: Dict[str, Any] = {}
    if plate_type == ARG_TYPE_DESTINATION:
        renderable = destination_plate_field_generators(barcode)
    else:
        renderable = source_plate_field_generators(barcode)

    formated_response: Dict[str, Any] = {}
    for field in renderable:
        if field not in exclude_props:
            formated_response[field] = renderable[field]()

    return formated_response


def pickable_sample_attributes(sample: SampleDoc) -> SampleDoc:
    """Renders into a Dict() the sample information from MongoDB to be sent inside a
    plate lookup call. This is currently in use for the Biosero robots to get the
    information of pickable samples in a source plate.

    Arguments:
        sample SampleDoc: A sample retrieved from MongoDB samples collection

    Returns:
        sample with the valid list of fields defined for a pickable sample
    """
    return {
        FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_PADDED: sample[FIELD_COORDINATE],
        FIELD_PLATE_LOOKUP_SOURCE_COORDINATE_UNPADDED: unpad_coordinate(sample[FIELD_COORDINATE]),
        FIELD_PLATE_LOOKUP_RNA_ID: sample[FIELD_RNA_ID],
        FIELD_PLATE_LOOKUP_LAB_ID: sample[FIELD_LAB_ID],
        FIELD_PLATE_LOOKUP_SAMPLE_ID: sample[FIELD_LH_SAMPLE_UUID],
    }
