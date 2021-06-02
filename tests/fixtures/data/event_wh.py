from lighthouse.constants.events import EVENT_CHERRYPICK_LAYOUT_SET, PE_BECKMAN_DESTINATION_CREATED
from tests.fixtures.data.uuids import testing_uuid_binary

EVENT_WH_DATA = {
    "subjects": [
        {"id": 1, "uuid": testing_uuid_binary(1), "friendly_name": "ss1", "subject_type_id": 1},
        {"id": 2, "uuid": testing_uuid_binary(2), "friendly_name": "ss2", "subject_type_id": 1},
        {"id": 3, "uuid": testing_uuid_binary(5), "friendly_name": "ss1-beck", "subject_type_id": 1},
        {"id": 4, "uuid": testing_uuid_binary(6), "friendly_name": "ss2-beck", "subject_type_id": 1},
        # Plate PB4
        {
            "id": 5,
            "uuid": testing_uuid_binary(35),
            "friendly_name": "pb_4",
            "subject_type_id": 1,
        },
        # Plate PB5
        {
            "id": 6,
            "uuid": testing_uuid_binary(36),
            "friendly_name": "pb_5",
            "subject_type_id": 1,
        },
    ],
    "roles": [
        {"id": 1, "event_id": 1, "subject_id": 1, "role_type_id": 1},
        {"id": 2, "event_id": 2, "subject_id": 2, "role_type_id": 1},
        {"id": 3, "event_id": 3, "subject_id": 3, "role_type_id": 1},
        {"id": 4, "event_id": 4, "subject_id": 4, "role_type_id": 1},
        # PB4 and PB5 are Beckman
        {"id": 5, "event_id": 4, "subject_id": 5, "role_type_id": 1},
        {"id": 6, "event_id": 4, "subject_id": 6, "role_type_id": 1},
    ],
    "events": [
        {
            "id": 1,
            "lims_id": "SQSCP",
            "uuid": testing_uuid_binary(1),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 2,
            "lims_id": "SQSCP",
            "uuid": testing_uuid_binary(2),
            "event_type_id": 1,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 3,
            "lims_id": "SQSCP",
            "uuid": testing_uuid_binary(3),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
        {
            "id": 4,
            "lims_id": "SQSCP",
            "uuid": testing_uuid_binary(4),
            "event_type_id": 2,
            "occured_at": "2015-11-25 11:35:30",
            "user_identifier": "test@example.com",
        },
    ],
    "event_types": [
        {"id": 1, "key": EVENT_CHERRYPICK_LAYOUT_SET, "description": "stuff"},
        {"id": 2, "key": PE_BECKMAN_DESTINATION_CREATED, "description": "stuff"},
    ],
    "subject_types": [{"id": 1, "key": "sample", "description": "stuff"}],
    "role_types": [{"id": 1, "key": "sample", "description": "stuff"}],
}
