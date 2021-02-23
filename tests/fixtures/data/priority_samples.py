from lighthouse.constants.fields import FIELD_MUST_SEQUENCE, FIELD_PREFERENTIALLY_SEQUENCE, FIELD_PROCESSED

PRIORITY_SAMPLES = [
    {
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False,
    },
    {
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: True,
        FIELD_PROCESSED: True,
    },
    {
        FIELD_MUST_SEQUENCE: True,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: True,
    },
    {
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: True,
    },
    {
        FIELD_MUST_SEQUENCE: False,
        FIELD_PREFERENTIALLY_SEQUENCE: False,
        FIELD_PROCESSED: False,
    },
]
