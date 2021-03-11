# flake8: noqa
import os

from lighthouse.authorization import APITokenAuth
from lighthouse.config.logging import *
from lighthouse.config.schemas import PRIORITY_SAMPLES_SCHEMA

###
# General config
###
REPORTS_DIR = "data/reports"
REPORT_WINDOW_SIZE = 84  # The window size when generating the fit to pick samples report
# If we're running in a container, then instead of localhost we want host.docker.internal, you can specify this in the
# .env file you use for docker. eg: LOCALHOST=host.docker.internal
LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")
DOWNLOAD_REPORTS_URL = f"http://{LOCALHOST}:5000/reports"

###
# Eve config
###
HATEOAS = True
# CORS (Cross-Origin Resource Sharing) support. Allows API maintainers to specify which domains are allowed to perform
#  CORS requests. Allowed values are: None, a list of domains, or '*' for a wide-open API.
X_DOMAINS = "*"
# We are overwriting the date format.
# By default eve DATE_FORMAT is set to RFC1123 standard which is %a, %d %b %Y %H:%M:%S GMT
# eg "2013-04-04T10:29:13"
DATE_FORMAT = r"%Y-%m-%dT%H:%M:%S"

RENDERERS = ["eve.render.JSONRenderer"]  # render all responses in JSON
# allow requests to set ?max_results= to more than the default
#  added for lighthouse-ui Imports page, to display all Imports in a table
PAGINATION_LIMIT = 10000

# A list of HTTP methods supported at resource endpoints, open to public access even when Authentication and
#   Authorization is enabled.
PUBLIC_METHODS = ["GET"]
PUBLIC_ITEM_METHODS = ["GET"]
DOMAIN = {
    "samples": {"internal_resource": True},
    "imports": {
        # When True, this option will allow insertion of arbitrary, unknown fields to any API endpoint. Since most
        #   endpoints are read-only, this will allow all the fields to be shown.
        "allow_unknown": True
    },
    "centres": {"internal_resource": True},
    "priority_samples": {
        "authentication": APITokenAuth,
        "item_title": "priority_sample",
        "resource_methods": ["GET", "POST"],
        "item_methods": ["GET", "PATCH", "PUT"],
        # If True, the patch document will be normalized according to schema. This means if a field is not included in
        #   the patch body, it will be reset to the default value in its schema. If False, the field which is not
        #   included in the patch body will be kept untouched.
        #   https://docs.python-eve.org/en/stable/features.html#editing-a-document-patch
        "normalize_on_patch": True,
        "bulk_enabled": True,
        "schema": PRIORITY_SAMPLES_SCHEMA,
    },
    "schema": {},
}
# Improve pagination performance. When optimization is active no count operation, which can be slow on large
#   collections, is performed on the database. This does have a few consequences. Firstly, no document count is returned.
#   Secondly, HATEOAS is less accurate: no last page link is available, and next page link is always included, even on
#   last page. On big collections, switching this feature on can greatly improve performance.#  no count operation, which
#   can be slow on large collections, is performed on the database.
OPTIMIZE_PAGINATION_FOR_SPEED = False
# Enable the Operations Log: https://docs.python-eve.org/en/stable/features.html#oplog
OPLOG = True

###
# mongo config (but consumed by Eve)
###
MONGO_OPTIONS = {"connect": True, "tz_aware": False}  # we are not interested in storing "aware" datetimes at present
MONGO_HOST = f"{LOCALHOST}"
MONGO_PORT = 27017
MONGO_USERNAME = ""
MONGO_PASSWORD = ""
MONGO_DBNAME = ""

###
# Baracoda config
###
BARACODA_URL = f"{LOCALHOST}:5000"
BARACODA_RETRY_ATTEMPTS = 3

###
# Labwhere config
###
LABWHERE_URL = f"{LOCALHOST}:3010"
LABWHERE_DESTROYED_BARCODE = os.environ.get("LABWHERE_DESTROYED_BARCODE", "lw-heron-destroyed-17338")

