from lighthouse.constants.fields import (
    FIELD_EVENT_BARCODE,
    FIELD_EVENT_ERRORS,
    FIELD_EVENT_ROBOT,
    FIELD_EVENT_RUN_ID,
    FIELD_EVENT_TYPE,
    FIELD_EVENT_USER_ID,
    FIELD_EVENT_UUID,
)

# NOTE: Remember that the samples of 'plate_123' are joined to the priority samples
#   There should be 7 fit to pick samples from all the plates below
PLATE_EVENTS = [
    {
        FIELD_EVENT_RUN_ID: "1",
        FIELD_EVENT_BARCODE: "plate_123",
        FIELD_EVENT_TYPE: "lh_",
        FIELD_EVENT_USER_ID: "user_1",
        FIELD_EVENT_ROBOT: "robot1",
        FIELD_EVENT_UUID: "655b768d-7646-471c-8417-393e7ef44f69",
    },
    {
        FIELD_EVENT_RUN_ID: "2",
        FIELD_EVENT_BARCODE: "plate_456",
        FIELD_EVENT_TYPE: "lh_",
        FIELD_EVENT_USER_ID: "user_2",
        FIELD_EVENT_ROBOT: "robot2",
        FIELD_EVENT_UUID: "870ee913-dcf1-497c-bd54-f27297838ea6",
        FIELD_EVENT_ERRORS: {"user_id": ["The user id is not right"]},
    },
]
