from lighthouse.config.defaults import *  # noqa: F403, F401

# setting here will overwrite those in 'defaults.py'

# Flask config
TESTING = True

# APScheduler config
SCHEDULER_RUN = False

# Eve config
MONGO_HOST = "127.0.0.1"
MONGO_DBNAME = "lighthouseTestDB"
MONGO_QUERY_BLACKLIST = ["$where"]  # not sure why this was required...

# logging config
LOGGING["loggers"]["lighthouse"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["lighthouse"]["handlers"] = ["colored_stream"]  # noqa: F405

REPORTS_DIR = "tests/data/reports"

WAREHOUSES_RO_CONN_STRING = "root@localhost"
ML_WH_DB = "unified_warehouse_test"
EVENTS_WH_DB = "event_warehouse_test"

WAREHOUSES_RW_CONN_STRING = "root:root@localhost"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"

DART_SQL_SERVER_HOST = "localhost"
DART_SQL_SERVER_DATABASE = "DartTestDB"
DART_SQL_SERVER_USER = "SA"
DART_SQL_SERVER_PASSWORD = "MyS3cr3tPassw0rd"

DART_SQL_SERVER_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:"
    + DART_SQL_SERVER_HOST
    + ";DATABASE="
    + DART_SQL_SERVER_DATABASE
    + ";UID="
    + DART_SQL_SERVER_USER
    + ";PWD="
    + DART_SQL_SERVER_PASSWORD
)
MLWH_SAMPLE_TABLE = "sample"
MLWH_STOCK_RESOURCES_TABLE = "stock_resource"
MLWH_STUDY_TABLE = "study"

EVENT_WH_SUBJECTS_TABLE = "subjects"
EVENT_WH_ROLES_TABLE = "roles"
EVENT_WH_EVENTS_TABLE = "events"
EVENT_WH_EVENT_TYPES_TABLE = "event_types"
EVENT_WH_SUBJECT_TYPES_TABLE = "subject_types"
EVENT_WH_ROLE_TYPES_TABLE = "role_types"
