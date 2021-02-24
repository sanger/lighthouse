import logging
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from flask import current_app as app

from lighthouse.constants.aggregation_stages import FACETS_FIT_TO_PICK, STAGES_FIT_TO_PICK_SAMPLES
from lighthouse.constants.fields import FIELD_PLATE_BARCODE
from lighthouse.constants.general import (
    FACET_COUNT_FILTERED_POSITIVE,
    FACET_COUNT_FIT_TO_PICK_SAMPLES,
    FACET_COUNT_MUST_SEQUENCE,
    FACET_COUNT_PREFERENTIALLY_SEQUENCE,
    FACET_FIT_TO_PICK_SAMPLES,
)
from lighthouse.types import SampleDocs
from lighthouse.utils import pretty

logger = logging.getLogger(__name__)


def get_fit_to_pick_samples_and_counts(
    plate_barcode: str,
) -> Tuple[Union[SampleDocs, None], Union[int, None], Union[int, None], Union[int, None], Union[int, None]]:

    samples_collection = app.data.driver.db.samples

    # We are only interested in the samples for a particular plate
    pipeline: List[Dict[str, Any]] = [{"$match": {FIELD_PLATE_BARCODE: plate_barcode}}]

    #  Prepare the stages we need
    pipeline.extend(STAGES_FIT_TO_PICK_SAMPLES)
    pipeline.append(FACETS_FIT_TO_PICK)

    pretty(logger, pipeline)

    results = next(samples_collection.aggregate(pipeline))

    pretty(logger, results)

    if results is None:
        return None, None, None, None, None

    def extract_count(count_name: str) -> Optional[int]:
        if (facet_result := results.get(count_name)) is not None and facet_result:
            if (count := facet_result[0].get("count")) is not None:
                return cast(int, count)

        return None

    fit_to_pick_samples = results.get(FACET_FIT_TO_PICK_SAMPLES)
    count_fit_to_pick_samples = extract_count(FACET_COUNT_FIT_TO_PICK_SAMPLES)
    count_must_sequence = extract_count(FACET_COUNT_MUST_SEQUENCE)
    count_preferentially_sequence = extract_count(FACET_COUNT_PREFERENTIALLY_SEQUENCE)
    count_filtered_positive = extract_count(FACET_COUNT_FILTERED_POSITIVE)

    return (
        fit_to_pick_samples,
        count_fit_to_pick_samples,
        count_must_sequence,
        count_preferentially_sequence,
        count_filtered_positive,
    )
