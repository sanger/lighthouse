from typing import Any, Dict
import os

# If we're running in a container, then instead of localhost
# we want host.docker.internal, you can specify this in the
# .env file you use for docker. eg
# LOCALHOST=host.docker.internal
LOCALHOST = os.environ.get("LOCALHOST", "localhost")

# lighthouse config
BARACODA_URL = f"{LOCALHOST}:5000"
DOWNLOAD_REPORTS_URL = f"http://{LOCALHOST}:5000/reports"
LABWHERE_URL = f"{LOCALHOST}:3010"
LABWHERE_DESTROYED_BARCODE = os.environ.get(
    "LABWHERE_DESTROYED_BARCODE", "lw-heron-destroyed-17338"
)
LIGHTHOUSE_API_KEY = "develop"
REPORTS_DIR = "data/reports"

SS_API_KEY = "develop"
SS_HOST = f"{LOCALHOST}:3000"
SS_URL = f"{LOCALHOST}:3000"
SS_UUID_PLATE_PURPOSE = ""
SS_UUID_PLATE_PURPOSE_CHERRYPICKED = ""
SS_UUID_STUDY = ""
SS_UUID_STUDY_CHERRYPICKED = ""

EVENTS_WH_DB = "events_wh_db"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"
WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
WAREHOUSES_RW_CONN_STRING = f"root:root@{LOCALHOST}"

# The window size when generating the positive samples report
REPORT_WINDOW_SIZE = 2

X_DOMAINS = "*"

# APScheduler config
SCHEDULER_RUN = True
JOBS = [
    {
        "id": "job1",
        "func": "lighthouse.jobs.reports:create_report_job",
        "trigger": "cron",
        "day": "*",
        "hour": 2,
    }
]


# We need to define timezone because current flask_apscheduler does not load from TZ env
SCHEDULER_TIMEZONE = "Europe/London"
SCHEDULER_API_ENABLED = False

# Eve config
ALLOW_UNKNOWN = True
DEBUG = True
HATEOAS = True

SAMPLES_DECLARATIONS_SCHEMA: Dict = {
    "root_sample_id": {"type": "string", "required": True, "validation_errors": True},
    "value_in_sequencing": {
        "type": "string",
        "allowed": ["Yes", "No", "Unknown"],
        "required": True,
    },
    "declared_at": {
        "type": "datetime",
        "required": True,
    },
}
# We are overwriting the date format.
# By default eve DATE_FORMAT is set to RFC1123 standard which is %a, %d %b %Y %H:%M:%S GMT
# eg "2013-04-04T10:29:13"
DATE_FORMAT = r"%Y-%m-%dT%H:%M:%S"

# allow requests to set ?max_results= to more than the default
#  added for lighthouse-ui Imports page, to display all Imports in a table
PAGINATION_LIMIT = 10000

DOMAIN: Dict = {
    "samples": {},
    "imports": {},
    "centres": {},
    "samples_declarations": {
        "resource_methods": ["GET", "POST"],
        "bulk_enabled": True,
        "schema": SAMPLES_DECLARATIONS_SCHEMA,
    },
    "schema": {},
}

MONGO_HOST = f"{LOCALHOST}"
MONGO_PORT = 27017
MONGO_USERNAME = ""
MONGO_PASSWORD = ""
MONGO_DBNAME = ""
MONGO_QUERY_BLACKLIST = ["$where"]

# logging config
LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(asctime)-15s %(name)-30s:%(lineno)s %(log_color)s%(levelname)-5s %(message)s",  # noqa: E501
        },
        "verbose": {"format": "%(asctime)-15s %(name)-30s:%(lineno)s %(levelname)-5s %(message)s"},
    },
    "handlers": {
        "colored_stream": {
            "level": "DEBUG",
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
        "slack": {
            "level": "ERROR",
            "class": "lighthouse.utils.SlackHandler",
            "formatter": "verbose",
            "token": "",
            "channel_id": "",
        },
    },
    "loggers": {
        "lighthouse": {"handlers": ["console", "slack"], "level": "INFO", "propagate": True}
    },
}

DART_RESULT_VIEW = "CherrypickingInfo"
BARACODA_RETRY_ATTEMPTS = 3

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

BECKMAN_ROBOTS = {
    "BKRB0001": {"name": "Robot 1", "uuid": "082effc3-f769-4e83-9073-dc7aacd5f71b"},
    "BKRB0002": {"name": "Robot 2", "uuid": "4fe4ca2b-09a7-40d6-a0ce-0e5dd5f30c47"},
    "BKRB0003": {"name": "Robot 3", "uuid": "90d8bc7a-2f6e-4a5f-8bea-1e8d27a1ac89"},
    "BKRB0004": {"name": "Robot 4", "uuid": "675002fe-f364-47e4-b71f-4fe1bb7b5091"},
}
