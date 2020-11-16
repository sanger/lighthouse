from typing import Any, Dict

# lighthouse config
BARACODA_URL = "localhost:5000"
SS_API_KEY = "develop"
LIGHTHOUSE_API_KEY = "develop"
SS_URL = "localhost:3000"
LABWHERE_URL = "localhost:3010"
SS_UUID_PLATE_PURPOSE = ""
SS_UUID_STUDY = ""
SS_UUID_PLATE_PURPOSE_CHERRYPICKED = ""
SS_UUID_STUDY_CHERRYPICKED = ""
REPORTS_DIR = "data/reports"
DOWNLOAD_REPORTS_URL = "http://localhost:5000/reports"
SS_HOST = "localhost:3000"

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

DATE_FORMAT = r"%Y-%m-%dT%H:%M:%S"
# eg "2013-04-04T10:29:13"

PAGINATION_LIMIT = 10000
# allow requests to set ?max_results= to more than the default
#  added for lighthouse-ui Imports page, to display all Imports in a table

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
MONGO_HOST = "localhost"
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
            "format": "%(asctime)-15s %(name)-18s:%(lineno)s %(log_color)s%(levelname)-5s %(message)s",  # noqa: E501
        },
        "verbose": {"format": "%(asctime)-15s %(name)-18s:%(lineno)s %(levelname)-5s %(message)s"},
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

WAREHOUSES_RO_CONN_STRING = "root@localhost"
EVENTS_WH_DB = "events_wh_db"

WAREHOUSES_RW_CONN_STRING = "root:root@localhost"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"

DART_RESULT_VIEW = "CherrypickingInfo"
BARACODA_RETRY_ATTEMPTS = 3
