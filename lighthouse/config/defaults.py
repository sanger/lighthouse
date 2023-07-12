# flake8: noqa
import os

from lighthouse.authorization import EventsAPITokenAuth, PriorityAPITokenAuth
from lighthouse.config.logging import *
from lighthouse.config.schemas import CHERRYPICK_TEST_DATA_SCHEMA, EVENTS_SCHEMA, PRIORITY_SAMPLES_SCHEMA
from lighthouse.constants.config import *

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
# When False, this option disables HATEOAS. Defaults to True.
HATEOAS = True
# CORS (Cross-Origin Resource Sharing) support. Allows API maintainers to specify which domains are allowed to perform
#  CORS requests. Allowed values are: None, a list of domains, or '*' for a wide-open API.
X_DOMAINS = "*"
# CORS (Cross-Origin Resource Sharing) support. Allows API maintainers to specify which headers are allowed to be sent
#   with CORS requests. Allowed values are: None or a list of headers names. Defaults to None.
X_HEADERS = ["Content-type", "Authorization"]
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
# Note that changes to the DOMAIN for public resources will also require updates to be made to
# lighthouse/routes/eve_routes.py
DOMAIN: dict = {
    "centres": {
        "internal_resource": True,
    },
    "cherrypick_test_data": {
        "internal_resource": True,  # Disabled unless explicitly overridden by the environment
        "url": "cherrypick-test-data",  # Dashes to match non-Eve endpoints
        "resource_methods": ["GET", "POST"],
        "bulk_enabled": False,
        "schema": CHERRYPICK_TEST_DATA_SCHEMA,
    },
    "events": {
        "authentication": EventsAPITokenAuth,
        "resource_methods": ["GET", "POST"],
        "schema": EVENTS_SCHEMA,
    },
    "imports": {
        # When True, this option will allow insertion of arbitrary, unknown fields to any API endpoint. Since most
        #   endpoints are read-only, this will allow all the fields to be shown.
        "allow_unknown": True
    },
    "priority_samples": {
        "authentication": PriorityAPITokenAuth,
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
    "samples": {
        "internal_resource": True,
    },
}
# Improve pagination performance. When optimization is active no count operation, which can be slow on large
#   collections, is performed on the database. This does have a few consequences. Firstly, no document count is returned.
#   Secondly, HATEOAS is less accurate: no last page link is available, and next page link is always included, even on
#   last page. On big collections, switching this feature on can greatly improve performance: no count operation, which
#   can be slow on large collections, is performed on the database.
OPTIMIZE_PAGINATION_FOR_SPEED = False
# Enable the Operations Log: https://docs.python-eve.org/en/stable/features.html#oplog
OPLOG = True

###
# mongo config (but consumed by Eve)
###
MONGO_DB = "lighthouseDevelopmentDB"
MONGO_URI = f"mongodb://{LOCALHOST}:27017/{MONGO_DB}?replicaSet=heron_rs"
MONGO_OPTIONS = {
    "connect": True,
    "tz_aware": False,  # we are not interested in storing "aware" datetimes at present
    "uuidRepresentation": "standard",  # this is needed to avoid a KeyError in Eve 2.0
}

###
# Crawler config
###
CRAWLER_BASE_URL = f"http://{LOCALHOST}:8100"

##
# Cherrytrack url
##
CHERRYTRACK_URL = f"http://{LOCALHOST}:3020"

###
# Labwhere config
###
LABWHERE_URL = f"https://{LOCALHOST}:3010"
LABWHERE_DESTROYED_BARCODE = os.environ.get("LABWHERE_DESTROYED_BARCODE", "lw-heron-destroyed-17338")

###
# Sequencescape config
###
SS_API_KEY = "development"
SS_URL = f"http://{LOCALHOST}:3000"
SS_PLATE_CONFIG = {
    SS_PLATE_TYPE_DEFAULT: {
        SS_UUID_PLATE_PURPOSE: "",
        SS_UUID_STUDY: "",
        SS_FILTER_FIT_TO_PICK: True,
        SS_ONLY_SUBMIT_NEW_SAMPLES: False,
    }
}
SS_UUIDS_CHERRYPICKED = {SS_UUID_PLATE_PURPOSE: "", SS_UUID_STUDY: ""}
SS_PLATE_CREATION_ENDPOINT = f"{ SS_URL }/api/v2/heron/plates"

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
# Beckman config
###
BECKMAN_ROBOTS = {
    "BKRB0001": {"name": "Robot 1", "uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b"},
    "BKRB0002": {"name": "Robot 2", "uuid": "4fe4ca2b-09a7-40d6-a0ce-0e5dd5f30c47"},
    "BKRB0003": {"name": "Robot 3", "uuid": "90d8bc7a-2f6e-4a5f-8bea-1e8d27a1ac89"},
    "BKRB0004": {"name": "Robot 4", "uuid": "675002fe-f364-47e4-b71f-4fe1bb7b5091"},
}
# failure types (shared by Beckman and Biosero fail screens in Lighthouse-UI)
ROBOT_FAILURE_TYPES = {
    "plate_too_low_empty": "Plate volumes are too low or empty",
    "general_software_error": "General software error",
    "robot_crashed": "The robot crashed",
    "sample_contamination": "Sample contamination occurred",
    "power_failure": "Power loss to instrument",
    "network_failure": "Cannot retrieve sample data",
    "SILAS_error": "Internal communication error in robot system",
    "instrument_loaded_incorrectly": "Labware has been incorrectly loaded onto instrument",
    "other": "Any other failure",
}

###
# Biosero config
###
BIOSERO_ROBOTS = {
    "CPA": {"name": "Robot 5", "uuid": "e465f4c6-aa4e-461b-95d6-c2eaab15e63f"},
    "CPB": {"name": "Robot 6", "uuid": "13325f3b-5f10-4c72-a590-8aa7203f108b"},
    "CPC": {"name": "Robot 7", "uuid": "41fe349d-0bcb-4839-a469-946611dd3ba9"},
    "CPD": {"name": "Robot 8", "uuid": "948c3a0c-7544-4a72-85cc-6b4e489c9725"},
}
