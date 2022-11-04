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
API_TOKENS_EVENTS = {
    "biosero_read_write": "biosero_read_write_dev",
    "lighthouse_ui_read_write": "lighthouse_ui_read_write_dev",
}
DOMAIN["cherrypick_test_data"]["internal_resource"] = False

###
# APScheduler config
###
SCHEDULER_RUN = False

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
