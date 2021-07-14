CHERRYPICK_TEST_DATA_SCHEMA = {
    "add_to_dart": {
        "type": "boolean",
        "required": True,
    },
    "barcodes": {
        "type": "list",
        "readonly": True,
        "nullable": True,
    },
    "failure_reason": {
        "type": "string",
        "readonly": True,
        "nullable": True,
    },
    "plate_specs": {
        "type": "list",
        "required": True,
        "check_with": "validate_cptd_plate_specs",
    },
    "status": {
        "type": "string",
        "readonly": True,
    },
}

EVENTS_SCHEMA = {
    "automation_system_run_id": {
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
    "event_wh_uuid": {
        "type": "string",
        "unique": True,
        "readonly": True,
    },
    "errors": {
        "type": "dict",
        "default": None,
        "nullable": True,
        "allow_unknown": True,  # TODO: Are we should we want to allow unknown here?
    },
    "failure_type": {
        "type": "string",
    },
    "user_id": {
        "type": "string",
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
