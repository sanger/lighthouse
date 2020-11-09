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
EVENTS_WH_DB = "event_warehouse_test"

WAREHOUSES_RW_CONN_STRING = "root@localhost"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"
MLWH_STOCK_RESOURCES_TABLE = "stock_resource"

EVENTS_WAREHOUSE_SUBJECTS_TABLE = "subjects"
EVENTS_WAREHOUSE_ROLES_TABLE = "roles"
EVENTS_WAREHOUSE_EVENTS_TABLE = "events"
EVENTS_WAREHOUSE_EVENT_TYPES_TABLE = "event_types"