###
# Sequencescape config
###
SS_API_KEY = "develop"
SS_HOST = f"{LOCALHOST}:3000"
SS_URL = f"{LOCALHOST}:3000"
SS_UUID_PLATE_PURPOSE = ""
SS_UUID_PLATE_PURPOSE_CHERRYPICKED = ""
SS_UUID_STUDY = ""
SS_UUID_STUDY_CHERRYPICKED = ""

###
# MLWH config
###
MLWH_DB = "unified_warehouse_test"
EVENTS_WH_DB = "events_wh_db"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"

WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
WAREHOUSES_RW_CONN_STRING = f"root:root@{LOCALHOST}"

MLWH_SAMPLE_TABLE = "sample"
MLWH_STOCK_RESOURCES_TABLE = "stock_resource"
MLWH_STUDY_TABLE = "study"

EVENT_WH_SUBJECTS_TABLE = "subjects"
EVENT_WH_ROLES_TABLE = "roles"
EVENT_WH_EVENTS_TABLE = "events"
EVENT_WH_EVENT_TYPES_TABLE = "event_types"
EVENT_WH_SUBJECT_TYPES_TABLE = "subject_types"
EVENT_WH_ROLE_TYPES_TABLE = "role_types"

###
# APScheduler config
###
SCHEDULER_RUN = True
SCHEDULER_TIMEZONE = (
    "Europe/London"  # We need to define timezone because current flask_apscheduler does not load from TZ env
)
SCHEDULER_API_ENABLED = False
JOBS = [
    {
        "id": "job1",
        "func": "lighthouse.jobs.reports:create_report_job",
        "trigger": "cron",
        "day": "*",
        "hour": 2,
    }
]

###
# DART config
###
DART_SQL_SERVER_HOST = f"{LOCALHOST}"
DART_SQL_SERVER_USER = "SA"
DART_SQL_SERVER_PASSWORD = "MyS3cr3tPassw0rd"
DART_SQL_SERVER_DATABASE = "DartDevDB"

DART_RESULT_VIEW = "CherrypickingInfo"

# NB: Remember to copy this definition to any config which redefines any of the variables that are used to create it.
DART_SQL_SERVER_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER=tcp:{DART_SQL_SERVER_HOST};"
    f"DATABASE={DART_SQL_SERVER_DATABASE};"
    f"UID={DART_SQL_SERVER_USER};"
    f"PWD={DART_SQL_SERVER_PASSWORD}"
)

###
# Broker config
###
RMQ_HOST = f"{LOCALHOST}"
RMQ_PORT = 5672
RMQ_USERNAME = "guest"
RMQ_PASSWORD = "guest"
RMQ_VHOST = "/"
RMQ_DECLARE_EXCHANGE = True
RMQ_EXCHANGE = "lighthouse.examples"
RMQ_EXCHANGE_TYPE = "topic"
RMQ_ROUTING_KEY = "staging.event.#"
RMQ_LIMS_ID = "LH_LOCAL"

###
# Backman config
###
BECKMAN_ENABLE = False
BECKMAN_ROBOTS = {
    "BKRB0001": {"name": "Robot 1", "uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b"},
    "BKRB0002": {"name": "Robot 2", "uuid": "4fe4ca2b-09a7-40d6-a0ce-0e5dd5f30c47"},
    "BKRB0003": {"name": "Robot 3", "uuid": "90d8bc7a-2f6e-4a5f-8bea-1e8d27a1ac89"},
    "BKRB0004": {"name": "Robot 4", "uuid": "675002fe-f364-47e4-b71f-4fe1bb7b5091"},
}
BECKMAN_FAILURE_TYPES = {
    "robot_crashed": "The robot crashed",
    "sample_contamination": "Sample contamination occurred",
    "power_failure": "Power loss to instrument",
    "network_failure": "Cannot retrieve sample data",
    "SILAS_error": "Internal communication error in Beckman system",
    "instrument_loaded_incorrectly": "Labware has been incorrectly loaded onto instrument",
    "other": "Any other failure",
}
