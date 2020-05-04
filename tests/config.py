TEST_SETTINGS_EVE = {
    "ALLOW_UNKNOWN": True,
    "HATEOAS": True,
    "DOMAIN": {"samples": {}, "imports": {}, "centres": {}, "schema": {}},
    "DEBUG": True,
    # Let's just use the local mongod instance. Edit as needed.
    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    "MONGO_HOST": "127.0.0.1",
    "MONGO_PORT": 27017,
    # Skip this block if your db has no auth. But it really should.
    # MONGO_USERNAME = '<your username>'
    # MONGO_PASSWORD = '<your password>'
    # Name of the database on which the user can be authenticated,
    # needed if --auth mode is enabled.
    # MONGO_AUTH_SOURCE = '<dbname>'
    "MONGO_DBNAME": "lighthouseTestDB",
    "MONGO_QUERY_BLACKLIST": ["$where"],
}

TEST_CONFIG_FLASK = {
    "TESTING": True,
    "BARACODA_HOST": "127.0.0.1",
    "BARACODA_PORT": 5001,
    "UUID_PLATE_PURPOSE": "be98e1ce-799c-11ea-8526-acde48001122",
    "UUID_STUDY": "d4bebaa0-799c-11ea-8526-acde48001122",
}
