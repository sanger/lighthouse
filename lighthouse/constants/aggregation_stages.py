from typing import Any, Dict, Final, List

from lighthouse.constants.fields import (
    FIELD_FILTERED_POSITIVE,
    FIELD_MUST_SEQUENCE,
    FIELD_PREFERENTIALLY_SEQUENCE,
    FIELD_PROCESSED,
    FIELD_SAMPLE_ID,
)

"""
Stage for mongo aggregation pipeline to select all the samples which are "fit to pick":
- we first need to merge the fields from the priority_samples collection
- we are then interested in samples which are:
    filtered_positive == True OR must_sequence == True OR preferentially_sequence == True
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
                    }
                },
                # include a project here to remove the other fields we are not interested in or could cause confusion
                #   such as '_created_at' and '_updated_at' which are automatically created by Eve
                {"$project": {FIELD_MUST_SEQUENCE: 1, FIELD_PREFERENTIALLY_SEQUENCE: 1}},
            ],
            "as": "from_priority_samples",
        }
    },
    # replace the document with a merge of the original and the first element of the array created from the lookup
    #   above - this should always be 1 element
    {"$replaceRoot": {"newRoot": {"$mergeObjects": [{"$arrayElemAt": ["$from_priority_samples", 0]}, "$$ROOT"]}}},
    # remove the lookup document
    {"$project": {"from_priority_samples": 0}},
    # perform the match for fit to pick samples
    {
        "$match": {
            "$or": [
                {FIELD_FILTERED_POSITIVE: True},
                {FIELD_MUST_SEQUENCE: True},
                {FIELD_PREFERENTIALLY_SEQUENCE: True},
            ],
        }
    },
]
