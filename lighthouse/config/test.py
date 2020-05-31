from lighthouse.config.defaults import *  # noqa: F403, F401

# APScheduler
RUN_SCHEDULER = False

# Eve
MONGO_HOST = "127.0.0.1"
MONGO_DBNAME = "lighthouseTestDB"
MONGO_QUERY_BLACKLIST = ["$where"]  # not sure why this was required...

# Flask
TESTING = True
