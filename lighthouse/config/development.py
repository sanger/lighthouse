# flake8: noqa
from lighthouse.config.defaults import *

# setting here will overwrite those in 'defaults.py'

###
# Eve config
###
DEBUG = True
API_TOKENS_PRIORITY = {
    "read_write": "priority_read_write_dev",
}
API_TOKENS_BIOSERO = {
    "read_write": "biosero_read_write_dev",
}

###
# APScheduler config
###
SCHEDULER_RUN = False

###
# mongo config (consumed by Eve)
###
MONGO_HOST = f"{LOCALHOST}"
MONGO_DBNAME = "lighthouseDevelopmentDB"

###
# Labwhere config
###
LABWHERE_URL = "https://localhost:3000"

###
# logging config
###
LOGGING["loggers"]["lighthouse"]["level"] = "DEBUG"
LOGGING["loggers"]["lighthouse"]["handlers"] = ["colored_stream_dev"]

###
# MLWH config
###
WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
MLWH_DB = "unified_warehouse_test"

WAREHOUSES_RW_CONN_STRING = f"root:root@{LOCALHOST}"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"


###
# Backman config
###
BECKMAN_ENABLE = True

###
# Cherrytrack config
###
CHERRYTRACK_URL = f"http://{LOCALHOST}:3020"
