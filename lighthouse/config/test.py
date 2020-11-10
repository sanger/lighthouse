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

MLWH_CONN_STRING = "root@localhost"
ML_WH_DB = "unified_warehouse_test"

MLWH_RW_CONN_STRING = "root@localhost"
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
