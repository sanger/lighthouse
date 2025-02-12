# flake8: noqa
from lighthouse.config.defaults import *

# setting here will overwrite those in 'defaults.py'

###
# Eve config
###
API_TOKENS_PRIORITY = {
    "read_write": "priority_read_write_test",
}
API_TOKENS_EVENTS = {
    "biosero_read_write": "biosero_read_write_test",
    "lighthouse_ui_read_write": "lighthouse_ui_read_write_test",
}
DOMAIN["cherrypick_test_data"]["internal_resource"] = False

###
# Flask config
###
TESTING = True

###
# APScheduler config
###
SCHEDULER_RUN = False

###
# General config
###
REPORTS_DIR = "tests/data/reports"

###
# mongo config
###
MONGO_QUERY_BLACKLIST = ["$where"]  # not sure why this was required...
MONGO_DB = "lighthouseTestDB"
MONGO_URI = f"mongodb://{LOCALHOST}:27017/{MONGO_DB}?replicaSet=heron_rs"

###
# Labwhere config
###
LABWHERE_DESTROYED_BARCODE = "heron-bin"

###
# logging config
###
LOGGING["loggers"]["lighthouse"]["level"] = "DEBUG"
LOGGING["loggers"]["lighthouse"]["handlers"] = ["colored_stream_dev"]

###
# MLWH config
###
MLWH_DB = "unified_warehouse_test"
EVENTS_WH_DB = "event_warehouse_test"

WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
WAREHOUSES_RW_CONN_STRING = f"root@{LOCALHOST}"

###
# DART config
###
DART_SQL_SERVER_DATABASE = "DartTestDB"

# NB: Create the connection string here as we define the database here. Since a f-string is evaluated immediately,
# it cannot only live in defaults.py if we redefine any of the variables that are used to create it.
DART_SQL_SERVER_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER=tcp:{DART_SQL_SERVER_HOST};"
    f"DATABASE={DART_SQL_SERVER_DATABASE};"
    f"UID={DART_SQL_SERVER_USER};"
    f"PWD={DART_SQL_SERVER_PASSWORD};"
    f"TrustServerCertificate=yes;"
)

###
# Broker config
###
RMQ_EXCHANGE = "lighthouse.test.examples"
RMQ_ROUTING_KEY = "test.event.#"
RMQ_LIMS_ID = "LH_TEST"

###
# Robot config
###
ROBOT_FAILURE_TYPES = {key: ROBOT_FAILURE_TYPES[key] for key in ("robot_crashed", "sample_contamination", "other")}

###
# SS plate creation config (UUID for the plate purpose and study of the plate created)
###
SS_PLATE_CONFIG = {
    SS_PLATE_TYPE_DEFAULT: {
        SS_UUID_PLATE_PURPOSE: "heron_purpose",
        SS_UUID_STUDY: "heron_study",
        SS_FILTER_FIT_TO_PICK: True,
        SS_ONLY_SUBMIT_NEW_SAMPLES: False,
    },
    "fit_to_pick_new_samples_only": {
        SS_UUID_PLATE_PURPOSE: "fit_to_pick_new_samples_purpose",
        SS_UUID_STUDY: "fit_to_pick_new_samples_study",
        SS_FILTER_FIT_TO_PICK: True,
        SS_ONLY_SUBMIT_NEW_SAMPLES: True,
    },
    "all_samples": {
        SS_UUID_PLATE_PURPOSE: "all_samples_purpose",
        SS_UUID_STUDY: "all_samples_study",
        SS_FILTER_FIT_TO_PICK: False,
        SS_ONLY_SUBMIT_NEW_SAMPLES: False,
    },
    "all_new_samples_only": {
        SS_UUID_PLATE_PURPOSE: "all_new_samples_purpose",
        SS_UUID_STUDY: "all_new_samples_study",
        SS_FILTER_FIT_TO_PICK: False,
        SS_ONLY_SUBMIT_NEW_SAMPLES: True,
    },
}
SS_UUIDS_CHERRYPICKED = {SS_UUID_PLATE_PURPOSE: "cherrypicked_purpose", SS_UUID_STUDY: "cherrypicked_study"}
