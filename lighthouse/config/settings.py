import os

SETTINGS = {
    "ALLOW_UNKNOWN": True,
    "DEBUG": True,
    "HATEOAS": True,
    "DOMAIN": {"samples": {}, "imports": {}, "centres": {}, "schema": {}},
    # Let's just use the local mongod instance. Edit as needed.
    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    "MONGO_HOST": os.environ["MONGO_HOST"],
    "MONGO_PORT": int(os.environ["MONGO_PORT"]),
    "MONGO_USERNAME": os.environ["MONGO_USERNAME"],
    "MONGO_PASSWORD": os.environ["MONGO_PASSWORD"],
    # Name of the database on which the user can be authenticated,
    # needed if --auth mode is enabled.
    # MONGO_AUTH_SOURCE = '<dbname>'
    "MONGO_DBNAME": os.environ["MONGO_DBNAME"],
    "MONGO_QUERY_BLACKLIST": ["$where"],
}

if "MONGO_URI" in os.environ:
    SETTINGS["MONGO_URI"] = os.environ["MONGO_URI"]
