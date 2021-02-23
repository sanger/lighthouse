PRIORITY_SAMPLES_SCHEMA = {
    "sample_id": {
        "type": "objectid",
        "required": True,
        "unique": True,
        "check_with": "required_bools",  # validator defined in lighthouse.validators.priority_samples.py
    },
    "must_sequence": {
        "type": "boolean",
        "required": False,
    },
    "preferentially_sequence": {
        "type": "boolean",
        "required": False,
    },
    "processed": {
        "type": "boolean",
        "required": False,
        "default": False,
        "readonly": True,  # we want to keep this field in the schema but not allow direct updates
    },
}
