from lighthouse.constants.events import EVENT_CHERRYPICK_LAYOUT_SET, PLATE_EVENT_DESTINATION_CREATED

EVENT_WH_DATA = {
    "subjects": [
        {"id": 1, "uuid": "1".encode("utf-8"), "friendly_name": "ss1", "subject_type_id": 1},
        {"id": 2, "uuid": "2".encode("utf-8"), "friendly_name": "ss2", "subject_type_id": 1},
        {"id": 3, "uuid": "5".encode("utf-8"), "friendly_name": "ss1-beck", "subject_type_id": 1},
        {"id": 4, "uuid": "6".encode("utf-8"), "friendly_name": "ss2-beck", "subject_type_id": 1},
    ],
    "roles": [
        {"id": 1, "event_id": 1, "subject_id": 1, "role_type_id": 1},
        {"id": 2, "event_id": 2, "subject_id": 2, "role_type_id": 1},
        {"id": 3, "event_id": 3, "subject_id": 3, "role_type_id": 1},
        {"id": 4, "event_id": 4, "subject_id": 4, "role_type_id": 1},
    ],
    "events": [
        {
            "id": 1,
            "lims_id": "SQSCP",
            "uuid": "1".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 2,
            "lims_id": "SQSCP",
            "uuid": "2".encode("utf-8"),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 3,
            "lims_id": "SQSCP",
            "uuid": "3".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 4,
            "lims_id": "SQSCP",
            "uuid": "4".encode("utf-8"),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
    ],
    "event_types": [
        {"id": 1, "key": EVENT_CHERRYPICK_LAYOUT_SET, "description": "stuff"},
        {"id": 2, "key": PLATE_EVENT_DESTINATION_CREATED, "description": "stuff"},
    ],
    "subject_types": [{"id": 1, "key": "sample", "description": "stuff"}],
    "role_types": [{"id": 1, "key": "sample", "description": "stuff"}],
}
