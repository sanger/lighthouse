from lighthouse.constants.fields import (
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER,
    FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME,
    FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER,
    FIELD_EVENT_USER_ID,
)

RUNS = [
    {
        "id": 1,
        FIELD_EVENT_USER_ID: "ab1",
        FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "LHS000001",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: "CPA",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
    },
    {
        "id": 2,
        FIELD_EVENT_USER_ID: "ab2",
        FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "LHS000001",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: "CPA",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
    },
    {
        "id": 3,
        FIELD_EVENT_USER_ID: "ab3",
        FIELD_CHERRYTRACK_LIQUID_HANDLER_SERIAL_NUMBER: "LHS000001",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_NAME: "CPA",
        FIELD_CHERRYTRACK_AUTOMATION_SYSTEM_MANUFACTURER: "biosero",
    },
]
