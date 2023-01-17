from typing import Any, Dict, Final, List

from lighthouse.constants.fields import (
    FIELD_FILTERED_POSITIVE,
    FIELD_MUST_SEQUENCE,
    FIELD_PLATE_BARCODE,
    FIELD_PREFERENTIALLY_SEQUENCE,
    FIELD_PROCESSED,
    FIELD_SAMPLE_ID,
)
from lighthouse.constants.general import (
    FACET_COUNT_FILTERED_POSITIVE,
    FACET_COUNT_FIT_TO_PICK_SAMPLES,
    FACET_COUNT_MUST_SEQUENCE,
    FACET_COUNT_PREFERENTIALLY_SEQUENCE,
    FACET_DISTINCT_PLATE_BARCODE,
    FACET_FIT_TO_PICK_SAMPLES,
)

"""
Stage for mongo aggregation pipeline to select all the samples which are "fit to pick":
- we first need to merge the fields from the priority_samples collection
- we are then interested in samples which are:
    filtered_positive == True OR must_sequence == True
    (samples that are preferentially_sequence == True must also be filtered_positive == True
    in order to be pickable so no need to select these independantly)
"""
STAGES_FIT_TO_PICK_SAMPLES: Final[List[Dict[str, Any]]] = [
    # first perform a lookup from samples to priority_samples using the '_id' field from samples on 'sample_id' on
    #   priority_samples
    {
        "$lookup": {
            "from": "priority_samples",
            "let": {FIELD_SAMPLE_ID: "$_id"},
            "pipeline": [
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": [f"${FIELD_SAMPLE_ID}", f"$${FIELD_SAMPLE_ID}"]},
                                {"$eq": [f"${FIELD_PROCESSED}", True]},
                            ]
                        }
                    },
                },
                # include a project here to remove the other fields we are not interested in or could cause confusion
                #   such as '_created_at' and '_updated_at' which are automatically created by Eve
                {
                    "$project": {
                        FIELD_PROCESSED: 1,
                        FIELD_MUST_SEQUENCE: 1,
                        FIELD_PREFERENTIALLY_SEQUENCE: 1,
                    },
                },
            ],
            "as": "from_priority_samples",
        }
    },
    # replace the document with a merge of the original and the first element of the array created from the lookup
    #   above - this should always be 1 element
    {
        "$replaceRoot": {
            "newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$from_priority_samples", 0]}, "$$ROOT"]},
        }
    },
    # remove the lookup document
    {
        "$project": {
            "from_priority_samples": 0,
        },
    },
    # perform the match for fit to pick samples
    {
        "$match": {
            "$or": [
                {FIELD_FILTERED_POSITIVE: True},
                {FIELD_MUST_SEQUENCE: True},
            ],
        }
    },
    # add facets to make extracting counts efficient
    {
        "$facet": {
            FACET_FIT_TO_PICK_SAMPLES: [
                {"$match": {}},
            ],
            FACET_COUNT_FIT_TO_PICK_SAMPLES: [
                {"$count": "count"},
            ],
            FACET_COUNT_FILTERED_POSITIVE: [
                {"$match": {FIELD_FILTERED_POSITIVE: True}},
                {"$count": "count"},
            ],
            FACET_COUNT_MUST_SEQUENCE: [
                {"$match": {FIELD_MUST_SEQUENCE: True}},
                {"$count": "count"},
            ],
            FACET_COUNT_PREFERENTIALLY_SEQUENCE: [
                {"$match": {FIELD_PREFERENTIALLY_SEQUENCE: True}},
                {"$count": "count"},
            ],
        }
    },
]

FACETS_REPORT = {
    "$facet": {
        FACET_FIT_TO_PICK_SAMPLES: [
            {"$match": {}},
        ],
        FACET_COUNT_FIT_TO_PICK_SAMPLES: [
            {"$count": "count"},
        ],
        FACET_DISTINCT_PLATE_BARCODE: [
            {"$match": {FIELD_PLATE_BARCODE: {"$nin": ["", None]}}},
            {"$group": {"_id": None, "distinct": {"$addToSet": "$plate_barcode"}}},
        ],
    }
}
