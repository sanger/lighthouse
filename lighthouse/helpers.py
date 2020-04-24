import logging
from typing import Dict, List

import requests
from flask import current_app as app

from lighthouse.exceptions import MissingCentreError, MissingSourceError, MultipleCentresError

logger = logging.getLogger(__name__)


def get_cog_barcodes(samples: List[Dict]) -> List[Dict]:
    logger.info(f"Getting COG-UK barcodes for {len(samples)} samples")

    centre_name = confirm_cente(samples)
    centre_prefix = get_centre_prefix(centre_name)

    body = {"prefix": centre_prefix, "count": len(samples)}
    baracoda_url = (
        f"http://{app.config['BARACODA_HOST']}:{app.config['BARACODA_PORT']}/prefix/{prefix}/new"
    )
    try:
        response = requests.post(baracoda_url, body)
    except Exception as e:
        logger.exception(e)

    try:
        for idx, sample in samples:
            sample["cog_barcode"] = response.json()["barcode"][idx]
    except Exception as e:
        logger.exception(e)

    logger.debug(samples)
    return samples


def get_centre_prefix(centre_name: str) -> str:
    try:
        response = app.test_client().get(f"/centres?where=name=='{centre_name}'")
    except Exception:
        pass
    else:
        logger.debug(response.json())
        response_dict = response.json()["prefix"]

    assert response_dict["_meta"]["total"] == 1

    try:
        return response_dict["items"][0]["prefix"]
    except Exception as e:
        logger.exception(e)
        return ""


def get_samples(plate_barcode: str) -> List[Dict]:
    logger.info(f"Getting all samples for {plate_barcode}")
    try:
        samples = get_all_samples(f"/samples?where=plate_barcode=='{plate_barcode}'")

        logger.info(f"Found {len(samples)} samples for {plate_barcode}")

        return samples
    except Exception as e:
        logger.exception(e)


def get_all_samples(url: str, samples: List = None) -> List[Dict]:
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


def confirm_cente(samples: List[Dict]) -> str:
    """Confirm that the centre for all the samples is populated and the same and return the centre
    name

    Arguments:
        samples {List} -- the list of samples to check

    Returns:
        str -- the name of the centre for these samples
    """
    logger.debug("confirm_cente()")

    try:
        centre = {sample["source"] for sample in samples}
    except KeyError:
        raise MissingSourceError()
    else:
        if len(centre) > 1:
            raise MultipleCentresError()

    for sample in samples:
        if sample["source"] is None:
            raise MissingCentreError(sample)

    return centre
