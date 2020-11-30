from lighthouse.config.defaults import *  # noqa: F403, F401

# setting here will overwrite those in 'defaults.py'

# Flask config
TESTING = True

# APScheduler config
SCHEDULER_RUN = False

# Eve config
MONGO_HOST = f"{LOCALHOST}"
MONGO_DBNAME = "lighthouseTestDB"
MONGO_QUERY_BLACKLIST = ["$where"]  # not sure why this was required...

# logging config
LOGGING["loggers"]["lighthouse"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["lighthouse"]["handlers"] = ["colored_stream"]  # noqa: F405

REPORTS_DIR = "tests/data/reports"

WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
ML_WH_DB = "unified_warehouse_test"
EVENTS_WH_DB = "event_warehouse_test"

WAREHOUSES_RW_CONN_STRING = f"root@{LOCALHOST}"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"

DART_SQL_SERVER_HOST = f"{LOCALHOST}"
DART_SQL_SERVER_DATABASE = "DartTestDB"
DART_SQL_SERVER_USER = "SA"
DART_SQL_SERVER_PASSWORD = "MyS3cr3tPassw0rd"

DART_SQL_SERVER_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER=tcp:{DART_SQL_SERVER_HOST};"
    f"DATABASE={DART_SQL_SERVER_DATABASE};"
    f"UID={DART_SQL_SERVER_USER};"
    f"PWD={DART_SQL_SERVER_PASSWORD}"
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

RMQ_HOST = f"{LOCALHOST}"
RMQ_PORT = 5672
RMQ_USERNAME = "guest"
RMQ_PASSWORD = "guest"
RMQ_VHOST = "/"
RMQ_DECLARE_EXCHANGE = True
RMQ_EXCHANGE = "lighthouse.test.examples"
RMQ_EXCHANGE_TYPE = "topic"
RMQ_ROUTING_KEY = "test.event.#"
RMQ_LIMS_ID = "LH_TEST"

BECKMAN_FAILURE_TYPES = {
    "robot_crashed": "The robot crashed",
    "sample_contamination": "Sample contamination occurred",
    "other": "Any other failure",
}
