EVENTS_SCHEMA = {
    "automation_system_run_id": {
        "required": True,
        "type": "integer",
    },
    "barcode": {
        "type": "string",
    },
    "event_type": {
        "required": True,
        "type": "string",
        "check_with": "plate_events_dependent_parameters",
    },
    "user_id": {
        "required": True,
        "type": "string",
    },
    "robot": {
        "required": True,
        "type": "string",
    },
    "event_wh_uuid": {
        "type": "string",
        "unique": True,
        "readonly": True,
    },
    "errors": {
        "type": "dict",
        "default": None,
        "nullable": True,
        "allow_unknown": True,
    },
}


PRIORITY_SAMPLES_SCHEMA = {
    "sample_id": {
        "type": "objectid",
        "required": True,
        "unique": True,
        "check_with": "priority_samples_required_bools",
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
