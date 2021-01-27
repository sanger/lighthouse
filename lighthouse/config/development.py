# flake8: noqa
from lighthouse.config.defaults import *

# setting here will overwrite those in 'defaults.py'

###
# APScheduler config
###
SCHEDULER_RUN = False

###
# Labwhere config
###
LABWHERE_URL = "labw-uat.psd.sanger.ac.uk"

###
# mongo config
###
MONGO_HOST = f"{LOCALHOST}"
MONGO_DBNAME = "lighthouseDevelopmentDB"

###
# logging config
###
LOGGING["loggers"]["lighthouse"]["level"] = "DEBUG"
LOGGING["loggers"]["lighthouse"]["handlers"] = ["colored_stream"]

###
# MLWH config
###
WAREHOUSES_RO_CONN_STRING = f"root@{LOCALHOST}"
MLWH_DB = "unified_warehouse_test"

WAREHOUSES_RW_CONN_STRING = f"root:root@{LOCALHOST}"
MLWH_LIGHTHOUSE_SAMPLE_TABLE = "lighthouse_sample"
