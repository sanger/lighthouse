import logging
from http import HTTPStatus
from typing import Any, Dict, List, Optional

import requests
from flask import current_app as app

from lighthouse.exceptions import MissingCentreError, MissingSourceError, MultipleCentresError

logger = logging.getLogger(__name__)


def add_cog_barcodes(samples: List[Dict[str, str]]) -> List[Dict[str, str]]:
    logger.info(f"Getting COG-UK barcodes for {len(samples)} samples")

    centre_name = confirm_cente(samples)
    centre_prefix = get_centre_prefix(centre_name)

    baracoda_url = (
        f"http://{app.config['BARACODA_HOST']}:{app.config['BARACODA_PORT']}"
        f"/barcodes/{centre_prefix}/new"
    )
    try:
        for sample in samples:
            response = requests.post(baracoda_url)

            if response.status_code == HTTPStatus.CREATED:
                sample["cog_barcode"] = response.json()["barcode"]
            else:
                raise Exception("Unable to create COG barcodes")
    except Exception as e:
        logger.exception(e)
        raise e

    return samples


def get_centre_prefix(centre_name: str) -> str:
    try:
        logger.debug(f"/centres?where=name=='{centre_name}'")
        response = app.test_client().get(f"/centres?where=name=='{centre_name}'")
    except Exception:
        pass
    else:
        logger.debug(response.json)
        response_dict = response.json

    assert response_dict["_meta"]["total"] == 1

    try:
        return response_dict["_items"][0]["prefix"]
    except Exception as e:
        logger.exception(e)
        return ""


def get_samples(plate_barcode: str) -> Optional[List[Dict[str, str]]]:
    logger.info(f"Getting all samples for {plate_barcode}")

    samples = get_all_samples(f"/samples?where=plate_barcode=='{plate_barcode}'")

    logger.info(f"Found {len(samples)} samples for {plate_barcode}")

    return samples


def get_all_samples(url: str, samples: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
    """[summary]

    Arguments:
        url {str} -- [description]

    Keyword Arguments:
        samples {List} -- [description] (default: {None})

    Returns:
        List[Dict] -- [description]
    """
    logger.info(f"Requesting samples at {url}")

    if samples is None:
        samples = []

    try:
        response = app.test_client().get(url)
    except Exception as e:
        logger.exception(e)
        return []
    else:
        response_data_dict = response.get_json()

    try:
        if response_data_dict["_meta"]["total"] > 0:
            samples.extend(response_data_dict["_items"])

            if "next" in list(response_data_dict["_links"].keys()):
                return get_all_samples(response_data_dict["_links"]["next"]["href"], samples)
            else:
                return samples
        else:
            return []
    except KeyError as e:
        logger.exception(e)
        return []


def confirm_cente(samples: List[Dict[str, str]]) -> str:
    """Confirm that the centre for all the samples is populated and the same and return the centre
    name

    Arguments:
        samples {List} -- the list of samples to check

    Returns:
        str -- the name of the centre for these samples
    """
    logger.debug("confirm_cente()")

    try:
        # check that the 'source' field has a valid name
        for sample in samples:
            if not sample["source"]:
                raise MissingCentreError(sample)

        # create a set from the 'source' field to check we only have 1 unique centre for these
        #   samples
        centre_set = {sample["source"] for sample in samples}
        logger.debug(centre_set)
    except KeyError:
        raise MissingSourceError()
    else:
        if len(centre_set) > 1:
            raise MultipleCentresError()

    return centre_set.pop()


def create_post_body(barcode: str, samples: List[Dict[str, str]]) -> Dict[str, Any]:
    logger.debug("Creating POST body to send to SS")
    wells = []
    for sample in samples:
        well = {"coordinate": sample["coordinate"]}
        wells.append(well)
    body = {"plate_barcode": barcode, "wells": wells}

    logger.debug(body)

    return body


def send_to_ss(body: Dict[str, Any]) -> requests.Response:
    ss_url = f"http://{app.config['SS_HOST']}/plates/new/"

    logger.info(f"Sending {body} to {ss_url}")

    response = requests.post(ss_url, json=body)

    logger.debug(response.status_code)

    return response
